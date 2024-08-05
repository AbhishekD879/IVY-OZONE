from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from voltron.utils.js_functions import scroll_to_center_of_element


class MarketSelectorOption(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="item-title"] | .//*[@data-crlat="dropdown.menuTitle"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)

    def scroll_to_we(self, web_element=None):
        """
        Bypassing scroll
        """
        if web_element is None:
            self._logger.debug(
                f'*** Nothing passed to scroll function, scrolling to current web element "{self.__class__.__name__}"')
            web_element = self._we
        scroll_to_center_of_element(web_element)


class MarketSelectorDropDown(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="dropdown.menuItem"]'
    _list_item_type = MarketSelectorOption
    _selected_market_selector_item = 'xpath=.//*[@data-crlat="selected-item"]| .//*[@data-crlat="dropdown.selectedItem"]'
    _dropdown_market_selector = 'xpath=.//*[@data-crlat="open-menu-button"] | .//*[@data-crlat="dropdown.label"]'
    _up_arrow = 'xpath=.//*[@data-crlat="dropdown.arrowUp"]'
    _down_arrow = 'xpath=.//*[@data-crlat="dropdown.arrowDown"] | .//*[@class="dropdown-down-arrow"]'

    @property
    def has_up_arrow(self):
        return self._find_element_by_selector(selector=self._up_arrow, timeout=1) is not None

    @property
    def has_down_arrow(self):
        return self._find_element_by_selector(selector=self._down_arrow, timeout=1) is not None

    def is_expanded(self, timeout=5, expected_result=True):
        result = wait_for_result(
            lambda: 'expanded' in self.get_attribute('class'),
            timeout=timeout,
            name=f'"{self.__class__.__name__}" to be expanded',
            expected_result=expected_result)
        return result

    def _wait_active(self, timeout=0):
        self._we = self._find_myself()
        if not self.is_expanded(timeout=1):
            self.dropdown.scroll_to()
            self.dropdown.click()
            self.is_expanded()

    def expand(self):
        if self.is_expanded():
            self._logger.warning(f'*** Bypassing accordion expand, since "{self.__class__.__name__}" already expanded')
        else:
            self._logger.debug(f'*** Expanding "{self.__class__.__name__}"')

            self.dropdown.click()
            wait_for_result(lambda: self.is_expanded(timeout=0),
                            name=f'"{self.__class__.__name__}" section to expand',
                            timeout=3)

    def collapse(self):
        if not self.is_expanded():
            self._logger.warning(f'*** Bypassing accordion collapse, since "{self.__class__.__name__}" already collapsed')
        else:
            self._logger.debug(f'*** Collapsing "{self.__class__.__name__}"')
            self.dropdown.click()
            wait_for_result(lambda: self.is_expanded(expected_result=False, timeout=0),
                            expected_result=False,
                            name=f'"{self.__class__.__name__}" section to collapse',
                            timeout=3)

    @property
    def dropdown(self):
        return ComponentBase(selector=self._dropdown_market_selector, context=self._we, timeout=2)

    @property
    def change_button(self):
        return self._find_element_by_selector(selector=self._dropdown_market_selector, context=self._we, timeout=2)

    @property
    def selected_item(self):
        menu_items = self.items_as_ordered_dict
        for menu_item, menu_items_we in menu_items.items():
            if menu_items_we.is_selected(timeout=1):
                return menu_item
        else:
            raise VoltronException(f'No selected market selector item found. All items are: {menu_items}')

    @property
    def selected_market_selector_item(self):
        return self._get_webelement_text(selector=self._selected_market_selector_item, timeout=2, context=self._we)

    @property
    def available_options(self):
        return list(self.items_as_ordered_dict.keys())

    def select_value(self, value):
        self.scroll_to_we()
        self.items_as_ordered_dict[value].click()

    @property
    def value(self):
        return self.selected_item

    @value.setter
    def value(self, value):
        items = self.items_as_ordered_dict
        result = wait_for_result(lambda: value in items,
                                 name=f'Value "{value}" to appear in "{items.keys()}"', timeout=1)
        if result:
            value = items.get(value)
            value.click()
        else:
            raise VoltronException(f'"{value}" market not found. Available in dropdown markets: {list(items.keys())}')
