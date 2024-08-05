from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class BottomToast(ComponentBase):
    _close_button = 'xpath=.//*[contains(@class, "rtms-toast__close")]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, timeout=2)
