import logging


class LoggingMixin(object):
    def __init__(self, logger_name='voltron_logger', *args, **kwargs):
        super(LoggingMixin, self).__init__(*args, **kwargs)
        self._logger = logging.getLogger('voltron_logger')

    @property
    def logger(self):
        return self._logger
