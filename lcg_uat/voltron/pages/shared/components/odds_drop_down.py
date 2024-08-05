from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class OddsSelectorOption(ComponentBase):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we, timeout=3)

    def scroll_to_we(self, web_element=None):
        """
        Bypassing scroll as element in a view
        """
        pass


class OddsDropdownList(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="oddsDropDownItem"]'
    _list_item_type = OddsSelectorOption
    _selected_market_selector_item = 'xpath=.//*[@data-crlat="odds"]'
    _expanded_criteria = 'xpath=.//*[@data-crlat="oddsDropDownList"]'

    def is_expanded(self, timeout=5, expected_result=True):
        section = self._find_element_by_selector(selector=self._expanded_criteria, context=self._we, timeout=2)
        if section:
            result = wait_for_result(lambda: 'open' in section.get_attribute('class'),
                                     name=f'Drop down expand status to be "{expected_result}"',
                                     expected_result=expected_result,
                                     timeout=timeout)
            self._logger.debug(f'*** Drop down expanded status is {result}')
            return result
        return False

    @property
    def selected_market_selector_item(self):
        return self._get_webelement_text(selector=self._selected_market_selector_item, timeout=1, context=self._we)

    def select_value(self, value):
        self.click()
        self.is_expanded()
        items = self.items_as_ordered_dict
        if value in items.keys():
            items.get(value).click()
        else:
            raise VoltronException(f'"{value}" is not present in the list of available prices {list(items.keys())}')

    def is_enabled(self, expected_result=True, timeout=1, poll_interval=0.5, name=None,
                   bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, TypeError)):
        if not name:
            name = f'"{self.__class__.__name__}" enabled status is: {expected_result}'
        result = wait_for_result(lambda: 'disabled' not in self._we.get_attribute('innerHTML'),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name,
                                 bypass_exceptions=bypass_exceptions)
        return result
