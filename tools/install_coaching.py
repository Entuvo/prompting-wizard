#!/usr/bin/env python3
"""Install optional local hooks into an explicitly selected host configuration."""
import argparse
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import sys
import tempfile

from course_files import COURSE_FILES

SOURCE=Path(__file__).resolve().parents[1]/'prompting-wizard'
EVENTS=('SessionStart','UserPromptSubmit','Stop','SessionEnd')


def read_file(path):
    if path.is_symlink():raise ValueError('Symlink configuration or receipt rejected')
    if path.exists() and not path.is_file():raise ValueError('Expected regular file')
    return path.read_bytes() if path.exists() else None


def atomic_write(path,data,expected):
    """Detect changed preimages; rollback callers also use this check."""
    if read_file(path)!=expected:raise ValueError('Concurrent edit detected; nothing overwritten')
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.wizard-config-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as stream:
            stream.write(data);stream.flush();os.fsync(stream.fileno())
        if read_file(path)!=expected:raise ValueError('Concurrent edit detected; nothing overwritten')
        os.replace(name,path)
        if read_file(path)!=data:raise ValueError('Configuration changed during verification')
    finally:
        if os.path.exists(name):os.unlink(name)


def decode(raw):
    value=json.loads(raw) if raw is not None else {}
    if not isinstance(value,dict):raise ValueError('Configuration must be an object')
    hooks=value.get('hooks',{})
    if not isinstance(hooks,dict) or any(not isinstance(items,list) for items in hooks.values()):
        raise ValueError('Malformed hook collection')
    return value


