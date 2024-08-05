from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class CoralRewardMoney(ComponentBase):
    _close_button = 'xpath=.//*[contains(@class, "ui-close")]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)
