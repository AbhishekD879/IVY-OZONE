from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import switch_to_iframe, switch_to_main_page
from voltron.utils.waiters import wait_for_result


class QuickDepositButton(ButtonBase):

    def _wait_active(self, timeout=0):
        self._we = self._find_myself(timeout=2)
        wait_for_result(lambda: self._we.is_displayed(),
                        name=f'{self.__class__.__name__} button is displayed',
                        timeout=5)


class QuickDepositDesktop(ComponentBase):
    _amount = 'xpath=.//*[@id="userAmount"]'
    _cvv = 'xpath=.//*[@id="cvv2"]'
    _deposit = 'xpath=.//*[@id="btnSubmitDeposit"]'
    _iframe = 'xpath=//vn-cashier-iframe//iframe'

    @property
    def amount(self):
        return InputBase(selector=self._amount)

    @property
    def cvv(self):
        return InputBase(selector=self._cvv)

    @property
    def deposit_btn(self):
        return ButtonBase(selector=self._deposit)

    def stick_to_iframe(self, timeout=10):
        switch_to_iframe(self._iframe, timeout=timeout)
        # self.wait_for_content(timeout=timeout)
        return self

    def wait_for_content(self, timeout=10, expected_result=True):
        return wait_for_result(
            lambda: ComponentBase(selector=self._content, context=get_driver(), timeout=0).is_displayed(timeout=0),
            name=f'Iframe content loading state to be {expected_result}',
            bypass_exceptions=VoltronException,
            expected_result=expected_result,
            timeout=timeout)

    @staticmethod
    def switch_to_main_page():
        switch_to_main_page()
