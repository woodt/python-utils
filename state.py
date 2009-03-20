class TransitionDict(dict):
    def __missing__(self, key):
        return False

class MachineState(object):
    def __init__(self, machine, target, initial_state):
        self._machine = machine
        self._target = target
        self._state = initial_state

    def state(self):
        return self._state

    def set_state(self, to_s):
        if self._machine.can_transit(self._state, to_s):
            if self._machine._states[to_s]:
                self._machine._states[to_s](self._target, self._state, to_s)
            self._state = to_s
            return True
        else:
            return False

class Machine(object):
    def __init__(self, initial_state):
        self._transitions = TransitionDict()
        self._initial_state = initial_state
        self._states = {}
        self._states[initial_state] = None
        
    def add_state(self, names, notify = None):
        if isinstance(names, basestring):
            names = [names]
        for name in names:
            self._states[name] = notify
         
    def add_transition(self, from_s, to_s, guard = True):
        if isinstance(to_s, basestring):
            to_s = [to_s]
        
        if isinstance(from_s, basestring):
            from_s = [from_s]
        
        self.validate_states(from_s)
        self.validate_states(to_s)

        for f_s in from_s:
            for t_s in to_s:
                self._transitions[(f_s, t_s)] = guard
                
    def validate_states(self, states):
        for state in states:
            if state not in self._states:
                raise Exception("Unknown state %s" % state)
                
    def can_transit(self, from_s, to_s):
        guard = self._transitions[(from_s, to_s)]
        if guard:
            if guard is True:
                return True
            else:
                return guard(self)
        else:
            return False
        

    def states(self):
        return self._states.keys()
        
    def new_state(self, target):
        return MachineState(self, target, self._initial_state) 
    
if __name__ == "__main__":
    
    def state_notify(s, old, new):
        print "%s -> %s" % (old, new)
        
    m = Machine('pending')
    m.add_state('pending', state_notify)
    m.add_state('matched', state_notify)
    m.add_state('cancelled', state_notify)
    m.add_state('completed', state_notify)
    
    m.add_transition('pending', ['matched', 'cancelled'])
    m.add_transition('matched', 'completed')
    m.add_transition(['completed','cancelled'], 'pending')
 
    print m
    
    print m.states()
    
    print m.can_transit('pending', 'matched')
    print m.can_transit('pending', 'completed')
    
    s = m.new_state(m)
    s.set_state('matched')
    s.set_state('completed')
    s.set_state('pending')

    
    
    