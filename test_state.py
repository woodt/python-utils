#!/usr/bin/env python
# encoding: utf-8
"""
test_state.py

Created by Tom Wood on 2009-03-18.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import unittest
from state import Machine

class Request(object):
    m = Machine('pending')
    
    def notify_change(self, old, new):
        self.changes.append((old, new))
    
    m.add_state(['assigned', 'started', 'completed', 'rejected', 'cancelled'],
                notify_change)
    m.add_transition('pending', ['assigned', 'cancelled'])
    m.add_transition('assigned', 'started')
    m.add_transition('started', 'completed')
    
    def set_state(self, new):
        return self._state.set_state(new)
    
    def get_state(self):
        return self._state.state()
        
    state = property(get_state, set_state)
    
    def __init__(self):
        self._state = Request.m.new_state(self)
        self.changes = []

class TestStateMachine(unittest.TestCase):
    def test_workflow(self):
        req = Request()
        req.state = 'assigned'
        self.assertEquals(req.state, 'assigned')
        # can't be completed
        req.state = 'completed'
        self.assertEquals(req.state, 'assigned')
        req.state = 'started'
        self.assertEquals(req.state, 'started')
        req.state = 'completed'
        self.assertEquals(req.state, 'completed')        
        self.assertEquals(req.changes, [('pending', 'assigned'),
                                        ('assigned', 'started'),
                                        ('started', 'completed')])

if __name__ == '__main__':
    unittest.main()


