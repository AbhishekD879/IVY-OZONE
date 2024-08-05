from selenium.common.exceptions import StaleElementReferenceException
import tests
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class GamblingPageHeader(ComponentBase):
    _header_title = 'xpath=.//*[contains(@class,"header-ctrl-username")]'
    _close_button = 'xpath=.//*[contains(@class,"ui-close")]'
    _avatar = 'xpath=.//*[contains(@class,"ui-icon theme-account")]'

    @property
    def header_title(self):
        return TextBase(selector=self._header_title)

    @property
    def user_name(self):
        return self.header_title.text

    @property
    def close(self):
        return ButtonBase(selector=self._close_button)

    @property
    def avatar(self):
        return self._find_element_by_selector(selector=self._avatar, timeout=1)


class MobileGamblingPageHeader(GamblingPageHeader):
    _header_title = 'xpath=.//*[contains(@class,"header-ctrl-txt")]'
    _back_button = 'xpath=.//*[contains(@class,"ui-back")]'
    @property
    def back_button(self):
        return self._find_element_by_selector(selector=self._back_button, timeout=1)


class Immediate24HoursBreak(ComponentBase):
    _message_panel = 'xpath=.//*[contains(@class,"message-panel")]'

    @property
    def close(self):
        _close_icon = 'xpath=.//vn-header-bar[2]//*[contains(@class,"close theme")]' if tests.settings.device_type == 'mobile' else 'xpath=.//vn-header-bar[1]//*[contains(@class,"close theme")]'
        return self._find_element_by_selector(selector=_close_icon, timeout=3)

    def has_message_panel_displayed(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._message_panel, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'Message panel shown status to be "{expected_result}"'
        )


class GamblingControlMenuItems(ComponentBase):
    _header_title = 'xpath=.//*[@class="list-nav-txt"]'
    _short_description = 'xpath=.//*[@class="sublist-nav"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._header_title, timeout=1)

    @property
    def short_desc(self):
        return self._find_element_by_selector(selector=self._short_description, timeout=1)


class GamblingControlsOption(ComponentBase):
    _image = 'xpath=.//img'
    _title = 'xpath=.//*[contains(@class, "mat-expansion-panel-header-title")]/span'
    _item = 'xpath=.//*[@class="menu-item"]'
    _list_item_type = GamblingControlMenuItems
    _chevron = 'xpath=.//*[contains(@class,"mat-expansion-indicator")]'
    _inner_section = 'xpath=.//*[contains(@class, "mat-expansion-panel-header mat")]'

    @property
    def image(self):
        return self._find_element_by_selector(selector=self._image, timeout=3)

    @property
    def title(self):
        return TextBase(selector=self._title, context=self._we)

    @property
    def name(self):
        return self.title.name

    @property
    def chevron(self):
        return self._find_element_by_selector(selector=self._chevron, timeout=3)

    @property
    def _section(self):
        return self._find_element_by_selector(selector=self._inner_section, context=self._we, timeout=2)

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException,)):
        result = wait_for_result(lambda: '-expanded' in self._section.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Panel to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'"{self.__class__.__name__}" panel expanded status is "{result}"')
        return result


class GamblingControls(BaseContent):
    _url_pattern = r'^https?://[a-zA-Z0-9.-]+/en/mobileportal/gamblingcontrols'
    _item = 'xpath=.//mat-accordion/div/*[contains(@class,"mat-expansion-panel")]'
    _list_item_type = GamblingControlsOption
    _option_content = 'xpath=.//*[@class="tab-tiles-content"]'
    _choose_button = 'xpath=.//button[contains(text(), "Choose")]'
    _time_management = 'xpath=.//*[@alt="Time Management"]'
    _account_closure = 'xpath=.//*[@alt="Account Closure & Reopening"]'
    _has_gambling_controls_content = 'xpath=.//*[contains(@class,"mat-expansion-panel-header-title ng-tns-c2690051721")]'

    @property
    def has_gambling_controls_content(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._has_gambling_controls_content, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'Close button shown status to be "{expected_result}"'
        )

    @property
    def header_line(self):
        # Return a class to return separate locator for mobile (Don't use device type in Xpaths)
        _header_line = 'xpath=.//vn-header-bar[2]/*[@class="header-ctrl-wrapper ng-star-inserted"]' if tests.settings.device_type == 'mobile' else 'xpath=.//*[@class="header-ctrl-wrapper ng-star-inserted"]'
        _header_line_type = MobileGamblingPageHeader if tests.settings.device_type == 'mobile' else GamblingPageHeader
        return _header_line_type(selector=_header_line)
    @property
    def time_management(self):
        return self._find_element_by_selector(selector=self._time_management, context=self._we)

    @property
    def account_closure(self):
        return self._find_element_by_selector(selector=self._account_closure, context=self._we)

    @property
    def choose_button(self):
        return ButtonBase(selector=self._choose_button, context=self._we)

    def select_option(self, option_name: str):
        items = self.items_as_ordered_dict
        if option_name in items:
            items[option_name].click()
        else:
            raise VoltronException(f'Item "{option_name}" not found, it has to be one of ["{", ".join(items.keys())}"]')

    @property
    def selected_option(self):
        options = self.items_as_ordered_dict
        selected_option = [option for option in options.values() if option.is_selected()]
        if len(selected_option) != 1:
            raise VoltronException(f'There is "{len(selected_option)}" selected options on "Gambling Controls" page.'
                                   f'Should be only one.')
        return selected_option

    @property
    def option_content(self):
        return self._get_webelement_text(selector=self._option_content, context=self._we)