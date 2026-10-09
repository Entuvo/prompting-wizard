import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
try:
    import install_coaching
except ImportError:
    install_coaching=None

class IntegrationInstallerTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(install_coaching,'Local integration installer missing')
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name)
        self.root=self.base/'learner $(not-executed) with spaces'
        self.config=self.base/'hooks.json'
        self.original={'unrelated':{'keep':True},'hooks':{'Stop':[{'hooks':[{'type':'command','command':'echo existing'}]}]}}
        self.config.write_text(json.dumps(self.original))

    def apply(self,action='install',host='codex'):
        return install_coaching.apply(host,self.root,self.config,action)

    def test_dry_run_has_no_mutations(self):
        before=self.config.read_bytes()
        result=self.apply('dry-run')
        self.assertFalse(self.root.exists())
        self.assertEqual(self.config.read_bytes(),before)
        self.assertIn('review',result)

    def test_install_is_idempotent_and_remove_preserves_other_hooks(self):
        for host in ('claude','codex'):
            self.apply(host=host);first=json.loads(self.config.read_text())
            self.apply(host=host);self.assertEqual(json.loads(self.config.read_text()),first)
            self.apply('remove',host=host)
            self.assertEqual(json.loads(self.config.read_text()),self.original)
        self.assertFalse((self.base/'not-executed').exists())

    def test_manual_edit_conflicts_without_mutation(self):
        self.apply();config=json.loads(self.config.read_text())
        config['hooks']['Stop'][-1]['hooks'][0]['command']+=' --custom'
        self.config.write_text(json.dumps(config));before=self.config.read_bytes()
        with self.assertRaises(ValueError):self.apply('remove')
        self.assertEqual(self.config.read_bytes(),before)

    def test_bad_config_and_symlink_rejected(self):
        self.config.write_text('not JSON')
        with self.assertRaises(ValueError):self.apply()
        self.assertFalse(self.root.exists())
        self.config.unlink();target=self.base/'target';target.write_text('{}');self.config.symlink_to(target)
        with self.assertRaises(ValueError):self.apply()
        self.assertEqual(target.read_text(),'{}')

    def test_runtime_copy_failure_does_not_modify_config(self):
        before=self.config.read_bytes()
        with patch.object(install_coaching.shutil,'copyfile',side_effect=OSError('disk full')):
            with self.assertRaises(OSError):self.apply()
        self.assertEqual(self.config.read_bytes(),before)

    def test_receipt_write_failure_rolls_back_unchanged_config(self):
        before=self.config.read_bytes();real=install_coaching.atomic_write
        def write(path,data,expected):
            if path.name.endswith('.receipt.json'):raise OSError('disk full')
            return real(path,data,expected)
        with patch.object(install_coaching,'atomic_write',side_effect=write):
            with self.assertRaises(OSError):self.apply()
        self.assertEqual(self.config.read_bytes(),before)

    def test_failed_rollback_retains_recoverable_config_backup(self):
        before=self.config.read_bytes();real=install_coaching.atomic_write;written=False
        def write(path,data,expected):
            nonlocal written
            if path.name.endswith('.receipt.json'):raise OSError('receipt failure')
            if path==self.config:
                if written:raise OSError('rollback failure')
                written=True
            return real(path,data,expected)
        with patch.object(install_coaching,'atomic_write',side_effect=write):
            with self.assertRaises(OSError):self.apply()
        backups=list(self.root.glob('config-*.backup'))
        self.assertEqual(len(backups),1)
        self.assertEqual(backups[0].read_bytes(),before)

    def test_concurrent_edit_during_failed_receipt_is_preserved(self):
        real=install_coaching.atomic_write
        def write(path,data,expected):
            if path.name.endswith('.receipt.json'):
                self.config.write_text('{"manual":"keep"}')
                raise OSError('disk full')
            return real(path,data,expected)
        with patch.object(install_coaching,'atomic_write',side_effect=write):
            with self.assertRaises(OSError):self.apply()
        self.assertEqual(json.loads(self.config.read_text()),{'manual':'keep'})

    def test_second_registration_for_same_host_profile_is_rejected(self):
        self.apply();other=self.base/'another-hooks.json';other.write_text('{}')
        with self.assertRaises(ValueError):install_coaching.apply('codex',self.root,other,'install')
        self.assertEqual(other.read_text(),'{}')

    def test_linked_runtime_directory_is_rejected(self):
        self.root.mkdir(mode=0o700);target=self.base/'elsewhere';target.mkdir()
        (self.root/'runtime').symlink_to(target,target_is_directory=True)
        before=self.config.read_bytes()
        with self.assertRaises(ValueError):self.apply()
        self.assertEqual(self.config.read_bytes(),before)
        self.assertEqual(list(target.iterdir()),[])

    def test_missing_python_fails_before_config_changes(self):
        before=self.config.read_bytes()
        with patch.object(install_coaching.sys,'executable',str(self.base/'missing-python')):
            with self.assertRaises(ValueError):self.apply()
        self.assertEqual(self.config.read_bytes(),before)

if __name__=='__main__':unittest.main()
