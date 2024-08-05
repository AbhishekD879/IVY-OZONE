import itertools
import time

from crlat_ws_clients.utils.loggers import domain_logger

logger = domain_logger


class DomainEvent:
    """A base class for all events in this domain.

    DomainEvents are value objects and all attributes are specified as keyword
    arguments at construction time. There is always a timestamp attribute which
    gives the event creation time in UTC, unless specified.  Events are
    equality comparable.
    """

    def __init__(self, event_time=None, **kwargs):
        self.__dict__['event_time'] = time.time() if event_time is None else event_time
        self.__dict__.update(kwargs)

    def __setattr__(self, key, value):
        if hasattr(self, key):
            raise AttributeError("{} attributes can be added but not modified."
                                 "Attribute {!r} already exists with value {!r}".format(self.__class__.__name__,
                                                                                        key,
                                                                                        getattr(self, key)))
        self.__dict__[key] = value

    def __eq__(self, rhs):
        if type(self) is not type(rhs):
            return NotImplemented
        return self.__dict__ == rhs.__dict__

    def __ne__(self, rhs):
        return not (self == rhs)

    def __hash__(self):
        return hash(tuple(itertools.chain(self.__dict__.items(),
                                          [type(self)])))

    def __repr__(self):
        args = "(" + ', '.join("{0}={1!r}".format(*item) for item in self.__dict__.items())
        args = args if len(args) <= 100 else args[:97] + '...'
        return self.__class__.__qualname__ + args + ')'
