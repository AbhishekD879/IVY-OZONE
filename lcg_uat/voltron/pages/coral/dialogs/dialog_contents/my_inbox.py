from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class CoralMyInbox(ComponentBase):
    _close_button = 'xpath=.//span[contains(@class, "ui-close")]'
    _back_button = 'xpath=.//*[contains(@class, "ui-back")]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we, timeout=1)
