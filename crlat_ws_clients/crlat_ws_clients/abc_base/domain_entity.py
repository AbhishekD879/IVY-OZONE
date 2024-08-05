import abc
from functools import singledispatch


class AbcDomainEntity(abc.ABC):

    _subscribe_events = []

    def __init__(self, event, *args, **kwargs):
        self._app = event.application
        self._version = 0
        self._entity_state = {}
        # logger.debug('Subscribing: %s' % type(self).__qualname__)
        self._app.subscribe(self._subscribe_events, self.apply_event)

    def _increment_version(self):
        self._version += 1
        return self._version

    def fire_event(self, event_class, *event_args, **event_kwargs):
        event = event_class(
            event_source=self.__class__.__qualname__,
            *event_args,
            **event_kwargs
        )
        self._app.publish(event)

    def apply_event(self, event):
        raise NotImplementedError(
            'apply_event method not implemented in %s' %
            type(self).__qualname__
        )


def mutate(event, obj):
    return _handler(event, obj)

@singledispatch
def _handler(event, entity):
    raise NotImplementedError(
        'No Handler implemention in "%s" for "%s"' % (
            entity.__class__.__qualname__,
            event.__class__.__qualname__,
        )
    )
