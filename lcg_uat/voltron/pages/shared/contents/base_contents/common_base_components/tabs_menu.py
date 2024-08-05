from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.webdriver import ActionChains
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from voltron.utils.js_functions import mouse_event_click as safari_click, scroll_to_center_of_element


class TabsMenuItem(ComponentBase):
    _item_name = 'xpath=.//a[@data-crlat="tab"]/span | .//*[@data-crlat="buttonSwitch"]/span'  # VOL-4078
    _fade_out_overlay = True

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None):
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        return wait_for_result(lambda: self.background_color_name == 'main_blue',
                               expected_result=expected_result,
                               timeout=timeout,
                               poll_interval=poll_interval,
                               name=name)

    @property
    def name(self):
        result = wait_for_result(lambda: self._get_webelement_text(selector=self._item_name),
                                 name="Tab to have visible name",
                                 timeout=5)
        return result if result else ''

    def click(self):
        we = self._find_element_by_selector(selector=self._item_name)
        self.scroll_to_we(we)
        if self.is_safari:
            safari_click(we)
        else:
            self.scroll_to_we()
            try:
               we.click()
            except:
                ActionChains(get_driver()).move_to_element(we).click(we).perform()


class TabsMenu(ComponentBase):
    _item = 'xpath=.//*[contains(@data-crlat, "tab.tpTabs") and not(@hidden)] | .//*[@data-crlat="buttonSwitch"]/parent::li[not(@hidden)]'
    _list_item_type = TabsMenuItem
    _selected_item = 'xpath=.//*[contains(@class, "active")]'

    def _wait_active(self, timeout=0):
        try:
            self._find_element_by_selector(selector=self._item, context=self._context,
                                           bypass_exceptions=(NoSuchElementException, ), timeout=3)
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')

    @property
    def menu_item_names(self):
        return list(self.items_as_ordered_dict.keys())

    @property
    def current(self):
        try:
            return self._list_item_type(selector=self._selected_item, context=self._we, timeout=2).name
        except (StaleElementReferenceException, VoltronException):
            self._logger.debug(f'*** Overriding Exception in {self.__class__.__name__}')
            self._we = self._find_myself(timeout=2)
            return self._list_item_type(selector=self._selected_item, context=self._we, timeout=2).name

    def click(self):
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')

    def open_tab(self, tab_name, timeout=5):
        scroll_to_center_of_element(self._we)
        result = wait_for_result(lambda: tab_name in self.items_as_ordered_dict,
                                 name=f'Tab "{tab_name}" to appear in {self.__class__.__name__} - {self._list_item_type.__name__}',
                                 timeout=timeout)
        if not result:
            raise VoltronException('Tab name "%s" is not found in list of tabs ["%s"]'
                                   % (tab_name, '", "'.join(filter(None, self.items_as_ordered_dict.keys()))))
        if tab_name == self.current:
            self._logger.warning(f'*** Bypassing click on tab "{tab_name}" as it is already active')
            return True
        opened_tab = self.items_as_ordered_dict[tab_name]
        scroll_to_center_of_element(opened_tab._we)
        opened_tab.click()
        return wait_for_result(lambda: self.current == tab_name,
                               name=f'"{tab_name}" to be active',
                               bypass_exceptions=(NoSuchElementException,
                                                  StaleElementReferenceException,
                                                  VoltronException),
                               timeout=timeout)


class SwitchersMenuItem(TabsMenuItem):
    _item_name = 'xpath=.//*[@data-crlat="switcher.name"]'


class SwitchersMenu(TabsMenu):
    _item = 'xpath=.//*[contains(@data-crlat, "buttonSwitch") and not(@hidden)]'
    _switcher_tab_list = 'xpath=//*[@data-crlat="switcher.name"]'
    _list_item_type = SwitchersMenuItem
