import tests
from voltron.environments.constants import gvc
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.checkboxes import CheckBoxBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.contents.registration.primitives.input import RegistrationInput
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class CoralDepositLimitsItem(ComponentBase):
    _input = 'xpath=.//input'
    _label = 'xpath=.//*[contains(@class, "sports-pill")]'

    @property
    def name(self):
        return self._we.text
        # return self._get_webelement_text(selector=self._label)

    @property
    def input(self):
        return ComponentBase(selector=self._input, context=self._we)


class CoralRegistrationDepositLimits(ComponentBase):
    _message = 'xpath=.//p'
    _item = 'xpath=.//*[@class="row"]/div[contains(@class, "col")]/a'
    _list_item_type = CoralDepositLimitsItem
    _amount = 'xpath=.//lh-form-field'
    _amount_type = RegistrationInput

    @property
    def message(self):
        return self._get_webelement_text(selector=self._message)

    @property
    def amount(self):
        return self._amount_type(selector=self._amount, context=self._we)


class CoralRegistrationFundsProtection(ComponentBase):
    _checkbox = 'xpath=.//div[./input[@id="fundprotection"]]'
    _checkbox_type = CheckBoxBase

    @property
    def checkbox(self):
        if tests.settings.device_type == 'mobile' and tests.use_browser_stack and self.is_safari:
            return self._find_elements_by_selector(selector='xpath=.//input[@id="fundprotection"]', context=self._we)[0]
        else:
            return self._checkbox_type(selector=self._checkbox, context=self._we)


class CoralFundsRegulation(ComponentBase):
    _deposit_limits = 'xpath=.//*[contains(@class, "bonus-card")]'
    _deposit_limits_type = CoralRegistrationDepositLimits
    _funds_protection = 'xpath=.//*[contains(@class, "funds-protection")]'
    _funds_protection_type = CoralRegistrationFundsProtection

    @property
    def deposit_limits(self):
        return self._deposit_limits_type(selector=self._deposit_limits, context=self._we)

    @property
    def funds_protection(self):
        return self._funds_protection_type(selector=self._funds_protection, context=self._we)


class CoralSetLimitsHeaderBar(ComponentBase):
    _page_title = 'xpath=.//*[contains(@class, "header-ctrl-txt")]'
    _close_button = 'xpath=.//*[contains(@class, "ui-close")]'

    @property
    def page_title(self):
        return TextBase(selector=self._page_title, context=self._we).name

    def has_close_button(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._close_button, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'Close button shown status to be "{expected_result}"'
        )


class CoralSetYourDepositLimits(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/en/mobileportal/lcgfundsregulation'
    _url_matcher_timeout = 20
    _header_line = 'xpath=.//lh-header-bar'
    _funds_regulation = 'xpath=.//*[@id="fundsregulation"]'
    _funds_regulation_type = CoralFundsRegulation
    _submit_button = 'xpath=.//button'
    _header_line_type = CoralSetLimitsHeaderBar

    @property
    def funds_regulation(self):
        return self._funds_regulation_type(selector=self._funds_regulation, context=self._we)

    @property
    def submit_button(self):
        return ButtonBase(selector=self._submit_button, context=self._we)

    def set_limits(self, deposit_limit=None, terms_and_conditions=True):
        limits = self.funds_regulation.deposit_limits.items_as_ordered_dict
        if not limits:
            raise VoltronException('No Limits Option available')
        if deposit_limit:
            limit = limits.get(gvc.YES_SET_LIMIT_NOW)
            limit.click()
            choose_limits = self.funds_regulation.deposit_limits.items_as_ordered_dict
            limit_name, limit = list(choose_limits.items())[-1]
            limit.click()
            self.funds_regulation.deposit_limits.amount.input.value = deposit_limit
        else:
            limit = limits.get(gvc.NO_MAYBE_LATER)
            limit.click()
        self.submit_button.click()
        if terms_and_conditions:
            if tests.settings.device_type == 'mobile' and tests.use_browser_stack and self.is_safari:
                self.funds_regulation.funds_protection.checkbox.click()
            else:
                self.funds_regulation.funds_protection.checkbox.value = True
        self.submit_button.click()
