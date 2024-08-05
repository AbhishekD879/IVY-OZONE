from selenium.common.exceptions import UnexpectedTagNameException
import tests
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.utils.waiters import wait_for_result
from selenium.webdriver.support.select import Select


class Header(ComponentBase):
    _close_button = 'xpath=//*[@class="header-ctrl-r"]//span'
    _user_name = 'xpath=//*[@class="header-ctrl-username"]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    @property
    def user_name(self):
        return self._get_webelement_text(selector=self._user_name, context=self._we, timeout=1)


class AccountClosureContainer(ComponentBase):
    _name = 'xpath=.//*[@class="p-2"]'
    _icon = 'xpath=.//*[contains(@class,"product-icon")]'
    _block_button = 'xpath=.//*[contains(@class,"btn btn-sm")]'

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, context=self._we, timeout=1)

    @property
    def block_button(self):
        return ButtonBase(selector=self._block_button, context=self._we)

    def has_icon(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._icon, context=self._we, timeout=0) is not None,
            name=f'icon info presence status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class AccountClosure(ComponentBase):
    _url_pattern = r'^http[s]?:\/\/.+\/accountclosure'
    _self_exclusion = 'xpath=//*[@id="navigation-layout-page"]'
    _time_out = 'xpath=//*[@id="navigation-layout-page"]'
    _list_item_type = AccountClosureContainer
    _item = 'xpath=.//*[contains(@class, "form-element")] | //*[contains(@class,"closure-detail row")]'
    _close_account_button = 'xpath=//*[contains(text(), "CLOSE ACCOUNT")]'
    _go_to_gamstop_button = 'xpath=//*[contains(text(),"GO TO GAMSTOP")]'
    _date_filter = 'xpath=//select[@id="duration"]'
    _continue_button = 'xpath=.//*[contains(text(), "Continue")]'
    _confirm_block_button = 'xpath=//*[contains(text(),"Confirm Block")]'
    _cancel_button = 'xpath=//*[contains(text(),"Cancel") and contains(@class,"cursorPointer")]'
    _change_duration_button = 'xpath=//*[contains(text(),"Change duration")]'

    @property
    def account_closure_header(self):
        _account_closure_header = 'xpath=//vn-header-bar[@class="d-block d-sm-none"]' \
            if tests.settings.device_type == "mobile" \
            else 'xpath=//vn-header-bar[not(@class="d-block d-sm-none")]'
        return Header(selector=_account_closure_header, context=self._we)

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_button, context=self._we)

    @property
    def confirm_block_button(self):
        return ButtonBase(selector=self._confirm_block_button, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)

    @property
    def change_duration_button(self):
        return ButtonBase(selector=self._change_duration_button, context=self._we)

    @property
    def blocking_date_filter(self):
        return BlockingDateFilter(selector=self._date_filter, timeot=2)

    @property
    def go_to_gamstop_button(self):
        return ButtonBase(selector=self._go_to_gamstop_button, context=self._we)

    @property
    def close_account_button(self):
        return ButtonBase(selector=self._close_account_button, context=self._we)

    def has_close_account_button(self, timeout=5, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._close_account_button,
                                                   timeout=0) is not None,
            name=f'Close account button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def time_out_layout(self):
        return TimeOutNavigationLayout(selector=self._time_out, context=self._we)

    @property
    def self_exclusion(self):
        return SelfExclusionNavigationLayout(selector=self._self_exclusion, context=self._we)


class AccountClosureOverlay(ComponentBase):
    _continue_button = 'xpath=.//*[contains(text(), "CONTINUE")]'
    _cancel_button = 'xpath=.//*[contains(text(), "Cancel") and contains(@class,"btn-md")] | //*[contains(text(),"Cancel") and contains(@class,"cursorPointer")]'
    _date_filter = 'xpath=//select[@id="duration"]'
    common_xpath = '//*[contains(@class,"generic-modal-wrapper")]'
    _sports_book = f'xpath={common_xpath}'
    _time_out_wrapper = f'xpath={common_xpath}'
    _self_exclusion = f'xpath={common_xpath}'

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_button, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)

    @property
    def blocking_date_filter(self):
        return BlockingDateFilter(selector=self._date_filter, timeot=2)

    @property
    def sports_book_service_closure(self):
        return SportBookServiceClosure(selector=self._sports_book, timeout=2)

    @property
    def time_out_wrapper(self):
        return TimeOutModelWrapper(selector=self._time_out_wrapper, timeout=2)

    @property
    def self_exclusion_wrapper(self):
        return SelfExclusionNavigationLayout(selector=self._self_exclusion, timeout=2)


