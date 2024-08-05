import os

from selenium.common.exceptions import WebDriverException

from voltron.utils import mixins
from voltron.utils.get_screenshot import screenshot


class VoltronException(mixins.LoggingMixin, Exception):
    """
    VoltronException for Page Objects (UI components not found, etc)
    """
    def __init__(self, message, *args, **kwargs):

        location = os.environ.get('LOCATION_NAME', 'IDE')
        is_ide = location == 'IDE'

        if not is_ide:
            from voltron.utils.content_manager import ContentManager
            content_manager = ContentManager()
            try:
                content_state = content_manager.get_content_state().__name__
            except AttributeError:
                content_state = r'N\A as browser was not started'
            except (RuntimeError, WebDriverException):
                content_state = 'Cannot detect'
        else:
            content_state = 'Local run'
        message = '{message}\nCurrent content state is: "{content_state}"'.format(message=message, content_state=content_state)

        super(VoltronException, self).__init__('voltron_logger', message, *args, **kwargs)
        if not is_ide:
            self._attach_screenshot()

    @staticmethod
    def _attach_screenshot():
        screenshot()
