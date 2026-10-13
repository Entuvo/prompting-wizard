import { describe, expect, it } from "bun:test";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  ChecksUnavailable,
  GhGitHubReader,
  WatcherQueryError,
  mapRollupNode,
  orderStack,
  parsePullRequest,
  parseReviewThreads,
  resolveChecks,
  resolveContext,
} from "./github.ts";
import {
  fakeReader,
  failedCheck,
  passingCheck,
  pendingCheck,
} from "./fakes.test-helper.ts";
import { parsePrNumber } from "./types.ts";
import { classifyPr, readSnapshot } from "./policy.ts";

const context = {
  owner: "owner",
  repo: "repo",
  number: parsePrNumber(42),
};

const reviewThread = (id: string, isResolved = true, run = "run-1") => ({
  id,
  isResolved,
  comments: {
    nodes: [{
      body: `RUN_ID: ${run}`,
      createdAt: "now",
      path: null,
      line: null,
      author: { login: "bugbot" },
    }],
  },
});
const threadPage = (nodes: unknown[], pageInfo: unknown) => ({
  data: { repository: { pullRequest: { reviewThreads: { nodes, pageInfo } } } },
});

// Substitute only the external gh process; exercise the real query, reader,
// parser and readiness policy without GitHub credentials or live PR changes.
async function withThreadPages(
  pages: Record<string, unknown>,
  check: (reader: GhGitHubReader) => Promise<void>
) {
  const directory = await mkdtemp(join(tmpdir(), "watch-pr-threads-"));
  const path = process.env.PATH;
  try {
    await writeFile(join(directory, "gh"), `#!${process.execPath}
const pages = ${JSON.stringify(pages)};
const cursor = process.argv.find(arg => arg.startsWith("after="))?.slice(6) ?? "first";
const response = pages[cursor];
if (response === undefined) process.exit(1);
const query = process.argv.find(arg => arg.startsWith("query=")) ?? "";
if (!query.includes("pageInfo")) {
  delete response.data?.repository?.pullRequest?.reviewThreads?.pageInfo;
}
if (cursor !== "first" && !query.includes("after: $after")) process.exit(1);
process.stdout.write(JSON.stringify(response));
`, { mode: 0o755 });
    process.env.PATH = `${directory}:${path ?? ""}`;
    await check(new GhGitHubReader());
  } finally {
    if (path === undefined) delete process.env.PATH;
    else process.env.PATH = path;
    await rm(directory, { recursive: true, force: true });
  }
}

const threadSnapshot = (reader: GhGitHubReader) => readSnapshot({
  reader: {
    ...fakeReader(),
    reviewThreads: (requested) => reader.reviewThreads(requested),
  },
  context,
  pendingHistory: "include",
  allowDraft: false,
});

describe("review thread pagination", () => {
  it("blocks readiness for an unresolved 101st thread and counts passes across pages", async () => {
    await withThreadPages({
      first: threadPage(Array.from({ length: 100 }, (_, i) => reviewThread(`${i}`)),
        { hasNextPage: true, endCursor: "next" }),
      next: threadPage([reviewThread("late-blocker", false, "run-2")],
        { hasNextPage: false, endCursor: "last" }),
    }, async (reader) => {
      const snapshot = await threadSnapshot(reader);
      expect(classifyPr(snapshot)).toMatchObject({
        kind: "blocker",
        blocker: { kind: "review-threads", threads: [{
          id: "late-blocker", isBugbot: true, bugbotReviewPasses: 2,
        }] },
      });
    });
  });

  it("reads every continuation, including a third page", async () => {
    await withThreadPages({
      first: threadPage([reviewThread("one", false)], { hasNextPage: true, endCursor: "two" }),
      two: threadPage([reviewThread("two", false)], { hasNextPage: true, endCursor: "three" }),
      three: threadPage([reviewThread("three", false)], { hasNextPage: false, endCursor: "last" }),
    }, async (reader) => {
      expect((await reader.reviewThreads(context)).map(thread => thread.id))
        .toEqual(["one", "two", "three"]);
    });
  });

  it("allows readiness after a complete empty connection", async () => {
    await withThreadPages({
      first: threadPage([], { hasNextPage: false, endCursor: null }),
    }, async (reader) => {
      expect(classifyPr(await threadSnapshot(reader)).kind).toBe("ready");
    });
  });

  for (const [label, pageInfo] of [
    ["missing pageInfo", undefined],
    ["missing hasNextPage", { endCursor: null }],
    ["non-boolean hasNextPage", { hasNextPage: "false", endCursor: null }],
    ["missing endCursor", { hasNextPage: true }],
    ["null continuation", { hasNextPage: true, endCursor: null }],
    ["empty continuation", { hasNextPage: true, endCursor: "" }],
    ["blank continuation", { hasNextPage: true, endCursor: " " }],
    ["non-string cursor", { hasNextPage: false, endCursor: 42 }],
  ] as const) {
    it(`fails closed on ${label}`, async () => {
      await withThreadPages({ first: threadPage([reviewThread("resolved")], pageInfo) },
        async (reader) => {
          await expect(threadSnapshot(reader)).rejects.toBeInstanceOf(WatcherQueryError);
        });
    });
  }

  it("fails closed on a repeated continuation cursor", async () => {
    await withThreadPages({
      first: threadPage([reviewThread("one")], { hasNextPage: true, endCursor: "again" }),
      again: threadPage([reviewThread("two")], { hasNextPage: true, endCursor: "again" }),
    }, async (reader) => {
      await expect(threadSnapshot(reader)).rejects.toBeInstanceOf(WatcherQueryError);
    });
  });

  it("fails closed on an empty nonterminal page", async () => {
    await withThreadPages({
      first: threadPage([], { hasNextPage: true, endCursor: "next" }),
      next: threadPage([], { hasNextPage: false, endCursor: null }),
    }, async (reader) => {
      await expect(threadSnapshot(reader)).rejects.toBeInstanceOf(WatcherQueryError);
    });
  });

  it("fails closed when a later page is incomplete", async () => {
    await withThreadPages({
      first: threadPage([reviewThread("resolved")], { hasNextPage: true, endCursor: "next" }),
      next: { data: { repository: { pullRequest: null } } },
    }, async (reader) => {
      await expect(threadSnapshot(reader)).rejects.toBeInstanceOf(WatcherQueryError);
    });
  });

  it("fails closed on GraphQL errors accompanying partial data", async () => {
    await withThreadPages({ first: {
      ...threadPage([], { hasNextPage: false, endCursor: null }),
      errors: [{ message: "Partial result" }],
    } }, async (reader) => {
      await expect(threadSnapshot(reader)).rejects.toBeInstanceOf(WatcherQueryError);
    });
  });
});

