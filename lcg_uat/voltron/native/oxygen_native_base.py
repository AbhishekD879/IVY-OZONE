import re
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.command import Command
from voltron.pages.shared import get_driver, get_platform
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import parse_selector
from voltron.utils.waiters import wait_for_result


class OxygenBaseNative(ComponentBase):
    _driver = None
    platform = None
    _logger = None

    def __init__(self, selector={}):
        self.__class__._driver = get_driver()
        # self._driver.switch_to.context('NATIVE_APP')
        self._driver.switch_to.context(self._driver.contexts[0])
        self.__class__.platform = get_platform()
        if selector:
            super(OxygenBaseNative, self).__init__(selector=selector[self.platform])

    @property
    def ios_keyboard(self):
        return IosKeyboard()

    def hide_keyboard(self):
        if self.platform == 'android':
            self._driver.hide_keyboard()
        else:
            self.ios_keyboard.done_button.click()

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
        self.hide_keyboard()

    @property
    def text(self):
        return self._get_webelement_text(we=self._we)

    @property
    def items(self):
        items_we = self._find_elements_by_selector(selector=self._item[self.platform], context=self._we)
        self._logger.debug('*** Found {0} {1} items'
                           .format(len(items_we), self.__class__.__name__ + ' - ' + self._list_item_type.__name__))
        items_array = []
        for item_we in items_we:
            if item_we.is_displayed():
                item_component = self._list_item_type(web_element=item_we)
                items_array.append(item_component)
        return items_array

    @property
    def items_names(self):
        items_titles = self._find_elements_by_selector(
            selector=self._list_item_type._title_text[self.platform], context=self._we)
        items_names = []
        for item_title in items_titles:
            items_names.append(item_title.text)
        return items_names

    def click_item(self, item_name: str):
        # ToDo: this is a workaround for appium issue (can't click element from context)
        items_titles = self._find_elements_by_selector(
            selector=self._list_item_type._title_text[self.platform], context=self._we)
        for title in items_titles:
            if title.text.lower() == item_name.lower():
                # ToDo: investigate if capital letters on iOS are ok
                title.click()
                break
        else:
            raise VoltronException('No item with name [%s]' % item_name)

    def get_content_desc(self):
        return self.get_attribute('name')

    def is_checked(self):
        if self.platform == 'android':
            return self.get_attribute('checked').title()
        else:
            check_white_selector = self._selector + '/../XCUIElementTypeImage[2]'
            return OxygenBaseNative(selector={'android': '',
                                              'ios': check_white_selector}).get_attribute('name') == 'check_white'

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
            'id': MobileBy.ACCESSIBILITY_ID if self.platform == 'ios' else MobileBy.ID,
            'xpath': MobileBy.XPATH
        }
        matcher = re.match(r'^([a-z]+)=(.+)', selector)
        if matcher is not None and matcher.lastindex == 2:
            sector_type = matcher.group(1)
            selector_string = matcher.group(2)
            if sector_type in by.keys():
                return by[sector_type], selector_string
            else:
                raise VoltronException('Unknown selector type [{0}]'.format(sector_type))
        else:
            raise VoltronException("Selector doesn't match pattern 'xpath=//*', given '{0}'".format(selector))

    def _find_element_by_selector(self, selector='', context=None, timeout=10):
        context = self._driver if context is None else context
        # ToDo: currently can't find from context because of appium issue
        (by, val) = self._parse_selector(selector)
        try:
            element = context.find_element(by=by, value=val)
        except NoSuchElementException:
            return wait_for_result(lambda: context.find_element(by=by, value=val),
                                   name='Waiting for web element to exist by selector %s' % selector,
                                   timeout=timeout
                                   )
        return element

    def _find_elements_by_selector(self, selector, context=None, timeout=10):
        context = self._driver if context is None else context
        (by, val) = parse_selector(selector)
        try:
            elements = context.find_elements(by=by, value=val)
        except NoSuchElementException:
            elements = wait_for_result(lambda: self._driver.find_elements(by=by, value=val),
                                       name='Waiting for web elements to exist by selector %s' % selector,
                                       timeout=timeout
                                       )
        if elements is None:
            return []
        return elements


class IosKeyboard(object):
    _done_button = {
        'android': '',
        'ios': 'xpath=//XCUIElementTypeButton[contains(@label, "Done")]'
    }

    @property
    def done_button(self):
        return OxygenBaseNative(selector=self._done_button)
