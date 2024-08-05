from voltron.pages.shared.components.quick_bet_betslip_panel import QuickDeposit
from voltron.pages.shared.contents.betslip.quick_deposit_payment_dropdown import PaymentAccountDropDown


class QuickDepositLadbrokes(QuickDeposit):
    _payment_account_dropdown = 'xpath=.//*[@data-crlat="paymentAccounts"]'
    _payment_account_type = PaymentAccountDropDown

    @property
    def payment_account_dropdown(self):
        dropdown_we = self._find_element_by_selector(selector=self._payment_account_dropdown, context=self._we, timeout=1)
        return self._payment_account_type(web_element=dropdown_we)
