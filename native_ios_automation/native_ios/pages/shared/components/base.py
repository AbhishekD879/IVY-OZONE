import logging
import time
from collections import OrderedDict
from time import sleep
from typing import List
from appium.webdriver import Remote as WebDriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.command import Command
from appium.webdriver.webelement import WebElement
from tenacity import retry

from native_ios.pages.shared import get_driver
from native_ios.utils.exceptions.voltron_exception import VoltronException
from native_ios.utils.helpers import find_element_by_selector
from native_ios.utils.helpers import find_elements_by_selector
import tests_ios_fully_native_regression as tests


class IOSNativeBase(object):
    _driver = None
    _logger = None
    _list_item_type = None
    _item = None
    _context_timeout = 15
    _webview = 'WEBVIEW_com.mobenga.ladbrokes.debug' if tests.settings.brand != 'bma' else 'WEBVIEW_com.galacoral.android.debug'

    def __init__(self, selector=None, web_element=None, timeout=_context_timeout, context=None):
        self._logger = logging.getLogger('native_ios_logger')
        self.__class__._driver = get_driver()
        self._driver.switch_to.context(self._driver.contexts[0])
        self._context = context if context is not None else get_driver()
        if context is not None and context in self._driver.contexts:
            self._driver.switch_to.context(context)
            self._context = get_driver()
        else:
            self._driver.switch_to.context(self._driver.contexts[0])
            self._context = context if context is not None else get_driver()
        self._timeout = timeout
        if web_element is not None:
            self._we = web_element
            try:
                self._wait_active(timeout=self._timeout)
            except Exception as e:
                self._logger.warning(f'*** {e}')
        else:
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

    def _find_element_by_selector(self, selector='', context=None,
                                  bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, WebDriverException), timeout=1):
        context = self._driver if context is None else context
        element = find_element_by_selector(selector=selector, context=context, bypass_exceptions=bypass_exceptions,
                                           timeout=timeout)
        return element

    def _find_elements_by_selector(self, selector='', context=None,
                                   bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, WebDriverException), timeout=25):
        context = self._driver if context is None else context
        elements = find_elements_by_selector(selector=selector, context=context, bypass_exceptions=bypass_exceptions,
                                             timeout=timeout)
        if elements is None:
            return []
        return elements

    def _find_myself(self, timeout=_context_timeout):
        element = self._find_element_by_selector(selector=self._selector, context=self._context, timeout=timeout)
        if not element:
            raise VoltronException(message=f'"{self.__class__.__name__}" component not found')
        return element

    def scroll_to_we(self, direction='down'):
        # action = TouchAction(self._driver)
        # action.move_to(x=self._we.location.get("x"), y=self._we.location.get("y")).perform()
        pass
        # ToDo: need a method which scrolls to invisible native element

    def scroll_to_element(self, driver=None, element=None):
        """
        Scroll to the specified element using TouchAction.

        Args:
            driver: An instance of the Appium WebDriver.
            element: The element you want to scroll to (Appium WebElement).

        Returns:
            None
        """
        if not element:
            element = self._we
        if not driver:
            driver = self._driver
        # Get the location of the element
        location = element.location
        x = location['x']
        y = location['y']

        # Get the size of the screen
        screen_size = driver.get_window_size()
        screen_width = screen_size['width']
        screen_height = screen_size['height']

        # Calculate the scroll coordinates (you can adjust these values as needed)
        start_x = screen_width // 2
        start_y = screen_height // 2
        end_x = x
        end_y = y

        # Perform the scroll action
        action = TouchAction(driver)
        action.press(x=start_x, y=start_y).move_to(x=end_x, y=end_y).release().perform()

    def click(self):
        try :
            self.scroll_to_we()
            self._we.click()
        except Exception:
            self.switch_to_context(self._webview)
            self._driver.execute_script("arguments[0].click();", self._we)

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
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            # scroll_into_view_above(item_we)
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        self._driver.scroll(items_we[0], items_we[-1])
        return items_ordered_dict

    @property
    def scrollable_items_as_ordered_dict(self) -> OrderedDict:
        driver: WebDriver = self._driver
        items_ordered_dict = OrderedDict()
        last_item_count = 0
        while True:
            items_we: List[WebElement] = self._find_elements_by_selector(selector=self._item, context=self._we)
            self._logger.debug(
                f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
            for item_we in items_we:
                list_item = self._list_item_type(web_element=item_we)
                items_ordered_dict.update({list_item.name.upper(): list_item})
            # Check if new items were added to the ordered dict
            if len(items_ordered_dict) == last_item_count:
                break
            last_item_count = len(items_ordered_dict)
            start_x = items_we[0].location_in_view['x']
            start_y = items_we[0].location_in_view['y']
            end_x = items_we[-1].location_in_view['x']
            end_y = items_we[-1].location_in_view['y']
            action = TouchAction(driver)
            action.press(x=end_x, y=end_y).move_to(x=start_x, y=start_y).release().perform()
            # self._driver.scroll(None, items_we[-1])
        return items_ordered_dict

    def get_on_item_in_scrollable_view(self, item_name: str):
        driver: WebDriver = self._driver
        items_ordered_dict = OrderedDict()
        last_item_count = 0
        while True:
            items_we: List[WebElement] = self._find_elements_by_selector(selector=self._item, context=self._we)
            self._logger.debug(
                f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
            for item_we in items_we:
                list_item = self._list_item_type(web_element=item_we)
                items_ordered_dict.update({list_item.name.upper(): list_item})
            # Check if new items were added to the ordered dict
            if len(items_ordered_dict) == last_item_count or items_ordered_dict.get(item_name.upper()):
                break
            last_item_count = len(items_ordered_dict)
            start_x = items_we[0].location_in_view['x']
            start_y = items_we[0].location_in_view['y']
            end_x = items_we[-2].location_in_view['x']
            end_y = items_we[-2].location_in_view['y']
            action = TouchAction(driver)
            action.press(x=end_x, y=end_y).move_to(x=start_x, y=start_y).release().perform()
            # self._driver.scroll(None, items_we[-1])
        return items_ordered_dict.get(item_name.upper())

    def scroll_in_direction(self, direction='down', value=50):
        # screen_size = self._driver.get_window_rect()
        # y = screen_size['height'] // 2
        # x = screen_size['width'] // 2
        # subprocess.run(f"adb shell input swipe {x} {y} {x} {y // 2}",
        #                shell=True)
        self.switch_to_context(self._webview)
        self._driver.execute_script(f"window.scrollBy(0,{value})")
        self._driver.switch_to.context(self._driver.contexts[0])

    def scroll_to_ele(self, selector=None, uiautomatorclassname=None, text=None, timeout=2):
        el = self._find_element_by_selector(selector=selector, timeout=timeout)
        while not el:
            scrollable_locator = MobileBy.ANDROID_UIAUTOMATOR, f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().className("{uiautomatorclassname}").text("{text}"))'
            self._driver.find_element(*scrollable_locator)
            el = self._find_element_by_selector(selector=selector, timeout=timeout)
        sleep(2)
        element_coordinates = self._find_element_by_selector(selector=selector, timeout=timeout).location
        y_coordinate = element_coordinates['y']
        screen_size = self._driver.get_window_rect()
        y = screen_size['height']
        if y_coordinate > y - y // 4:
            self.scroll_in_direction(value=300)
        if y_coordinate < y // 4:
            self.scroll_in_direction(value=-300)

    def scroll_to_ele2(self, selector=None, parent_uiautomator_classname=None, parent_text=None,
                       child_uiautomator_classname=None, child_text=None):
        el = self._find_element_by_selector(selector=selector)
        while not el:
            parent = f'new UiSelector().className("{parent_uiautomator_classname}").text("{parent_text}")'
            child = f'new UiSelector().className("{child_uiautomator_classname}").text("{child_text}")'
            final = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView({child}.fromParent({parent}))'
            scrollable_locator = MobileBy.ANDROID_UIAUTOMATOR, final
            self._driver.find_element(*scrollable_locator)
            el = self._find_element_by_selector(selector=selector)

    def scroll_up_from_middle(self, flick_level=4):
        # Get the screen size
        screen_size = self._driver.get_window_rect()

        # Define the start and end coordinates for the scroll
        start_x = screen_size['width'] // flick_level
        start_y = screen_size['height'] // 1.1
        end_x = start_x
        end_y = screen_size['height'] / flick_level  # Adjust the scroll distance as needed

        # Create a TouchAction instance
        # action = TouchAction(self._driver)

        # Perform the scroll gesture
        self._driver.flick(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y)

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

    def capture_screenshot(self):
        driver: WebDriver = self._driver
        driver.save_screenshot('foo.png')

    def is_enabled(self):
        return self.get_attribute('enabled') == 'true'

    def get_attribute(self, name):
        resp = self._we._execute(Command.GET_ELEMENT_ATTRIBUTE, {'name': name})
        if resp['value'] is None:
            attribute_value = None
        else:
            attribute_value = resp['value']
        return attribute_value

    @property
    def available_contexts(self):
        return get_driver().contexts

    @property
    def current_context(self):
        return get_driver().current_context

    @staticmethod
    def switch_to_context(context):
        return get_driver().switch_to.context(context)

    def is_displayed(self):
        return self._we.is_displayed()
