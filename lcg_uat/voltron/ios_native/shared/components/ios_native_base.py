import re
import logging
from collections import OrderedDict
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.command import Command
from voltron.pages.shared import get_driver
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class IOSNativeBase(object):
    _driver = None
    _logger = None
    _list_item_type = None
    _item = None
    _context_timeout = 15

    def __init__(self, selector=None, timeout=_context_timeout, context=None):
        self._logger = logging.getLogger('voltron_logger')
        self.__class__._driver = get_driver()
        self._driver.switch_to.context(self._driver.contexts[0])
        self._context = context if context is not None else get_driver()
        self._timeout = timeout
        if selector:
            self._selector = selector
            self._wait_active(timeout=self._timeout)
            self._we = self._find_myself(timeout=self._timeout)

    def _wait_active(self, timeout=_context_timeout):
        """
        Waits for component's content to be loaded.
        :return:
        """
        pass

    def _find_myself(self, timeout=_context_timeout):
        element = self._find_element_by_selector(selector=self._selector, context=self._context, timeout=timeout)
        if not element:
            raise VoltronException(message=f'"{self.__class__.__name__}" component not found')
        return element

    def scroll_to_we(self, direction='down'):
        pass
        # ToDo: need a method which scrolls to invisible native element

    def click(self):
        self.scroll_to_we()
        self._we.click()

    def clear(self):
        self.scroll_to_we()
        self._we.clear()

    def type(self, text):
        self.clear()
        self._we.set_value(text)

    def enter_text(self, text):
        self.type(text)

    @property
    def text(self):
        return self._we.text

    @property
    def items(self):
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug('*** Found {0} {1} items'
                           .format(len(items_we), self.__class__.__name__ + ' - ' + self._list_item_type.__name__))
        items_array = []
        for item_we in items_we:
            if item_we.is_displayed():
                item_component = self._list_item_type(web_element=item_we)
                items_array.append(item_component)
        return items_array

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict

    def click_item(self, item_name: str):
        # ToDo: this is a workaround for appium issue (can't click element from context)
        items_titles = self._find_elements_by_selector(
            selector=self._list_item_type._title_text, context=self._we)
        for title in items_titles:
            if title.text.lower() == item_name.lower():
                # ToDo: investigate if capital letters on iOS are ok
                title.click()
                break
        else:
            raise VoltronException(f'No item with name [{item_name}]')

    def is_enabled(self):
        return self.get_attribute('enabled') == 'true'

    def get_attribute(self, name):
        resp = self._we._execute(Command.GET_ELEMENT_ATTRIBUTE, {'name': name})
        if resp['value'] is None:
            attribute_value = None
        else:
            attribute_value = resp['value']
        return attribute_value

    def _parse_selector(self, selector=''):
        by = {
            'id': MobileBy.ACCESSIBILITY_ID,
            'xpath': MobileBy.XPATH
        }
        matcher = re.match(r'^([a-z]+)=(.+)', selector)
        if matcher is not None and matcher.lastindex == 2:
            sector_type = matcher.group(1)
            selector_string = matcher.group(2)
            if sector_type in by.keys():
                return by[sector_type], selector_string
            else:
                raise VoltronException(f'Unknown selector type [{sector_type}]')
        else:
            raise VoltronException(f"Selector doesn't match pattern 'xpath=//*', given '{selector}'")

    def _find_element_by_selector(self, selector='', context=None, timeout=10):
        context = self._driver if context is None else context
        # ToDo: currently can't find from context because of appium issue
        (by, val) = self._parse_selector(selector)
        try:
            element = context.find_element(by=by, value=val)
        except NoSuchElementException:
            return wait_for_result(lambda: context.find_element(by=by, value=val),
                                   name=f'Waiting for web element to exist by selector "{selector}"',
                                   timeout=timeout
                                   )
        return element

    def _find_elements_by_selector(self, selector, context=None, timeout=10):
        context = self._driver if context is None else context
        (by, val) = self._parse_selector(selector)
        try:
            elements = context.find_elements(by=by, value=val)
        except NoSuchElementException:
            elements = wait_for_result(lambda: self._driver.find_elements(by=by, value=val),
                                       name=f'Waiting for web elements to exist by selector "{selector}"',
                                       timeout=timeout
                                       )
        if elements is None:
            return []
        return elements
