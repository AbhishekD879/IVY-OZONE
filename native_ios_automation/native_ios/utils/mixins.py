import logging


class LoggingMixin(object):
    def __init__(self, logger_name='native_ios_logger', *args, **kwargs):
        super(LoggingMixin, self).__init__(*args, **kwargs)
        self._logger = logging.getLogger('native_ios_logger')

    @property
    def logger(self):
        return self._logger
