from voltron.pages.shared.components.primitives.selects import SelectBase
from voltron.pages.shared.contents.sports_tab_contents.live import LiveTabContent


class LiveTabContentDesktop(LiveTabContent):
    _dropdown_market_selector = 'xpath=.//*[@data-crlat="marketSelectorModule"]'
    _dropdown_market_selector_type = SelectBase
    _selected_market_name = 'xpath=.//*[@class="option-title"]'
    _selected_market_selector_item = 'xpath=.//*[@data-crlat="selected-item"]| .//*[@data-crlat="dropdown.selectedItem"]'

    @property
    def selected_market_selector_item(self):
        return self._get_webelement_text(selector=self._selected_market_selector_item, timeout=2, context=self._we)

    @property
    def selected_market(self):
        return self._get_webelement_text(selector=self._selected_market_name)
