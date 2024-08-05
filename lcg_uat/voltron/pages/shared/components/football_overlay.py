from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class FootballOverlay(ComponentBase):
    _close_btn = 'xpath=.//*[@data-crlat="closeBtn"]'
    _football_tutorial = 'xpath=.//*[contains(@class,"arr-div")]'
    _football_close_button = 'xpath=.//*[@class="btn btn-style1"]'

    @property
    def close_btn(self):
        return ButtonBase(selector=self._close_btn, timeout=5, context=self._we)

    @property
    def football_tutorial(self):
        return self._find_elements_by_selector(selector=self._football_tutorial)

    @property
    def close_football_tutorial(self):
        return ButtonBase(selector=self._football_close_button)