describe("checks fallback chain", () => {
  it("uses a non-empty fast-path result without a rollup query", async () => {
    const reader = fakeReader({
      fastPath: { kind: "checks", checks: [passingCheck("fast")] },
    });
    const read = await resolveChecks(reader, context);
    expect(read.source).toBe("gh-pr-checks");
    expect(read.checks.map((check) => check.name)).toEqual(["fast"]);
    expect(reader.calls).toEqual(["checksFastPath"]);
  });

  it("paginates GraphQL when the fast path is unusable", async () => {
    const reader = fakeReader({
      fastPath: { kind: "unusable", exitCode: 8, stderr: "" },
      rollupPages: [
        { checks: [passingCheck("first")], endCursor: "next" },
        { checks: [failedCheck("second")], endCursor: null },
      ],
    });
    const read = await resolveChecks(reader, context);
    expect(read.source).toBe("graphql-rollup");
    expect(read.checks.map((check) => check.name)).toEqual(["first", "second"]);
    expect(reader.calls).toEqual([
      "checksFastPath",
      "checkRollupPage:null",
      "checkRollupPage:next",
    ]);
  });

  it("falls back when valid fast-path JSON represented an empty list", async () => {
    const reader = fakeReader({
      fastPath: { kind: "checks", checks: [] },
      rollupPages: [{ checks: [pendingCheck("fallback")], endCursor: null }],
    });
    expect((await resolveChecks(reader, context)).checks[0].name).toBe(
      "fallback"
    );
    expect(reader.calls).toEqual(["checksFastPath", "checkRollupPage:null"]);
  });

  it("fails closed when both paths are empty", async () => {
    const reader = fakeReader({
      fastPath: {
        kind: "unusable",
        exitCode: 8,
        stderr: "credential cannot read checks",
      },
    });
    await expect(resolveChecks(reader, context)).rejects.toBeInstanceOf(
      ChecksUnavailable
    );
    expect(reader.calls).toEqual(["checksFastPath", "checkRollupPage:null"]);
  });
});

describe("rollup node mapping", () => {
  it("maps terminal and non-terminal CheckRun states fail closed", () => {
    const cases = [
      ["IN_PROGRESS", null, "pending", "PENDING"],
      ["COMPLETED", "SUCCESS", "passed", "SUCCESS"],
      ["COMPLETED", "NEUTRAL", "skipped", "NEUTRAL"],
      ["COMPLETED", "SKIPPED", "skipped", "SKIPPED"],
      ["COMPLETED", "ACTION_REQUIRED", "failed", "ACTION_REQUIRED"],
      ["COMPLETED", "TIMED_OUT", "failed", "FAILURE"],
      ["COMPLETED", "FUTURE_VALUE", "failed", "FAILURE"],
    ] as const;
    for (const [status, conclusion, kind, reportedState] of cases) {
      expect(
        mapRollupNode({
          __typename: "CheckRun",
          name: "ci",
          status,
          conclusion,
        })
      ).toMatchObject({ kind, reportedState });
    }
  });

  it("classifies an in-progress Code Review Gate from the rollup as the gate", () => {
    expect(
      mapRollupNode({
        __typename: "CheckRun",
        name: "Code Review Gate",
        status: "IN_PROGRESS",
        conclusion: null,
      })
    ).toMatchObject({ kind: "code-review-gate" });
    expect(
      mapRollupNode({
        __typename: "StatusContext",
        context: "Code Review Gate",
        state: "PENDING",
      })
    ).toMatchObject({ kind: "code-review-gate" });
  });

  it("maps StatusContext states and drops unknown typenames", () => {
    expect(
      mapRollupNode({
        __typename: "StatusContext",
        context: "ci",
        state: "EXPECTED",
      })
    ).toMatchObject({ kind: "pending", reportedState: "PENDING" });
    expect(
      mapRollupNode({
        __typename: "StatusContext",
        context: "ci",
        state: "FUTURE_VALUE",
      })
    ).toMatchObject({ kind: "failed", reportedState: "FUTURE_VALUE" });
    expect(mapRollupNode({ __typename: "FutureNode" })).toBeNull();
  });
});

