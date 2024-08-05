from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class PolicyBanner(ComponentBase):
    _close_icon = 'xpath=.//*[@data-crlat="buttonClose"]'

    @property
    def close_icon(self):
        return ButtonBase(selector=self._close_icon, context=self._we)
