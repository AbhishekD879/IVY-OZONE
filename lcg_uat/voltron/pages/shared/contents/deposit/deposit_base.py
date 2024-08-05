from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import switch_to_iframe, switch_to_main_page
from voltron.utils.waiters import wait_for_result


class GVCDepositContent(ComponentBase):
    _close_button = 'xpath=.//*[contains(@class, "close-button")] | .//*[contains(@class, "ui-close")]| .//*[@class="quick-deposit__svg"]'
    _deposit_title = 'xpath=//cashier-header//div[contains(@class,"header-ctrl-txt")]'
    _deposit_sub_title = 'xpath=.//*[@class="main"]/*[contains(text(),"Select a deposit method")] | //*[contains(text()," Popular Payment Methods ")]'
    _back_btn = 'xpath=.//*[@class="button-back"] | .//*[contains(@class,"back")]'
    _add_card = 'xpath=.//*[@class="add-link"]'
    _add_payment_methods = 'xpath=.//*[@class="add-payment-cta"]'

    @property
    def add_payment_methods(self):
        return self._find_element_by_selector(selector=self._add_payment_methods, context=self._we)

    @property
    def back_button(self):
        return self._find_element_by_selector(selector=self._back_btn, context=self._we)

    @property
    def add_new_card(self):
        return self._find_element_by_selector(selector=self._add_card, context=self._we)

    @property
    def deposit_title(self):
        return self._find_element_by_selector(selector=self._deposit_title, context=self._we)

    @property
    def deposit_sub_title(self):
        return self._find_element_by_selector(selector=self._deposit_sub_title, context=self._we)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)


class GVCDepositIframeBase(GVCDepositContent):
    _iframe = 'xpath=.//iframe[contains(@class, "quick_deposit__iframe")] | .//iframe'
    _close_button = 'xpath=.//*[contains(@class, "close-button") or contains(@class, "ui-close")]'
    _content = 'xpath=.//div[contains(@class,"main-deposit-block")]'
    _amount = 'xpath=.//*[@id="userAmount"]'
    _cvv = 'xpath=.//*[@id="cvv2"]'
    _deposit = 'xpath=.//*[@id="btnSubmitDeposit"]'

    @property
    def amount(self):
        return InputBase(selector=self._amount)

    @property
    def cvv(self):
        return InputBase(selector=self._cvv)

    @property
    def deposit_btn(self):
        return ButtonBase(selector=self._deposit)

    def wait_for_content(self, timeout=10, expected_result=True):
        return wait_for_result(lambda: ComponentBase(selector=self._content, context=get_driver(), timeout=0).is_displayed(timeout=0),
                               name=f'Iframe content loading state to be {expected_result}',
                               bypass_exceptions=VoltronException,
                               expected_result=expected_result,
                               timeout=timeout)

    def stick_to_iframe(self, timeout=10):
        switch_to_iframe(self._iframe, timeout=timeout)
        self.wait_for_content(timeout=timeout)
        return self

    @staticmethod
    def switch_to_main_page():
        switch_to_main_page()
