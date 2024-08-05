import time

from native_ios.utils import mixins

_current_action = 'MainThread'


class ActionItem(object):
    def __init__(self, name, action_func, timeout, expected_result):
        self.name = name
        self.action = action_func
        self.expected_result = expected_result
        self.end_time = time.time() + timeout


class DialogAction(mixins.LoggingMixin,):
    def __init__(self):
        super(DialogAction, self).__init__()
        self._actions = []

    def push(self, action):
        self._logger.debug('*** Added action "%s"' % action.name)
        self._actions.append(action)

    def perform_actions(self):
        global _current_action
        if _current_action == 'MainThread':
            i = 0
            while i < len(self._actions):
                _current_action = self._actions[i].name
                self._logger.debug('*** Executing action "%s"' % _current_action)
                if self._actions[i].end_time < time.time():
                    self._actions.pop(i)
                    self._logger.warning('*** "%s" action TIMEOUT!' % _current_action)
                elif self._actions[i].action() == self._actions[i].expected_result:
                    self._actions.pop(i)
                    self._logger.debug('*** "%s" action DONE!' % _current_action)
                else:
                    i += 1
            _current_action = 'MainThread'
