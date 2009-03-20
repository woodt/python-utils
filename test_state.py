#!/usr/bin/env python
# encoding: utf-8
"""
test_state.py

Created by Tom Wood on 2009-03-18.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

from state import Machine

class Request(object):
    m = Machine('pending')
    
    def notify_change(self, old, new):
         print "%s: %s -> %s" % (self, old, new)
    
    m.add_state(['assigned', 'started', 'completed', 'rejected', 'cancelled'], notify_change)
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
   
def main():
    req = Request()
    req.state = 'assigned'
    req.state = 'completed'
    req.state = 'started'
    
if __name__ == '__main__':
	main()

