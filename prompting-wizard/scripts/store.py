"""Local learner evidence. Standard library only; no model or network calls."""
from contextlib import closing, contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import stat
import tempfile
import time
import uuid

SKILLS = frozenset(('noun verb adjective adverb pronoun preposition conjunction determiner numeral interjection particle '
                   'role-framing few-shot-examples output-schemas task-decomposition reasoning-scaffolds negative-constraints '
                   'context-ordering system-prompts agent-and-tool-prompting self-critique-loops writing-evals token-economy '
                   'failure-diagnosis prompt-library capstone').split())
TTL = 30 * 86400


class RevisionConflict(ValueError):
    pass


def identifier(value):
    if not isinstance(value, str) or str(uuid.UUID(value)) != value:
        raise ValueError('Expected canonical UUID')
    return value


def string(value, limit=4096, empty=False):
    if not isinstance(value, str) or (not value and not empty) or len(value.encode()) > limit:
        raise ValueError('Invalid text field')
    return value


def skill(value, optional=False):
    if value is None and optional:
        return None
    if not isinstance(value, str) or value not in SKILLS:
        raise ValueError('Unknown skill')
    return value


def keys(record, required, optional=()):
    if not isinstance(record, dict) or not set(required) <= record.keys() or record.keys() - set(required) - set(optional):
        raise ValueError('Invalid record fields')


def workspace_path(value):
    string(value)
    path = Path(value)
    if not path.is_absolute():
        raise ValueError('Workspace must be absolute')
    return str(path.resolve())


def revisions(values):
    if not isinstance(values, list) or len(values) > 20:
        raise ValueError('Invalid source revisions')
    for value in values:
        string(value, 200)
    return values


