from time import sleep

from selenium.common.exceptions import NoSuchElementException

from voltron.pages.shared.components.market_selector_drop_down import MarketSelectorDropDown
from voltron.pages.shared.components.market_selector_drop_down import MarketSelectorOption
from voltron.pages.shared.components.primitives.selects import SelectBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import scroll_to_center_of_element
from voltron.utils.waiters import wait_for_result


class MarketSelectorOptionDesktop(MarketSelectorOption):
    _name = 'xpath=.//*[@data-crlat="dropdown.menuTitle"]'

    @property
    def name(self):
        name_we = self._find_element_by_selector(selector=self._name, timeout=1)
        if not name_we:
            raise VoltronException('Market selector name web element not found on page')
        return name_we.get_attribute('innerHTML').replace('&amp;', '&')

    def scroll_to_we(self, web_element=None):
        if web_element is None:
            self._logger.debug(
                f'*** Nothing passed to scroll function, scrolling to current web element "{self.__class__.__name__}"')
            web_element = self._we
        scroll_to_center_of_element(web_element)


class MarketSelectorDesktopDropDown(MarketSelectorDropDown):
    _item = 'xpath=.//*[@data-crlat="dropdown.menuItem"]'
    _list_item_type = MarketSelectorOptionDesktop
    _dropdown_market_selector = 'xpath=.//*[@data-crlat="dropdown.label"]'
    _selected_market_selector_item = 'xpath=.//*[@data-crlat="dropdown.selectedItem"]'

    def select_value(self, value):
        self.items_as_ordered_dict[value].click()

    @property
    def selected_item(self):
        try:
            return SelectBase(web_element=self._we).selected_item
        except (NoSuchElementException, VoltronException):
            raise VoltronException(f'No selected market selector item found. '
                                   f'All items are: {self.items_as_ordered_dict}')

    @property
    def value(self):
        return self.selected_item

    @value.setter
    def value(self, value):
        self.click()
        sleep(0.3)  # make sure drop-down is opened
        items = self.items_as_ordered_dict
        result = wait_for_result(lambda: value in items,
                                 name=f'Value "{value}" to appear in "{items.keys()}"', timeout=1)
        if result:
            value = items.get(value)
            value.click()
        else:
            raise VoltronException(f'"{value}" market not found. Available in dropdown markets: {list(items.keys())}')
