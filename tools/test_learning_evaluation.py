import copy
import importlib.util
import unittest

CASES=[{'id':'one','input':'Help with a task','expectations':['work-first','optional']}]
RUN={'case_id':'one','surface':'tool-disabled synthetic','model':'test-model','run_date':'2026-10-11',
     'steps':[{'role':'user','content':'Help with a task'},{'role':'assistant','content':'Here is your work.'}],
     'reviewer':'human reviewer','observations':{'work-first':{'assessment':'pass','reason':'Work delivered first'},
                                               'optional':{'assessment':'pass','reason':'No demand to practise'}}}

class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('evaluate_learning'),'Offline evaluator missing')
        import evaluate_learning
        self.evaluate=evaluate_learning.evaluate

    def test_unrun_and_unsupported_cannot_pass(self):
        receipt=self.evaluate(CASES,{'runs':[]})
        self.assertFalse(receipt['all_pass']);self.assertEqual(receipt['unrun'],['one'])
        with self.assertRaises(ValueError):self.evaluate(CASES,{'runs':[],'request_all_pass':True})
        run=copy.deepcopy(RUN);run['observations']['optional']['assessment']='unsupported'
        self.assertFalse(self.evaluate(CASES,{'runs':[run]})['all_pass'])

    def test_reviewed_complete_run_passes_with_explicit_limits(self):
        receipt=self.evaluate(CASES,{'runs':[RUN]})
        self.assertTrue(receipt['all_pass'])
        self.assertIn('does not establish native compatibility',receipt['limits'])

    def test_duplicate_unknown_and_missing_ids_fail(self):
        for cases,doc in [(CASES*2,{'runs':[]}), (CASES,{'runs':[RUN,RUN]}),
                          (CASES,{'runs':[dict(RUN,case_id='other')]}),
                          ([{'input':'x','expectations':['a']}],{'runs':[]})]:
            with self.assertRaises(ValueError):self.evaluate(cases,doc)

    def test_malformed_or_unreviewed_receipts_fail(self):
        for changes in [{'reviewer':''},{'observations':{}},{'run_date':'yesterday'},{'steps':[]},
                        {'observations':{'work-first':{'assessment':'pass','reason':''},'optional':{'assessment':'pass','reason':'ok'}}}]:
            with self.assertRaises(ValueError):self.evaluate(CASES,{'runs':[dict(RUN,**changes)]})

if __name__=='__main__':unittest.main()