class Store:
    def __init__(self, root, clock=time.time):
        root = Path(root)
        if os.name != 'posix' or not root.is_absolute() or root.is_symlink():
            raise ValueError('Owner-only absolute POSIX data root required')
        root.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.root = root.resolve()
        self.path = self.root / 'learner.sqlite3'
        self.clock = clock
        self._check_path(self.root, directory=True)
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
        except FileExistsError:
            pass
        else:
            os.close(fd)
        self._check_files()
        with self._db(initialize=True) as db:
            version = db.execute('PRAGMA user_version').fetchone()[0]
            if version == 0:
                if db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchone():
                    raise ValueError('Unrecognized existing database; not migrated')
                statements = [
                    'CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)',
                    'CREATE TABLE sessions (token TEXT PRIMARY KEY, host TEXT, native TEXT, workspace TEXT, lease REAL DEFAULT 0, UNIQUE(host,native))',
                    'CREATE TABLE observations (id TEXT PRIMARY KEY, workspace TEXT, created REAL, expires REAL, skill TEXT, claimed INTEGER DEFAULT 0, data TEXT)',
                    'CREATE TABLE findings (id TEXT PRIMARY KEY, observation_id TEXT REFERENCES observations(id) ON DELETE CASCADE, data TEXT)',
                    'CREATE TABLE lessons (id TEXT PRIMARY KEY, workspace TEXT, created REAL, data TEXT)',
                    'CREATE TABLE progress (hash TEXT PRIMARY KEY, original BLOB NOT NULL, baseline TEXT NOT NULL)',
                ]
                for statement in statements:
                    db.execute(statement)
                db.execute("INSERT INTO settings VALUES ('revision','0')")
                db.execute('PRAGMA user_version=1')
            if db.execute('PRAGMA user_version').fetchone()[0] == 1:
                db.execute('ALTER TABLE sessions ADD COLUMN model TEXT')
                db.execute('CREATE TABLE drafts (host TEXT, native TEXT, workspace TEXT, id TEXT, turn_id TEXT, prompt TEXT, expires REAL, PRIMARY KEY(host,native))')
                db.execute('PRAGMA user_version=2')
            if db.execute('PRAGMA user_version').fetchone()[0] == 2:
                db.execute('ALTER TABLE progress ADD COLUMN current BLOB')
                db.execute('UPDATE progress SET current=original')
                db.execute('PRAGMA user_version=3')
            if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                raise ValueError('Database integrity check failed')

    @staticmethod
    def _check_path(path, directory=False):
        info = path.lstat()
        valid_type = stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)
        if not valid_type or info.st_uid != os.getuid() or info.st_mode & 0o077 or (not directory and info.st_nlink != 1):
            raise ValueError('Unsafe managed path ownership, permissions, or link')

    def _check_files(self):
        self._check_path(self.root, directory=True)
        self._check_path(self.path)
        for suffix in ('-journal', '-wal', '-shm'):
            path = Path(str(self.path) + suffix)
            try:
                self._check_path(path)
            except FileNotFoundError:
                # SQLite may remove a sidecar when another writer commits.
                pass

    @contextmanager
    def _db(self, initialize=False):
        self._check_files()
        with closing(sqlite3.connect(self.path, timeout=2)) as db:
            db.row_factory = sqlite3.Row
            version = db.execute('PRAGMA user_version').fetchone()[0]
            if version > 3 or (version != 3 and not initialize):
                raise ValueError('Unsupported schema; database left unchanged')
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('PRAGMA secure_delete=ON')
            db.execute('PRAGMA journal_mode=DELETE')
            db.execute('BEGIN IMMEDIATE')
            try:
                if version in (1,2,3):
                    db.execute('DELETE FROM observations WHERE expires <= ?', (self.clock(),))
                if version in (2,3):
                    db.execute('DELETE FROM drafts WHERE expires <= ?', (self.clock(),))
                yield db
                db.commit()
            except BaseException:
                db.rollback()
                raise

    @staticmethod
    def _get(db, key, default=None):
        row = db.execute('SELECT value FROM settings WHERE key=?', (key,)).fetchone()
        return json.loads(row[0]) if row else default

    @staticmethod
    def _set(db, key, value):
        db.execute('INSERT INTO settings VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key,json.dumps(value)))

    def configure(self, workspace, mode):
        if mode not in ('after-result', 'lesson-only'):
            raise ValueError('Unknown feedback mode')
        if workspace is not None and self.root.is_relative_to(workspace_path(workspace)):
            raise ValueError('Data root must be outside captured workspaces')
        key = 'default_mode' if workspace is None else 'mode:' + workspace_path(workspace)
        with self._db() as db:
            self._set(db,key,mode)

    def set_paused(self, value):
        if type(value) is not bool:
            raise ValueError('Expected boolean')
        with self._db() as db:
            self._set(db,'paused',value)
            if value: db.execute('DELETE FROM drafts')

    def set_excluded(self, workspace, value):
        if type(value) is not bool:
            raise ValueError('Expected boolean')
        with self._db() as db:
            resolved=workspace_path(workspace)
            if not value and self.root.is_relative_to(resolved):
                raise ValueError('Data root must be outside captured workspaces')
            self._set(db,'excluded:'+resolved,value)
            if not value and self._get(db,'mode:'+resolved) is None:
                self._set(db,'mode:'+resolved,'default')
            if value:
                for row in db.execute('SELECT DISTINCT workspace FROM drafts').fetchall():
                    if Path(row[0]).is_relative_to(resolved):
                        db.execute('DELETE FROM drafts WHERE workspace=?',(row[0],))

    def _mode(self, db, workspace):
        if self._get(db, 'paused', False):
            return None
        path = Path(workspace)
        if any(self._get(db,'excluded:'+str(p),False) for p in (path,*path.parents)):
            return None
        # Explicit workspace opt-in is required even when a learner default exists.
        value=self._get(db,'mode:'+workspace)
        return self._get(db,'default_mode','lesson-only') if value == 'default' else value

    def mode(self, workspace):
        with self._db() as db:
            return self._mode(db,workspace_path(workspace))

    def status(self, workspace=None):
        with self._db() as db:
            count=db.execute('SELECT count(*) FROM observations').fetchone()[0]
            result = dict(has_progress=db.execute('SELECT 1 FROM progress').fetchone() is not None,
                        pending=count,revision=self._get(db,'revision',0),
                        paused=self._get(db,'paused',False),default_mode=self._get(db,'default_mode','lesson-only'),
                        warning='pending_queue_full' if count >= 1000 else None)
            if workspace is not None:
                workspace=workspace_path(workspace)
                result.update(workspace_mode=self._get(db,'mode:'+workspace),
                              effective_mode=self._mode(db,workspace),
                              excluded=any(self._get(db,'excluded:'+str(p),False)
                                           for p in (Path(workspace),*Path(workspace).parents)))
            return result

    def session_model(self, token):
        identifier(token)
        with self._db() as db:
            row=db.execute('SELECT model FROM sessions WHERE token=?',(token,)).fetchone()
            if row is None: raise ValueError('Unknown session token')
            return row['model']

    def read_progress(self):
        with self._db() as db:
            row=db.execute('SELECT current FROM progress').fetchone()
            return row[0].decode() if row else None

    def register_session(self, host, native, workspace):
        if host not in ('claude','codex'):
            raise ValueError('Unknown host')
        string(native,200)
        workspace=workspace_path(workspace)
        with self._db() as db:
            token=str(uuid.uuid4())
            db.execute('DELETE FROM sessions WHERE host=? AND native=?',(host,native))
            db.execute('INSERT INTO sessions(token,host,native,workspace) VALUES (?,?,?,?)',(token,host,native,workspace))
            return token

    def enter_session(self, token):
        identifier(token)
        with self._db() as db:
            if not db.execute('UPDATE sessions SET lease=? WHERE token=?',(self.clock()+7200,token)).rowcount:
                raise ValueError('Unknown session token')
            db.execute('DELETE FROM drafts WHERE (host,native) IN (SELECT host,native FROM sessions WHERE token=?)',(token,))

    def exit_session(self, token):
        identifier(token)
        with self._db() as db:
            db.execute('UPDATE sessions SET lease=0 WHERE token=?',(token,))

    def in_lesson(self, host, native):
        with self._db() as db:
            return bool(db.execute('SELECT 1 FROM sessions WHERE host=? AND native=? AND lease>?',(host,native,self.clock())).fetchone())

    def add_observation(self, record):
        with self._db() as db:
            return self._save_observation(db,record)

    def _save_observation(self, db, record):
        keys(record, ('id','host','session_id','turn_id','workspace','model_id','prompt','result','context_complete','skill'))
        identifier(record['id']); string(record['session_id'],200)
        if record['host'] not in ('claude','codex') or type(record['context_complete']) is not bool:
            raise ValueError('Invalid observation metadata')
        for field in ('turn_id','model_id'):
            if record[field] is not None: string(record[field],200)
        skill(record['skill'],optional=True)
        record=dict(record,workspace=workspace_path(record['workspace']))
        truncated=False
        for field in ('prompt','result'):
            string(record[field],1024*1024,empty=True)
            raw=record[field].encode()
            truncated |= len(raw)>16384
            record[field]=raw[:16384].decode('utf-8',errors='ignore')
        record['truncated']=truncated
        if self._mode(db,record['workspace']) is None:
            return None
        existing=db.execute('SELECT data FROM observations WHERE id=?',(record['id'],)).fetchone()
        if existing:
            if json.loads(existing[0]) != record:
                raise RevisionConflict('Observation ID already holds different evidence')
            return record['id']
        if db.execute('SELECT count(*) FROM observations').fetchone()[0]>=1000:
            return None
        now=self.clock()
        db.execute('INSERT INTO observations(id,workspace,created,expires,skill,data) VALUES (?,?,?,?,?,?)',
                   (record['id'],record['workspace'],now,now+TTL,record['skill'],json.dumps(record)))
        return record['id']


    def pending(self, skill=None, now=None):
        if skill is not None and skill not in SKILLS:
            raise ValueError('Unknown skill')
        with self._db() as db:
            rows=db.execute('SELECT data FROM observations WHERE expires>? AND (? IS NULL OR skill=? OR skill IS NULL) ORDER BY created DESC,id DESC LIMIT 100',
                            (max(self.clock(), now or self.clock()),skill,skill))
            records=[]
            for row in rows:
                item=json.loads(row[0])
                item['findings']=[json.loads(f[0]) for f in db.execute('SELECT data FROM findings WHERE observation_id=?',(item['id'],))]
                records.append(item)
            return records

    def evidence(self, observation_id):
        identifier(observation_id)
        with self._db() as db:
            row=db.execute('SELECT data FROM observations WHERE id=?',(observation_id,)).fetchone()
            return json.loads(row[0]) if row else None

    def claim_coaching(self, observation_id):
        identifier(observation_id)
        with self._db() as db:
            return bool(db.execute('UPDATE observations SET claimed=1 WHERE id=? AND claimed=0',(observation_id,)).rowcount)

    def add_finding(self, record):
        keys(record,('id','observation_id','skill','explanation','source_revisions'))
        identifier(record['id']); identifier(record['observation_id']); skill(record['skill'])
        string(record['explanation']); revisions(record['source_revisions'])
        with self._db() as db:
            if any(db.execute('SELECT 1 FROM '+table+' WHERE id=?',(record['id'],)).fetchone() for table in ('observations','lessons')):
                raise ValueError('Finding ID must identify only the finding')
            if not db.execute('SELECT 1 FROM observations WHERE id=?',(record['observation_id'],)).fetchone():
                raise ValueError('Observation unavailable')
            old=db.execute('SELECT data FROM findings WHERE observation_id=?',(record['observation_id'],)).fetchone()
            if old:
                if json.loads(old[0])==record:return
                raise RevisionConflict('Observation already has an unreviewed finding')
            db.execute('INSERT INTO findings VALUES (?,?,?)',(record['id'],record['observation_id'],json.dumps(record)))
            db.execute('UPDATE observations SET skill=? WHERE id=?',(record['skill'],record['observation_id']))

    def commit_lesson(self, record, expected_revision):
        keys(record,('id','kind','schema_version','observation_ids','skill','explanation','reflection','confirmed','source_revisions','approved_excerpt'),('progress_text','workspace'))
        identifier(record['id']); skill(record['skill']); string(record['explanation']); string(record['reflection'])
        string(record['approved_excerpt'],4096,empty=True); revisions(record['source_revisions'])
        ids=record['observation_ids']
        if record['kind']!='lesson' or type(record['schema_version']) is not int or record['schema_version']!=1 or record['confirmed'] is not True:
            raise ValueError('Lesson requires learner confirmation')
        if type(expected_revision) is not int or expected_revision<0 or not isinstance(ids,list) or not 0<=len(ids)<=20 or len(set(ids))!=len(ids):
            raise ValueError('Invalid lesson references or revision')
        for value in ids: identifier(value)
        with self._db() as db:
            if self._get(db,'revision',0)!=expected_revision:
                raise RevisionConflict('Progress changed; refresh before committing')
            if any(db.execute('SELECT 1 FROM '+table+' WHERE id=?',(record['id'],)).fetchone() for table in ('observations','findings')):
                raise ValueError('Lesson ID must identify only the lesson')
            workspaces=[]
            for value in ids:
                row=db.execute('SELECT workspace FROM observations WHERE id=?',(value,)).fetchone()
                if not row: raise ValueError('Observation unavailable')
                workspaces.append(row[0])
            if not ids:
                if not record.get('progress_text'): raise ValueError('Empty-example lesson requires course progress')
                workspaces.append(workspace_path(record.get('workspace')))
            elif 'workspace' in record and workspace_path(record['workspace']) not in workspaces:
                raise ValueError('Workspace does not match examples')
            # One workspace per lesson keeps workspace deletion precise.
            if len(set(workspaces))!=1: raise ValueError('Review each workspace separately')
            record=dict(record)
            progress_text=record.pop('progress_text',None)
            if progress_text is not None:
                string(progress_text,1024*1024)
                baseline=self._validate_progress(progress_text.encode())
                current=db.execute('SELECT baseline,current FROM progress').fetchone()
                if not current or current['baseline']!=baseline:
                    raise ValueError('Original Day 0 baseline must remain unchanged')
                old=current['current'].decode()
                old_day=int(re.search(r'^current_day: (\d+)$',old,re.M)[1])
                new_day=int(re.search(r'^current_day: (\d+)$',progress_text,re.M)[1])
                if old_day>=31 or new_day!=old_day+1:
                    raise ValueError('Complete exactly one current lesson')
                old_log=self._progress_log(old)
                new_log=self._progress_log(progress_text)
                prefix=old_log+'\n' if old_log else ''
                addition=new_log[len(prefix):] if new_log.startswith(prefix) else ''
                if len(addition.splitlines())!=1 or not re.match(r'^- Day '+str(old_day)+r'\b',addition):
                    raise ValueError('Preserve prior log and append exactly one current lesson')
                db.execute('UPDATE progress SET current=?',(progress_text.encode(),))
            db.execute('INSERT INTO lessons VALUES (?,?,?,?)',(record['id'],workspaces[0],self.clock(),json.dumps(record)))
            db.executemany('DELETE FROM observations WHERE id=?',((value,) for value in ids))
            self._set(db,'revision',expected_revision+1)
            return expected_revision+1

    def list_records(self, kind='all', cursor=None):
        if kind not in ('all','pending','reviewed'):
            raise ValueError('Unknown record kind')
        if cursor is not None and (not isinstance(cursor,str) or not cursor.isdigit() or len(cursor)>9):
            raise ValueError('Invalid cursor')
        offset=int(cursor or 0)
        with self._db() as db:
            parts=[]
            if kind in ('all','pending'):
                parts.append("SELECT created,id,'observation' AS kind,data FROM observations")
                parts.append("SELECT o.created,f.id,'finding' AS kind,f.data FROM findings f JOIN observations o ON o.id=f.observation_id")
            if kind in ('all','reviewed'):
                parts.append("SELECT created,id,'lesson' AS kind,data FROM lessons")
            rows=db.execute(' UNION ALL '.join(parts)+' ORDER BY created,id LIMIT 101 OFFSET ?',(offset,)).fetchall()
            return dict(records=[dict(kind=r['kind'],data=json.loads(r['data'])) for r in rows[:100]],cursor=str(offset+100) if len(rows)>100 else None)

    def delete(self, id=None, workspace=None, all_data=False, kind=None):
        if type(all_data) is not bool or sum((id is not None,workspace is not None,all_data))!=1:
            raise ValueError('Select exactly one deletion scope')
        if id is not None: identifier(id)
        if workspace is not None: workspace=workspace_path(workspace)
        tables={'observation':'observations','lesson':'lessons','finding':'findings'}
        if kind is not None and (id is None or kind not in tables): raise ValueError('Record kind requires ID')
        with self._db() as db:
            if all_data:
                for table in ('findings','observations','lessons','sessions','drafts','progress'):
                    db.execute('DELETE FROM '+table)
                self._set(db,'revision',self._get(db,'revision',0)+1)
            elif workspace is not None:
                for table in ('observations','lessons','sessions','drafts'):
                    # Descendant workspaces are part of the selected root.
                    for row in db.execute('SELECT DISTINCT workspace FROM '+table).fetchall():
                        if Path(row[0]).is_relative_to(workspace):
                            db.execute('DELETE FROM '+table+' WHERE workspace=?',(row[0],))
            else:
                selected=(tables[kind],) if kind else tuple(tables.values())
                if kind is None and sum(bool(db.execute('SELECT 1 FROM '+table+' WHERE id=?',(id,)).fetchone()) for table in selected)>1:
                    raise ValueError('Ambiguous ID; specify record kind')
                row=db.execute('SELECT o.id,o.data FROM findings f JOIN observations o ON o.id=f.observation_id WHERE f.id=?',(id,)).fetchone()
                if row and 'findings' in selected:db.execute('UPDATE observations SET skill=? WHERE id=?',(json.loads(row['data'])['skill'],row['id']))
                for table in selected:
                    db.execute('DELETE FROM '+table+' WHERE id=?',(id,))

    @staticmethod
    def _validate_progress(raw):
        if len(raw)>1024*1024: raise ValueError('Progress too large')
        text=raw.decode('utf-8')
        def section(name):
            matches=re.findall(r'^## '+re.escape(name)+r'\n(.*?)(?=^## |\Z)',text,re.M|re.S)
            if len(matches)!=1: raise ValueError('Missing or repeated progress section')
            return matches[0]
        if len(re.findall(r'^level: (?:novice|working|advanced)$',text,re.M))!=1 or len(re.findall(r'^current_day: (?:[1-9]|[12][0-9]|3[01])$',text,re.M))!=1:
            raise ValueError('Invalid course progress; original preserved')
        lever_names='noun verb adjective adverb pronoun preposition conjunction determiner numeral interjection particle'.split()
        lever_text=section('Levers')
        scores=re.findall(r'([a-z]+):\s*([1-5])(?=\s|$)',lever_text)
        if [name for name,_ in scores]!=lever_names or re.sub(r'[a-z]+:\s*[1-5](?=\s|$)','',lever_text).strip():
            raise ValueError('Invalid lever scores')
        if len(re.findall(r'^- .+',section('Tasks'),re.M))<3:
            raise ValueError('At least three recurring tasks required')
        log=section('Log')
        baselines=re.findall(r'^- Day 0[^\n]*baseline[^\n]*$',log,re.M)
        if len(baselines)>1:
            raise ValueError('Conflicting baselines')
        baseline=baselines[0] if baselines else ''
        if baseline and [name for name,_ in re.findall(r'([a-z]+) ([1-5])(?=,|$)',baseline.split('baseline',1)[1])]!=lever_names:
            raise ValueError('Invalid Day 0 baseline')
        return baseline

    @staticmethod
    def _progress_log(text):
        return re.search(r'^## Log\n(.*?)(?=^## |\Z)',text,re.M|re.S)[1].strip()

    def import_progress(self, path, expected_revision=None):
        raw=Path(path).read_bytes()
        baseline=self._validate_progress(raw)
        digest=hashlib.sha256(raw).hexdigest()
        with self._db() as db:
            old=db.execute('SELECT hash,current,baseline FROM progress').fetchone()
            if expected_revision is not None:
                if type(expected_revision) is not int or expected_revision<0 or self._get(db,'revision',0)!=expected_revision:
                    raise RevisionConflict('Progress changed; refresh before reconciling')
                if not old or baseline!=old['baseline']: raise ValueError('Preserve original baseline')
                previous=old['current'].decode(); updated=raw.decode()
                if int(re.search(r'^current_day: (\d+)$',updated,re.M)[1])<int(re.search(r'^current_day: (\d+)$',previous,re.M)[1]):
                    raise ValueError('Reconciliation cannot rewind progress')
                old_log=self._progress_log(previous)
                new_log=self._progress_log(updated)
                if old_log and not (new_log==old_log or new_log.startswith(old_log+'\n')):
                    raise ValueError('Reconciliation must preserve prior log')
                db.execute('UPDATE progress SET current=?',(raw,))
                self._set(db,'revision',expected_revision+1)
                return old['hash']
            if old and hashlib.sha256(old['current']).hexdigest()==digest:return old['hash']
            if old:
                raise RevisionConflict('Different progress history; no merge performed. Keep both original files.')
            db.execute('INSERT OR IGNORE INTO progress(hash,original,baseline,current) VALUES (?,?,?,?)',(digest,raw,baseline,raw))
        return digest

    def export_progress(self, path):
        path=Path(path)
        if path.is_symlink() or path.resolve().is_relative_to(self.root):
            raise ValueError('Export must be outside managed data root, without symlink')
        with self._db() as db:
            row=db.execute('SELECT current FROM progress').fetchone()
            if not row: raise ValueError('No imported progress')
            raw=row[0]
        fd,name=tempfile.mkstemp(prefix='.wizard-export-',dir=path.parent)
        try:
            with os.fdopen(fd,'wb') as stream:
                stream.write(raw); stream.flush(); os.fsync(stream.fileno())
            os.replace(name,path)
        finally:
            if os.path.exists(name): os.unlink(name)

    def session_event(self, host, event):
        """Atomically pair submissions with a completed result; never parse transcripts."""
        native=event['session_id'];workspace=workspace_path(event['cwd']);name=event['hook_event_name']
        with self._db() as db:
            if name=='SessionStart':
                token=str(uuid.uuid4())
                db.execute('DELETE FROM drafts WHERE host=? AND native=?',(host,native))
                db.execute('DELETE FROM sessions WHERE host=? AND native=?',(host,native))
                db.execute('INSERT INTO sessions(token,host,native,workspace,model) VALUES (?,?,?,?,?)',
                           (token,host,native,workspace,event.get('model')))
                return {'token':token}
            session=db.execute('SELECT * FROM sessions WHERE host=? AND native=?',(host,native)).fetchone()
            if not session or session['workspace']!=workspace:
                return None
            if 'model' in event:
                db.execute('UPDATE sessions SET model=? WHERE token=?',(event['model'],session['token']))
            if name in ('SessionEnd','Interrupt'):
                db.execute('DELETE FROM drafts WHERE host=? AND native=?',(host,native))
                if name=='SessionEnd': db.execute('DELETE FROM sessions WHERE host=? AND native=?',(host,native))
                return None
            if self._mode(db,workspace) is None or session['lease']>self.clock():
                db.execute('DELETE FROM drafts WHERE host=? AND native=?',(host,native))
                return None
            draft=db.execute('SELECT * FROM drafts WHERE host=? AND native=?',(host,native)).fetchone()
            if name=='UserPromptSubmit':
                prompt=event['prompt']
                # Explicit Wizard requests are controls/learning, never work evidence.
                if re.match(r'^\s*[/\$](?:prompting-wizard:)?pw(?:\s|$)', prompt):
                    db.execute('DELETE FROM drafts WHERE host=? AND native=?',(host,native))
                    return None
                if draft: prompt=draft['prompt']+'\n\n[Additional user submission]\n'+prompt
                # Keep a byte beyond the excerpt limit so the observation retains truncation evidence.
                prompt=prompt.encode()[:16388].decode('utf-8',errors='ignore')
                db.execute('INSERT INTO drafts VALUES (?,?,?,?,?,?,?) ON CONFLICT(host,native) DO UPDATE SET prompt=excluded.prompt,turn_id=excluded.turn_id',
                           (host,native,workspace,draft['id'] if draft else str(uuid.uuid4()),event.get('turn_id'),prompt,self.clock()+TTL))
                return None
            if name!='Stop' or not draft:
                return None
            record=dict(id=draft['id'],host=host,session_id=native,turn_id=draft['turn_id'],workspace=workspace,
                        model_id=event.get('model'),prompt=draft['prompt'],
                        result=event.get('last_assistant_message') or '',context_complete=False,skill=None)
            observation_id=self._save_observation(db,record)
            db.execute('DELETE FROM drafts WHERE host=? AND native=?',(host,native))
            return {'observation_id':observation_id,'mode':self._mode(db,workspace)}