class BlockingDateFilter(ComponentBase, Select):
    def __init__(self, *args, **kwargs):
        ComponentBase.__init__(self, *args, **kwargs)
        try:
            Select.__init__(self, webelement=self._we)
        except UnexpectedTagNameException:
            pass


class SportBookServiceClosure(ComponentBase):
    _confirm_block_button = 'xpath=//*[contains(text(),"Confirm Block")]'
    _cancel_button = 'xpath=//*[contains(text(),"Cancel") and contains(@class,"cursorPointer")]'
    _change_duration_button = 'xpath=//*[contains(text(),"Change duration")]'
    _continue_button = 'xpath=.//*[contains(text(), "Continue")]'

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_button, context=self._we)

    @property
    def confirm_block_button(self):
        return ButtonBase(selector=self._confirm_block_button, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)

    @property
    def change_duration_button(self):
        return ButtonBase(selector=self._change_duration_button, context=self._we)


class SelfExclusionNavigationLayout(ComponentBase):
    _exclude_me_button = 'xpath=.//*[contains(text(),"Exclude me")]'
    _continue_process_button = 'xpath=.//*[contains(text()," CONTINUE PROCESS ")]'
    _password_input = 'xpath=.//*[@id="password"]/input'
    _confirm_self_exclusion_button = 'xpath=//*[contains(text(),"CONFIRM SELF-EXCLUSION")]'
    _change_duration_button = 'xpath=//*[contains(text(),"Change duration")]'
    _continue_button = 'xpath=//*[contains(text(),"CONTINUE") and contains(@class,"btn submit btn")]|//*[contains(text(),"CONTINUE") and contains(@class,"btn btn-primary")]'
    _cancel_button = 'xpath=//a[contains(text(),"Cancel")]'

    @property
    def header(self):
        _header = 'xpath=//vn-header-bar[not(@class="d-block d-sm-none")]' \
            if tests.settings.device_type == "mobile" \
            else 'xpath=//vn-header-bar[@class="d-block d-sm-none"]'
        return Header(selector=_header, context=self._we)

    @property
    def confirm_self_exclusion_button(self):
        return ButtonBase(selector=self._confirm_self_exclusion_button, context=self._we)

    @property
    def change_duration_button(self):
        return ButtonBase(selector=self._change_duration_button, context=self._we)

    @property
    def exclude_me_button(self):
        return ButtonBase(selector=self._exclude_me_button, context=self._we)

    @property
    def continue_process_button(self):
        return ButtonBase(selector=self._continue_process_button, context=self._we)

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_button, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)

    @property
    def password(self):
        return InputBase(selector=self._password_input, context=self._we)


class TimeOutNavigationLayout(ComponentBase):
    _date_filter = 'xpath=//select[@id="duration"]'
    _continue_button = 'xpath=.//*[contains(text(), "CONTINUE")]'

    @property
    def blocking_date_filter(self):
        return BlockingDateFilter(selector=self._date_filter, timeot=2)

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_button, context=self._we)

    @property
    def header(self):
        _header = 'xpath=//vn-header-bar[not(@class="d-block d-sm-none")]' \
            if tests.settings.device_type == "mobile" \
            else 'xpath=//vn-header-bar[@class="d-block d-sm-none"]'
        return Header(selector=_header, context=self._we)


class TimeOutModelWrapper(ComponentBase):
    _change_duration_button = 'xpath=//*[contains(text(),"Change duration")]'
    _confirm_time_out_button = 'xpath=//*[contains(text(),"CONFIRM TIME OUT")]'
    _cancel_button = 'xpath=//*[contains(text(),"CANCEL")]'
    _continue_button = 'xpath=//*[contains(text(),"CONTINUE")]'

    @property
    def change_duration_button(self):
        return ButtonBase(selector=self._change_duration_button, context=self._we)

    @property
    def confirm_time_out_button(self):
        return ButtonBase(selector=self._confirm_time_out_button, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_button, context=self._we)