describe("closed enum parsing", () => {
  const rawPullRequest = {
    mergeable: "MERGEABLE",
    mergeStateStatus: "CLEAN",
    reviewDecision: "APPROVED",
    headRefOid: "head",
    headRefName: "feature",
    baseRefName: "main",
    state: "OPEN",
    mergedAt: null,
    isDraft: false,
  };

  it("accepts mergeStateStatus CONFLICTING", () => {
    expect(
      parsePullRequest(
        { ...rawPullRequest, mergeStateStatus: "CONFLICTING" },
        context
      ).mergeStateStatus
    ).toBe("CONFLICTING");
  });

  it("reads gh's empty reviewDecision as no decision rather than a parse failure", () => {
    expect(
      parsePullRequest({ ...rawPullRequest, reviewDecision: "" }, context)
        .reviewDecision
    ).toBeNull();
  });

  it("still rejects an unknown reviewDecision", () => {
    expect(() =>
      parsePullRequest({ ...rawPullRequest, reviewDecision: "MAYBE" }, context)
    ).toThrow(WatcherQueryError);
  });

  it("rejects unknown enum values as retryable errors carrying the raw value", () => {
    try {
      parsePullRequest(
        { ...rawPullRequest, mergeStateStatus: "FUTURE_STATE" },
        context
      );
      throw new Error("expected parser to throw");
    } catch (error) {
      expect(error).toBeInstanceOf(WatcherQueryError);
      if (!(error instanceof WatcherQueryError)) throw error;
      expect(error.failure).toMatchObject({
        kind: "missing-key",
        retryable: true,
        rawValue: '"FUTURE_STATE"',
      });
    }
  });
});

it("annotates Bugbot threads with distinct review-pass counts", () => {
  const response = {
    data: {
      repository: {
        pullRequest: {
          reviewThreads: {
            nodes: [
              {
                id: "one",
                isResolved: false,
                comments: {
                  nodes: [
                    {
                      body: "RUN_ID: run-1",
                      createdAt: "now",
                      path: "a.ts",
                      line: 1,
                      author: { login: "bugbot" },
                    },
                  ],
                },
              },
              {
                id: "two",
                isResolved: false,
                comments: {
                  nodes: [
                    {
                      body: "CURSOR_AUTOMATION_ID: run-2 severity high",
                      createdAt: "now",
                      path: null,
                      line: null,
                      author: { login: "cursor" },
                    },
                  ],
                },
              },
              {
                id: "resolved",
                isResolved: true,
                comments: {
                  nodes: [
                    {
                      body: "RUN_ID: run-3",
                      createdAt: "now",
                      path: null,
                      line: null,
                      author: { login: "bugbot" },
                    },
                  ],
                },
              },
            ],
          },
        },
      },
    },
  };
  const threads = parseReviewThreads(response);
  expect(threads).toHaveLength(2);
  expect(threads.map((thread) => thread.isBugbot)).toEqual([true, true]);
  expect(threads.map((thread) => thread.bugbotReviewPasses)).toEqual([3, 3]);
});

describe("context and stack discovery", () => {
  it("returns a fully explicit context without any reader call", async () => {
    const reader = fakeReader();
    expect(
      await resolveContext({
        reader,
        owner: "explicit",
        repo: "repo",
        pr: context.number,
      })
    ).toEqual({ owner: "explicit", repo: "repo", number: context.number });
    expect(reader.calls).toEqual([]);
  });

  it("uses the local origin before currentPr for an explicit number", async () => {
    const reader = fakeReader({ origin: { owner: "local", repo: "checkout" } });
    expect(
      await resolveContext({
        reader,
        owner: null,
        repo: null,
        pr: context.number,
      })
    ).toEqual({ owner: "local", repo: "checkout", number: context.number });
    expect(reader.calls).toEqual(["originRepo"]);
  });

  it("orders the connected stack bottom-to-top", () => {
    const ordered = orderStack(context, [
      {
        number: parsePrNumber(41),
        headRefName: "base-feature",
        baseRefName: "main",
      },
      {
        number: context.number,
        headRefName: "feature",
        baseRefName: "base-feature",
      },
      {
        number: parsePrNumber(43),
        headRefName: "upstack",
        baseRefName: "feature",
      },
    ]);
    expect(ordered.map((item) => Number(item.number))).toEqual([41, 42, 43]);
  });
});
