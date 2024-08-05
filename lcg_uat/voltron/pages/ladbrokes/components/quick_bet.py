from voltron.pages.ladbrokes.components.byb_betslip import LadbrokesDepositInfoMessage
from voltron.pages.shared.components.quick_bet import QuickBet
from voltron.utils.waiters import wait_for_result


class QuickBetLadbrokes(QuickBet):
    _german_tax_message = 'xpath=.//*[@data-crlat="taxMessage"]'
    _incorrect_bet_amount_warning_message = 'xpath=.//*[@data-crlat="message"]'
    _deposit_info_message = 'xpath=.//*[@data-crlat="infoMessage"]'

    def has_german_tax_message(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._german_tax_message, timeout=0) is not None,
            name=f'"Tax message" message to be "{expected_result}"', expected_result=expected_result,
            timeout=timeout)

    @property
    def german_tax_message_text(self):
        return self._get_webelement_text(selector=self._german_tax_message, timeout=1)

    @property
    def bet_amount_warning_message(self):
        return self._wait_for_not_empty_web_element_text(selector=self._incorrect_bet_amount_warning_message,
                                                         context=self._we, timeout=5)

    def wait_for_deposit_info_panel(self, expected_result=True, timeout=15):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._deposit_info_message, timeout=0) is not None and
                               self._find_element_by_selector(selector=self._deposit_info_message, timeout=0).is_displayed(),
                               name='Quick Bet info panel to be displayed',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def deposit_info_message(self):
        return LadbrokesDepositInfoMessage(selector=self._deposit_info_message, context=self._we, timeout=15)

    def wait_for_deposit_message_to_change(self, previous_message='', timeout=10):
        result = wait_for_result(lambda: self._get_webelement_text(selector=self._deposit_info_message,
                                                                   timeout=0) != previous_message,
                                 name='Waiting for warning text to change',
                                 timeout=timeout,
                                 poll_interval=0.3)
        return result
