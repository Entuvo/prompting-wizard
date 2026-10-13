"""Loopback-only read-only HTTP/SSE service. No filesystem-serving handler."""
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import secrets
import threading
from urllib.parse import parse_qs, urlsplit

from model import collect_registry

ASSETS = {'/':('index.html','text/html'), '/app.js':('app.js','text/javascript'), '/style.css':('style.css','text/css')}


class DashboardServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, registry, port, interval):
        self.registry = Path(registry).resolve()
        self.token = secrets.token_urlsafe(32)
        self.interval = interval
        self.changed = threading.Condition()
        self.stopped = threading.Event()
        self.snapshot = collect_registry(self.registry)
        self.version = 0
        super().__init__(('127.0.0.1', port), Handler)
        self.collector = threading.Thread(target=self.refresh, daemon=True)
        self.collector.start()

    def refresh(self):
        while not self.stopped.wait(self.interval):
            try:
                snapshot = collect_registry(self.registry, self.snapshot)
            except Exception as error:  # Keep the observer alive on any ordinary record/collector error.
                snapshot = {**self.snapshot, 'error':f'Registry unavailable: {type(error).__name__}',
                            'projects':[{**p, 'historical':True} for p in self.snapshot['projects']]}
            with self.changed:
                self.snapshot = snapshot
                self.version += 1
                self.changed.notify_all()

    def server_close(self):
        self.stopped.set()
        with self.changed: self.changed.notify_all()
        self.collector.join(5)
        super().server_close()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # Never log authentication query parameters.

    def send_common_headers(self, status, content_type):
        self.send_response(status)
        self.send_header('Content-Type', content_type + '; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")

    def reply(self, status, body, content_type='text/plain'):
        data = body.encode('utf-8')
        self.send_common_headers(status, content_type)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        hosts = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
        if self.headers.get('Host') not in hosts or (self.headers.get('Origin') and self.headers['Origin'] not in {'http://' + h for h in hosts}):
            self.reply(403, 'Local same-origin access required')
            return
        route = urlsplit(self.path)
        if route.path.startswith('/api/'):
            token = self.headers.get('Authorization', '').removeprefix('Bearer ')
            if route.path == '/api/events': token = parse_qs(route.query).get('token', [''])[0]
            if not token.isascii() or not hmac.compare_digest(token, self.server.token):
                self.reply(401, 'Open the authenticated URL printed by the dashboard launcher')
                return
        if route.path == '/api/snapshot':
            with self.server.changed: data = json.dumps(self.server.snapshot)
            self.reply(200, data, 'application/json')
        elif route.path == '/api/events':
            self.headers_out_events()
        elif route.path in ASSETS:
            name, content_type = ASSETS[route.path]
            self.reply(200, Path(__file__).with_name(name).read_text(), content_type)
        else:
            self.reply(404, 'Not found')

    def headers_out_events(self):
        self.send_common_headers(200, 'text/event-stream')
        self.end_headers()
        version = -1
        try:
            while not self.server.stopped.is_set():
                with self.server.changed:
                    self.server.changed.wait_for(lambda: self.server.version != version or self.server.stopped.is_set(), timeout=10)
                    version = self.server.version
                    data = json.dumps(self.server.snapshot, separators=(',', ':'))
                self.wfile.write(('event: snapshot\ndata: ' + data + '\n\n').encode())
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, TimeoutError):
            pass


def make_server(registry, port=0, interval=2):
    if not .05 <= interval <= 60: raise ValueError('Collection interval must be 0.05–60 seconds')
    return DashboardServer(registry, port, interval)
