"""
Tests that the event dispatcher works as expected.
"""
import os
import sys
import unittest

# Ensure we can import smallwm
sys.path.append(os.path.join(*os.path.split(sys.path[0])[:-1]))

import smallwm.events

EVENT = 1
VALUE1 = 42
VALUE2 = 84
class SimpleDispatcher(smallwm.events.Dispatch):
    """
    Dispatches on an event, which is just the number 1.
    """
    def get_next_event(self):
        """
        Returns 1, [42, 84]
        """
        return EVENT, [VALUE1, VALUE2]

class TestDispatcher(unittest.TestCase):
    """
    Tests the functionality of the dispatcher:

     - Registration
     - Unregistration
     - Termination
    """
    def test_register(self):
        """
        Makes sure that a dispatcher _doesn't_ call an event before registration,
        but _does_ call it after registration.
        """
        handler_called = False
        handler_value = None
        def handler(x, y):
            nonlocal handler_called, handler_value
            handler_called = True
            handler_value = x, y

        dispatch = SimpleDispatcher()
        dispatch.step()

        self.assertFalse(handler_called)
        
        dispatch.register(EVENT, handler)
        dispatch.step()

        self.assertTrue(handler_called)
        self.assertEqual(handler_value, (VALUE1, VALUE2))

    def test_unregister(self):
        """
        Makes sure that a dispatcher's unregister function prevents a callback
        from being called.
        """
        handler_called = False
        handler_value = None
        def handler(x, y):
            nonlocal handler_called, handler_value
            handler_called = True
            handler_value = x, y

        dispatch = SimpleDispatcher()
        dispatch.register(EVENT, handler)
        dispatch.step()

        self.assertTrue(handler_called)
        self.assertEqual(handler_value, (VALUE1, VALUE2))
        handler_called = False
        handler_value = None

        dispatch.unregister(EVENT, handler)
        dispatch.step()

        self.assertFalse(handler_called)

    def test_terminate(self):
        dispatch = SimpleDispatcher()
        def handler(x, y):
            dispatch.terminate()

        dispatch = SimpleDispatcher()
        dispatch.register(EVENT, handler)
        dispatch.run()

if __name__ == '__main__':
    unittest.main()
