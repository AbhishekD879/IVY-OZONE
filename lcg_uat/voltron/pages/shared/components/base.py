import itertools
import logging
from collections import OrderedDict

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains

from voltron.pages.shared import get_device_properties
from voltron.pages.shared import get_driver
from voltron.pages.shared import get_platform
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import find_element
from voltron.utils.helpers import find_elements
from voltron.utils.helpers import parse_pattern
from voltron.utils.js_functions import get_css_property_text, scroll_to_center_of_element, click, delete_popups
from voltron.utils.js_functions import get_location
from voltron.utils.js_functions import mouse_event_click as safari_click
from voltron.utils.waiters import wait_for_result


class ComponentBase(object):
    _local_spinner = 'xpath=.//*[contains(@data-crlat, "spinner.loader") or contains(@class, "spinner-loader")]'
    _betslip_animation = 'xpath=//*[@data-crlat="betSlipAnimation"]'
    _is_focused_flag = 'dk-active-input'
    _fade_out_screen_container = 'xpath=.//*[@data-crlat="fadeOutCont"]'
    _fade_out_overlay = False
    _verify_spinner = False
    _list_item_type = None
    _item = None
    _pattern_values = {}
    currencies = ['$', 'Kr', '€', '£', 'HK', 'AU']
    _context_timeout = 15
    safari_browser = 'safari'
    _color_map = {
        'rgba(0, 0, 0, 0)': 'transparent',
        'rgba(7, 41, 75, 1)': 'main_blue',
        'rgba(240, 30, 40, 1)': 'red',
        'rgba(18, 132, 224, 1)': 'blue',
        'rgba(67, 189, 53, 1)': 'green',
        'rgba(45, 179, 67, 1)': 'green',
        'rgba(255, 205, 0, 1)': 'yellow'
    }

    def __init__(self, selector='', context=None, web_element=None, timeout=_context_timeout, pattern_values=None, *args, **kwargs):
        self._logger = logging.getLogger('voltron_logger')
        self._args, self._kwargs = args, kwargs
        self._context = context if context is not None else get_driver()
        self._selector = selector
        self._timeout = timeout
        if isinstance(pattern_values, dict):
            self._pattern_values.update(pattern_values)
        if web_element is not None:
            self._we = web_element
            try:
                self._load_complete(timeout=self._timeout)
                self._wait_active(timeout=self._timeout)
            except Exception as e:
                self._logger.warning(f'*** {e}')
        else:
            if self._pattern_values:
                selector = parse_pattern(selector, pattern_values=self._pattern_values)
            self._selector = selector
            self._load_complete(timeout=self._timeout)
            self._wait_active(timeout=self._timeout)
            self._we = self._find_myself(timeout=self._timeout)

    @property
    def is_safari(self):
        if get_platform() == 'ios':
            return True
        else:
            return (get_device_properties()['browser'].lower() in ['safari','chromium'] and
                    'iphone' in get_device_properties()['device'].lower())

    def _load_complete(self, timeout=_context_timeout):
        """
        Waits for component to load. Most commonly component is considered to be loaded if splash disappears, url is
        changed (if applicable), spinner and fade out overlay are gone.
        :param timeout:
        :return:
        """
        if self._fade_out_overlay:
            self._fade_out_container_wait()
        if self._verify_spinner:
            return self._spinner_wait()
        return False

    def _spinner_wait(self, timeout=_context_timeout):
        """
        Waits for spinner to disappear. Looks for spinner within current context (web element or web driver)
        :param timeout:
        :return:
        """
        def check_spinner_displayed():
            try:
                spinner = self._find_element_by_selector(selector=self._local_spinner, context=self._context, timeout=0)
                if spinner is None:
                    return False
                self.scroll_to_we(spinner)
                return spinner.is_displayed()
            except StaleElementReferenceException:
                try:
                    self._we = self._find_myself(timeout=1)
                    spinner = self._find_element_by_selector(selector=self._local_spinner, context=self._we, timeout=0)
                    if spinner is None:
                        return False
                    self.scroll_to_we(spinner)
                    return spinner.is_displayed()
                except VoltronException:
                    return False

        wait_for_result(lambda: check_spinner_displayed(),
                        name=f'Local spinner displayed. Context "{self.__class__.__name__}"',
                        expected_result=False,
                        timeout=timeout)

    def _fade_out_container_wait(self, timeout=_context_timeout):
        """
        Waits for fade_out_screen_container class to disappear
        :param timeout:
        :return:
        """
        def check_fade_out_container():
            try:
                container = self._find_element_by_selector(selector=self._fade_out_screen_container, context=self._context, timeout=0)
                return container.is_displayed()
            except AttributeError:
                return False
            except StaleElementReferenceException:
                try:
                    fadeout = self._find_element_by_selector(selector=self._fade_out_screen_container, context=self._context, timeout=0)
                    self.scroll_to_we(fadeout)
                    return fadeout.is_displayed()
                except (AttributeError, VoltronException):
                    return False

        result = wait_for_result(lambda: check_fade_out_container(),
                                 name=f'Fade out screen container is displayed. Context "{self.__class__.__name__}"',
                                 expected_result=False,
                                 timeout=timeout)
        return result

    def wait_for_fade_out(self,
                          expected_result: bool = True,
                          bypass_exceptions=(NoSuchElementException, StaleElementReferenceException),
                          timeout: int = 1,
                          poll_interval: int = 0.5):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._fade_out_screen_container,
                                                                      context=self._context,
                                                                      timeout=0) is not None,
                               name=f'Fadeout container to be {expected_result}',
                               bypass_exceptions=bypass_exceptions,
                               expected_result=expected_result,
                               poll_interval=poll_interval,
                               timeout=timeout)

    def _wait_active(self, timeout=_context_timeout):
        """
        Waits for component's content to be loaded.
        :return:
        """
        pass

    def _find_element_by_selector(self, selector='', context=None, pattern_values=None,
                                  bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, WebDriverException),
                                  timeout=10):
        context = self._we if context is None else context

        selector = parse_pattern(selector, pattern_values=pattern_values) if pattern_values else selector
        element = find_element(selector=selector, context=context, bypass_exceptions=bypass_exceptions, timeout=timeout)
        return element

    def _find_myself(self, timeout=_context_timeout):
        element = self._find_element_by_selector(selector=self._selector, context=self._context, timeout=timeout)
        if not element:
            raise VoltronException(message=f'"{self.__class__.__name__}" component not found')
        return element

    def _find_elements_by_selector(self, selector='', context=None, pattern_values=None,
                                   bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, WebDriverException), timeout=25):
        context = self._we if context is None else context
        selector = parse_pattern(selector, pattern_values=pattern_values) if pattern_values else selector
        elements = find_elements(selector=selector, context=context, bypass_exceptions=bypass_exceptions, timeout=timeout)
        if elements is None:
            return []
        return elements

    @property
    def background_color_value(self):
        return self._we.value_of_css_property('background-color')

    @property
    def text_color_value(self):
        return self.css_property_value('color')

    @property
    def opacity_value(self):
        return self.css_property_value('opacity')

    @property
    def background_color_name(self):
        return self._color_map.get(self.background_color_value, 'unknown')

    def css_property_value(self, value):
        value = self._we.value_of_css_property(value)
        if not value:
            raise VoltronException(f'CSS Value "{value}" is empty/not exist for "{self.__class__.__name__}"')
        return value

    @property
    def has_landscape_animation(self):
        result = wait_for_result(lambda: self.css_property_value('display'),
                                 name='property value',
                                 timeout=5)
        return result

    def scroll_to_we(self, web_element=None):
        if web_element is None:
            self._logger.debug(f'*** Nothing passed to scroll function, scrolling to current web element "{self.__class__.__name__}"')
            web_element = self._we
        scroll_to_center_of_element(web_element)

    def wait_for_element_disappear(self, we=None, timeout=10):
        if we is None:
            self._logger.warning(f'*** Nothing passed to wait for element disappear function "{self.__class__.__name__}"')
            we = self._we

        def check_disappear(webelement):
            try:
                return not webelement.is_displayed()
            except StaleElementReferenceException:
                return True
            except NoSuchElementException:
                return True

        return wait_for_result(lambda: check_disappear(webelement=we), timeout=timeout,
                               name=f'WebElement "{self.__class__.__name__}" to disappear')

    def scroll_to_bottom(self):
        drv = get_driver()
        drv.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    def scroll_to_top(self):
        drv = get_driver()
        drv.execute_script("window.scrollTo(0,0);")

    def _get_webelement_text(self, selector='', we=None, context=None, pattern_values=None, timeout=0) -> str:
        try:
            if we:
                return self._we_text(we)
            elif selector is not None and selector != '':
                selector = parse_pattern(selector, pattern_values=pattern_values) if pattern_values else selector
                we = self._find_element_by_selector(selector=selector, context=context, timeout=timeout)
                return self._we_text(we) if we else ''
            else:
                raise VoltronException(
                    'Internal error: No selector or webelement passed to get_webelement_text function')
        except StaleElementReferenceException:
            we = self._find_element_by_selector(selector=selector, context=context, timeout=timeout)
            self._we = we
            return self._we_text(we) if we else ''
        except Exception as err:
            raise VoltronException(f'Error getting WebElement text. Exception string: "{err}"')

    def _we_text(self, we):
        try:
            if self.is_safari:
                return we.get_attribute('innerText').strip('\n').strip()
            else:
                return we.text
        except Exception as err:
            return we.get_attribute('innerText').strip('\n').strip()

    def _wait_for_not_empty_web_element_text(self, selector='', we=None, context=None, pattern_values=None, name=None, timeout=0):
        return wait_for_result(lambda: self._get_webelement_text(selector, we, context, pattern_values, timeout=0),
                               name=name if name else f'Waiting while text of {selector} is not empty',
                               timeout=timeout)

    def wait_for_betslip_animation_disappear(self):
        device = get_device_properties()
        if device['type'] == 'desktop':
            self._logger.warning('*** Bypassing wait for Betslip animation as it\'s not present on Desktop')
            return
        try:
            wait_for_result(lambda: 'bet-visible' not in self._find_element_by_selector(selector=self._betslip_animation,
                                                                                        context=get_driver(),
                                                                                        timeout=0.5).get_attribute('class'),
                            name='Waiting till Betslip animation disappears',
                            timeout=3,
                            poll_interval=1,
                            bypass_exceptions=(),
                            )
        except (NoSuchElementException, AttributeError):
            pass
        except StaleElementReferenceException:
            pass

    def scroll_to(self):
        self.scroll_to_we()

    def click(self):
        self.scroll_to_we()
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')

    def perform_click(self, we=None):
        self._logger.debug(
            f'*** User has clicked "{self._we.text}" button. Call "{self.__class__.__name__}.click" method'
        )
        we = we if we else self._we
        if self.is_safari:
            get_driver().implicitly_wait(0.7)
            try:
                we.click()
            except:
                safari_click(we)
            get_driver().implicitly_wait(0)
        else:
            try:
                we.click()
            except:
                click(we)

    def check_click(self, we=None):
        self._logger.debug(
            f'*** User has clicked "{self._we.text}" button. Call "{self.__class__.__name__}.click" method'
        )
        we = we if we else self._we
        if self.is_safari:
            get_driver().implicitly_wait(0.7)
            safari_click(we)
            get_driver().implicitly_wait(0)
        else:
            we.click()

    def is_displayed(self, expected_result=True, timeout=1, poll_interval=0.5, name=None, scroll_to=True,
                     bypass_exceptions=(NoSuchElementException, StaleElementReferenceException)) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" displayed status is: {expected_result}'
        self.scroll_to_we() if scroll_to else None
        if self.is_safari:
            return True if self._we else False
        result = wait_for_result(lambda: self._we.is_displayed(),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 bypass_exceptions=bypass_exceptions,
                                 name=name)
        return result

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        result = wait_for_result(lambda: 'active' in self.get_attribute('class').strip(' ').split(' '),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name)
        return result

    def is_focused(self, expected_result=True, timeout=2, poll_interval=0.5, name=None) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        result = wait_for_result(lambda: f"{self._is_focused_flag}" in self.get_attribute('class').strip(' ').split(' '),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name)
        return result

    def is_disabled(self, *args, **kwargs):
        raise VoltronException('Deprecated method "is_disabled", use "is_enabled" instead')

    def is_active(self, *args, **kwargs):
        raise VoltronException('Deprecated method "is_active", use "is_selected" instead')

    def is_enabled(self, expected_result=True, timeout=1, poll_interval=0.5, name=None,
                   bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, TypeError)) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" enabled status is: {expected_result}'

        def _is_enabled(we):
            if we.get_attribute('disabled') is not None:
                return any([False for status in ('true', 'disabled') if status in we.get_attribute('disabled')])
            elif 'disabled' in we.get_attribute('class').strip(' ').split(' '):
                return False
            else:
                return True

        result = wait_for_result(lambda: _is_enabled(we=self._we),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name,
                                 bypass_exceptions=bypass_exceptions)
        return result

    def is_truncated(self, we=None, selector='', context=None) -> bool:
        """Verifies if in case of long name it's truncated like this: 'long event nam...' """
        if we:
            webelement = we
        elif selector is not None and selector != '':
            webelement = self._find_element_by_selector(selector=selector, timeout=1, context=context)
        else:
            webelement = self._we

        def _is_truncated(webelement_):
            text_overflow = webelement_.value_of_css_property('text-overflow')
            overflow = webelement_.value_of_css_property('overflow')
            white_space = webelement_.value_of_css_property('white-space')
            is_truncated = all((text_overflow == 'ellipsis', overflow == 'hidden', white_space == 'nowrap'))
            return is_truncated
        parent_webelement = self._find_element_by_selector(selector='xpath=..', context=webelement, timeout=0)

        return any((_is_truncated(webelement), _is_truncated(parent_webelement)))

    def is_wrapped(self, we=None, selector='', context=None) -> bool:
        """
        Verifies if text is wrapped to the next line
        """
        if we:
            webelement = we
        elif selector is not None and selector != '':
            webelement = self._find_element_by_selector(selector=selector, timeout=1, context=context)
        else:
            webelement = self._we

        def _is_wrapped(webelement_):
            import re
            word_break = webelement_.value_of_css_property('word-break')
            is_wrapped = word_break == 'break-word'
            return is_wrapped or webelement.size['height'] >= \
                int(re.findall(r'\d+', webelement.value_of_css_property('font-size'))[0]) * 2
        parent_webelement = self._find_element_by_selector(selector='xpath=..', context=webelement, timeout=0)
        return any((_is_wrapped(webelement), _is_wrapped(parent_webelement)))

    @property
    def items(self):
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_array = []
        for item_we in items_we:
            if item_we.is_displayed():
                item_component = self._list_item_type(web_element=item_we)
                items_array.append(item_component)
        return items_array

    @property
    def items_names(self):
        return list(self.items_as_ordered_dict.keys())

    def click_item(self, item_name: str, timeout: int = 5):
        if not item_name:
            raise VoltronException('Item name was not specified')

        item_found = wait_for_result(lambda: next((item for item_name_, item in self.items_as_ordered_dict.items()
                                                   if item_name_.upper().strip() == item_name.upper()), None),
                                     timeout=timeout,
                                     name=f'Specified "{item_name}" to appear between items')
        if not item_found:
            raise VoltronException(f'"{self.__class__.__name__}" item: "{item_name}" not found in items list: {self.items_names}')
        item_found.click()

    @property
    def has_items(self):
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        return bool(items_we)

    @property
    def first_item(self):
        item_we = self._find_element_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        if not item_we:
            return (None, None)
        list_item = self._list_item_type(web_element=item_we)
        return (list_item.name, list_item)

    def n_items_as_ordered_dict(self, no_of_items=5) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        n_items_ordered_dict = OrderedDict()
        for item_we in items_we[:no_of_items]:
            list_item = self._list_item_type(web_element=item_we)
            list_item.scroll_to()
            n_items_ordered_dict.update({list_item.name: list_item})
        return n_items_ordered_dict

    @property
    def count_of_items(self):
        return len(self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout))

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            list_item.scroll_to()
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict

    @property
    def expanded_items(self) -> OrderedDict:
        _expanded_items = self._item[:len(self._item) - 1] + " and contains(@class, 'is-expanded')]"
        items_we = self._find_elements_by_selector(selector=_expanded_items, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            list_item.scroll_to()
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict

    @property
    def items_as_ordered_dict_inc_dup(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        # Generate unique keys using itertools.count()
        key_generator = itertools.count()
        # Create an OrderedDict with generated unique keys
        items_ordered_dict = OrderedDict((next(key_generator), self._list_item_type(web_element=item_we)) for item_we in items_we
        )
        return items_ordered_dict

    def wait_item_appears(self, item_name, timeout=15, expected_result=True):
        return wait_for_result(lambda: item_name in self.items_as_ordered_dict,
                               name='Item "%s" appear status in items list to be %s' % (item_name, expected_result),
                               expected_result=expected_result,
                               timeout=timeout)

    def get_items(self, **kwargs) -> OrderedDict:
        """
        Get limited number of items in container
        :param kwargs: number - number of items
        :return: OrderedDict with item name: item web element
        """
        number = kwargs.get('number')
        name = kwargs.get('name')
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        search_scope = [item_we for item_we in items_we] if name else [item_we for item_we in items_we[:number]]

        items_ordered_dict = OrderedDict()
        for item_we in search_scope:
            list_item = self._list_item_type(web_element=item_we)
            list_item_name = list_item.name
            if name and (list_item_name.lower() == name.lower()):
                items_ordered_dict.update({name: list_item})
                break
            else:
                items_ordered_dict.update({list_item_name: list_item})
        return items_ordered_dict

    def get_attribute(self, attribute):
        result = self._we.get_attribute(attribute)
        self._logger.debug(f'*** Found attribute "{result}" for {self.__class__.__name__}')
        return result

    @property
    def size(self):
        return self._we.size

    @property
    def location(self):
        if self.is_safari:
            return get_location(self._we)
        else:
            return self._we.location

    def wait_until_refreshed(self, timeout=5, poll_interval=0.5, item=None, name=None):
        item = item if item else self._item
        name = name if name else f'Class "{self.__class__.__name__}" Item with xpath "{item}" to refresh'
        result = False
        a = self._find_elements_by_selector(selector=item, timeout=0)
        for i in range(0, len(a)):
            result = wait_for_result(lambda: a[i] != self._find_elements_by_selector(selector=item, timeout=0.5)[i],
                                     name=name,
                                     timeout=timeout,
                                     poll_interval=poll_interval)
        return result

    def strip_currency_sign(self, text):
        text = '' if text is None else text
        for i in self.currencies:
            text = text.replace(i, '')
        return text

    def get_currency_sign(self, text):
        text = '' if text is None else text
        for i in self.currencies:
            if i in text:
                return i
        return None

    def mouse_over(self, we=None):
        # todo: VOL-1875
        if not we:
            we = self._we
        ActionChains(get_driver()).move_to_element(we).perform()

    def after_element(self, selector, context=None):
        context = context if context else get_driver()
        el = self._find_element_by_selector(selector=selector, context=context, timeout=1)
        if el:
            return get_css_property_text(el, ':after')
        else:
            return None

    def before_element(self, selector, context=None):
        context = context if context else get_driver()
        el = self._find_element_by_selector(selector=selector, context=context, timeout=1)
        if el:
            return get_css_property_text(el, ':before')
        else:
            return None
