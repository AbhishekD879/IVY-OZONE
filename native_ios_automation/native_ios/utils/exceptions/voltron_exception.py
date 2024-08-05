import os


from native_ios.utils import mixins
from native_ios.utils.get_screenshot import screenshot


class VoltronException(mixins.LoggingMixin, Exception):
    """
    VoltronException for Page Objects (UI components not found, etc)
    """
    def __init__(self, message, *args, **kwargs):

        location = os.environ.get('LOCATION_NAME', 'IDE')
        is_ide = location == 'IDE'

        super(VoltronException, self).__init__('native_ios_logger', message, *args, **kwargs)
        if not is_ide:
            self._attach_screenshot()

    @staticmethod
    def _attach_screenshot():
        screenshot()
