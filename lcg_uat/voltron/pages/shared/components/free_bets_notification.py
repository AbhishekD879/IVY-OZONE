from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class FreeBetsNotification(ComponentBase):
    _close_button = 'xpath=.//*[@data-crlat="closeIcon"]'
    _text = 'xpath=.//*[@data-crlat="text"]'

    @property
    def text(self):
        return self._get_webelement_text(selector=self._text)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we, timeout=3)
