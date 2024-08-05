from crlat_ws_clients.utils.loggers import app_logger

logger = app_logger


class BaseApplication:
    def __init__(self, *args, **kwargs):
        self._event_handlers = {}

    def subscribe(self, event_classes, subscriber):
        """Subscribe to events.

        Args:
            event_classes: A list of event classes to subscribe.
            subscriber: A unary callable function which handles the passed event.
        """
        logger.debug('Subscribed matcher: %s to [%s]' %
                     (subscriber.__qualname__, ', '.join([ec.__qualname__ for ec in event_classes])))
        for event_class in event_classes:
            if event_class not in self._event_handlers.keys():
                self._event_handlers[event_class] = set()
            self._event_handlers[event_class].add(subscriber)

    def unsubscribe(self, event_classes, subscriber):
        """Unsubscribe from events.

        Args:
            event_classes: A list of event classes to subscribe.
            subscriber: The subscriber to disconnect.
        """
        for event_class in event_classes:
            if event_class in self._event_handlers.keys():
                self._event_handlers[event_class].discard(subscriber)

    def unsubscribe_all(self, subscriber):
        event_class_for_removal = []
        for event_class, event_handlers in self._event_handlers.items():
            event_handlers.discard(subscriber)
            if len(event_handlers) == 0:
                event_class_for_removal.append(event_class)

        for event_class in event_class_for_removal:
            del self._event_handlers[event_class]

    def publish(self, event):
        """Send an event to all subscribers.

        Each subscriber will receive each event only once, even if it has been subscribed multiple
        times, possibly with different predicates.

        Args:
            event: The object to be tested against by all registered predicate functions
            and sent to all matching subscribers.
        """

        matching_handlers = self._event_handlers.get(type(event), set())
        logger.debug(
            'Publishing "%s" to [%s]' %
            (type(event).__qualname__, ', '.join([h.__qualname__ for h in matching_handlers]))
        )
        for handler in matching_handlers:
            handler(event)
