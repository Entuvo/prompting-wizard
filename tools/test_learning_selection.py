import copy
import datetime
import unittest
import uuid
from test_learning_card import BASE, EVENT, TODAY, card
import learning


def event(n=1, **changes):
    return dict(EVENT, **dict({'id': str(uuid.UUID(int=n)), 'task_id': 'task-'+str(n),
                              'assistance': 'none'}, **changes))

class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(getattr(learning, 'summarize', None)), 'Evidence stages missing')

    def state(self, *events, **kwargs):
        return learning.summarize(card(*events), kwargs.get('today', TODAY))['noun']

    def test_all_stages_and_non_evidence(self):
        for changes, expected in [({},'demonstrated-independently'),
            ({'activity':'introduction','assistance':'example'},'introduced'),
            ({'assistance':'hint'},'practised-with-help'),
            ({'assistance':'unknown'},'practised-assistance-unknown'),
            ({'context_quality':'partial'},'unknown'), ({'outcome':'uncertain'},'unknown'),
            ({'outcome':'not-applicable'},'unknown'), ({'outcome':'not-yet'},'unknown')]:
            with self.subTest(changes=changes): self.assertEqual(self.state(event(**changes))['stage'], expected)
        self.assertEqual(self.state()['stage'], 'unknown')

    def test_assistance_cannot_be_laundered_by_retry(self):
        helped = event(1, assistance='hint')
        retry = event(2, task_id=helped['task_id'], date='2026-10-02')
        self.assertEqual(self.state(helped,retry)['stage'],'practised-with-help')
        self.assertIsNone(self.state(helped,retry)['last_independent_date'])
        unknown = event(1, assistance='unknown')
        self.assertEqual(self.state(unknown,retry)['stage'],'practised-assistance-unknown')

    def test_retry_inherits_help_from_introduction_and_failed_attempt(self):
        for changes, expected in [({'assistance':'hint','outcome':'not-yet'},'practised-with-help'),
                                  ({'activity':'introduction','assistance':'example'},'practised-with-help'),
                                  ({'activity':'introduction','assistance':'none'},'practised-with-help'),
                                  ({'assistance':'unknown','outcome':'not-yet'},'practised-assistance-unknown')]:
            earlier=event(1,**changes)
            retry=event(2,task_id=earlier['task_id'],date='2026-10-02')
            with self.subTest(changes=changes):
                self.assertEqual(self.state(earlier,retry)['stage'],expected)
                self.assertEqual(learning.select_next(card(earlier,retry),['verb','noun'],
                                                      'meeting preparation',TODAY)['activity'],'independent-practice')

    def test_transfer_retention_and_same_task(self):
        one = event(1,date='2026-09-01')
        two = event(2,date='2026-09-02', task_family='lesson planning')
        self.assertEqual(self.state(one,two)['stage'],'demonstrated-another-context')
        self.assertEqual(self.state(one,dict(two,task_id=one['task_id']))['stage'],'demonstrated-independently')
        self.assertEqual(self.state(one,dict(two,task_family=one['task_family']))['stage'],'demonstrated-independently')
        self.assertEqual(self.state(one,two,event(3,date='2026-09-08'))['stage'],'demonstrated-another-context')
        self.assertEqual(self.state(one,two,event(3,date='2026-09-09'))['stage'],'retained-later')
        self.assertEqual(self.state(one,two,event(3,date='2026-09-09',task_id=one['task_id']))['stage'],'demonstrated-another-context')

    def test_review_uses_dates_not_id_or_merge_direction(self):
        good = event(1); bad = event(2,outcome='not-yet')
        a,b=card(good),card(bad)
        for merged in [learning.merge_cards(a,b,TODAY), learning.merge_cards(b,a,TODAY)]:
            state=learning.summarize(merged,TODAY)['noun']
            self.assertTrue(state['needs_review'])
            self.assertEqual(state['stage'],'demonstrated-independently')
            self.assertEqual(learning.select_next(merged,['verb','noun'],'meeting preparation',TODAY)['skill'],'noun')
        self.assertFalse(self.state(good,bad,event(3,date='2026-10-02'))['needs_review'])
        self.assertTrue(self.state(good,bad,event(3,date='2026-10-02',context_quality='partial'))['needs_review'])

    def test_repeated_task_does_not_refresh_retention_clock(self):
        first=event(1,date='2026-09-01')
        retry=event(2,date='2026-10-11',task_id=first['task_id'])
        self.assertEqual(self.state(first,retry)['last_independent_date'],'2026-09-01')

    def test_priority_relevance_and_no_forced_lesson(self):
        self.assertIsNone(learning.select_next(BASE,[],'meeting preparation',TODAY))
        self.assertEqual(learning.select_next(BASE,['verb','noun'],'meeting preparation',TODAY)['skill'],'verb')
        c=card(event(1,assistance='hint'))
        self.assertEqual(learning.select_next(c,['verb','noun'],'meeting preparation',TODAY)['skill'],'noun')
        recent=card(event(1,date='2026-10-10'))
        self.assertIsNone(learning.select_next(recent,['noun'],'meeting preparation',TODAY))
        self.assertEqual(learning.select_next(recent,['noun'],'lesson planning',TODAY)['activity'],'transfer')
        self.assertEqual(learning.select_next(card(event(1)),['verb'],'meeting preparation',TODAY)['skill'],'verb')
        result=learning.select_next(card(event(1)),['verb','noun'],'meeting preparation',TODAY)
        self.assertEqual(result['activity'],'revisit')
        self.assertEqual(result['evidence_ids'],[event(1)['id']])
        self.assertTrue(result['reason'])

    def test_transferred_and_retained_due_boundary(self):
        for events in [(event(1,date='2026-09-01'),event(2,date='2026-09-02',task_family='lesson planning')),
                       (event(1,date='2026-08-01'),event(2,date='2026-08-02',task_family='lesson planning'),event(3,date='2026-09-02'))]:
            c=card(*events)
            self.assertIsNone(learning.select_next(c,['noun'],'new family',datetime.date(2026,9,8)))
            self.assertEqual(learning.select_next(c,['noun'],'new family',datetime.date(2026,9,9))['activity'],'revisit')

    def test_invalid_relevance_is_rejected(self):
        for skills in [['bad'],['noun','noun'],'noun',[{}]]:
            with self.assertRaises(ValueError): learning.select_next(BASE,skills,'meeting preparation',TODAY)
        with self.assertRaises(ValueError): learning.select_next(BASE,['noun'],'',TODAY)

if __name__ == '__main__': unittest.main()
