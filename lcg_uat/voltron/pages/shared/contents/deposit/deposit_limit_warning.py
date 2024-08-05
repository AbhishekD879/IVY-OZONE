from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.deposit.deposit_base import GVCDepositContent


class GVCDepositLimitWarning(GVCDepositContent):
    _url_pattern = '^http[s]?:\/\/.+\/deposit?'
    _header = 'xpath=.//*[@class="main-header"]'
    _warning_message_title = 'xpath=.//*[@class="message-text"]/h4'
    _warning_message = 'xpath=.//*[@class="message-text"]'
    _deposit_now_button = 'xpath=.//*[@class="btn active-btn" and @type="submit"]'

    @property
    def header(self):
        return ComponentBase(selector=self._header, context=self._we)

    @property
    def warning_message_title(self):
        return self._wait_for_not_empty_web_element_text(selector=self._warning_message_title, context=self._we, timeout=2)

    @property
    def warning_message(self):
        message = self._wait_for_not_empty_web_element_text(selector=self._warning_message, context=self._we, timeout=3)
        return '\n'.join(message.split('\n')[1:])

    @property
    def deposit_now_button(self):
        return ButtonBase(selector=self._deposit_now_button, context=self._we)
