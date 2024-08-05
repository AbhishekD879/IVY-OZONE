from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class Withdraw(ComponentBase):
    _url_pattern = r'^http[s]?:\/\/.+\/cashout'
    _title = 'xpath=.//h1[contains(@class,"label-specific-header")]'
    _close_button = 'xpath=.//a[contains(@class,"close-button")]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, timeout=0.5)

    @property
    def withdrawal_title(self):
        return self._find_element_by_selector(selector=self._title, timeout=0.5)