def apply(host,root,config,action):
    if host not in ('claude','codex') or action not in ('dry-run','install','remove'):
        raise ValueError('Unknown host or action')
    root,config=Path(root),Path(config)
    if not root.is_absolute() or not config.is_absolute() or root.is_symlink():
        raise ValueError('Absolute paths without symlink root required')
    if not Path(sys.executable).is_file():raise ValueError('Python interpreter unavailable')
    before=read_file(config);original=decode(before)
    digest=hashlib.sha256()
    for name in COURSE_FILES:
        source=SOURCE/name
        if not source.is_file() or source.is_symlink():raise ValueError('Canonical runtime incomplete or linked')
        digest.update(name.encode()+b'\0'+source.read_bytes())
    runtime=root/'runtime'/digest.hexdigest()[:16]
    command=shlex.join([sys.executable,str(runtime/'scripts/wizard.py'),'hook','--host',host,'--root',str(root)])
    events=EVENTS+(('Interrupt',) if host=='codex' else ())
    owned={event:{'hooks':[{'type':'command','command':command,'timeout':3 if event=='Interrupt' else 10}]} for event in events}
    review={'host':host,'config':str(config),'data_root':str(root),'runtime':str(runtime),
            'capture':'Only explicitly enabled workspaces; none enabled by installer',
            'retention':'30-day pending excerpts; reviewed history until deletion',
            'sharing':'Same-computer profile; lessons can send selected excerpts to the current provider',
            'quota':'After-result coaching uses additional host inference',
            'trust':'Review exact hooks through normal host controls; installation does not grant trust',
            'permissions':'Continuation needs narrowly scoped access to this runtime and data root'}
    if action=='dry-run':return {'review':review,'changes':owned}
    if os.name!='posix':raise ValueError('This installer currently requires POSIX ownership and locking')
    root.mkdir(mode=0o700,parents=True,exist_ok=True)
    info=root.lstat()
    if info.st_uid!=os.getuid() or info.st_mode & 0o077:raise ValueError('Data root must be owner-only')
    lock=root/'install.lock'
    fd=os.open(lock,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'a+') as stream:
        fcntl.flock(stream,fcntl.LOCK_EX)
        receipt=root/(host+'-'+hashlib.sha256(str(config).encode()).hexdigest()[:16]+'.receipt.json')
        if action=='install':
            for other in root.glob(host+'-*.receipt.json'):
                if other!=receipt:raise ValueError('This host already uses another configuration for this profile')
        receipt_raw=read_file(receipt)
        previous=json.loads(receipt_raw) if receipt_raw else None
        # Re-read after locking; never overwrite a pre-lock edit.
        if read_file(config)!=before:raise ValueError('Concurrent configuration edit detected')
        updated=copy.deepcopy(original);hooks=updated.setdefault('hooks',{})
        if previous:
            if previous.get('config')!=str(config) or previous.get('host')!=host or not isinstance(previous.get('owned'),dict):
                raise ValueError('Invalid ownership receipt')
            for event,item in previous['owned'].items():
                if hooks.get(event,[]).count(item)!=1:
                    raise ValueError('Owned hook was edited or removed; resolve conflict manually')
            for event,item in previous['owned'].items():
                hooks[event].remove(item)
                if not hooks[event] and event not in previous['original_events']:del hooks[event]
        elif action=='remove':
            return {'ok':True,'status':'not-installed'}
        if action=='install':
            for event,item in owned.items():
                # An unowned exact registration must never be duplicated or adopted silently.
                if item in hooks.get(event,[]):raise ValueError('Unowned duplicate hook; resolve before install')
                hooks.setdefault(event,[]).append(item)
            if runtime.parent.is_symlink():raise ValueError('Linked runtime directory rejected')
            runtime.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
            if runtime.is_symlink():raise ValueError('Linked runtime rejected')
            if runtime.exists():
                for name in COURSE_FILES:
                    target=runtime/name
                    if target.is_symlink() or not target.is_file() or target.read_bytes()!=(SOURCE/name).read_bytes():
                        raise ValueError('Installed runtime changed; not overwritten')
            else:
                stage=Path(tempfile.mkdtemp(prefix='.wizard-runtime-',dir=runtime.parent))
                try:
                    for name in COURSE_FILES:
                        target=stage/name;target.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
                        shutil.copyfile(SOURCE/name,target);target.chmod(0o600)
                    os.rename(stage,runtime)
                finally:
                    if stage.exists():shutil.rmtree(stage)
            state={'host':host,'config':str(config),'owned':owned,
                   'original_events':previous['original_events'] if previous else list(original.get('hooks',{})),
                   'had_hooks':previous['had_hooks'] if previous else 'hooks' in original}
        else:
            if not hooks and not previous['had_hooks']:updated.pop('hooks')
            state=None
        after=(json.dumps(updated,indent=2)+'\n').encode()
        # Backup configuration only, never learner database content.
        backup=root/('config-'+str(os.getpid())+'.backup')
        atomic_write(backup,before or b'',None)
        cleanup_backup=False
        try:
            atomic_write(config,after,before)
            if state is not None:
                atomic_write(receipt,(json.dumps(state,indent=2)+'\n').encode(),receipt_raw)
            else:
                if read_file(receipt)!=receipt_raw:raise ValueError('Receipt changed concurrently')
                receipt.unlink()
            cleanup_backup=True
        except BaseException:
            # Preserve any intervening manual edit instead of overwriting it during rollback.
            if read_file(config)==after:
                if before is None:config.unlink()
                else:atomic_write(config,before,after)
                cleanup_backup=True
            raise
        finally:
            if cleanup_backup:backup.unlink(missing_ok=True)
        return {'ok':True,'status':'installed-needs-host-trust-and-workspace-setup' if state else 'removed',
                'review':review}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host',required=True,choices=['claude','codex'])
    parser.add_argument('--root',required=True,type=Path);parser.add_argument('--config',required=True,type=Path)
    group=parser.add_mutually_exclusive_group(required=True)
    for action in ('dry-run','install','remove'):group.add_argument('--'+action,action='store_true')
    args=parser.parse_args()
    try:
        result=apply(args.host,args.root,args.config,'dry-run' if args.dry_run else 'remove' if args.remove else 'install')
        print(json.dumps(result,indent=2));return 0
    except (ValueError,OSError):
        print('Prompting Wizard install failed: check paths, ownership, configuration and receipt conflicts. No success recorded.',file=sys.stderr)
        return 1


if __name__=='__main__':raise SystemExit(main())
