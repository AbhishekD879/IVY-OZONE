import re

from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException


class UserHeader(ComponentBase):
    _user_balance = 'xpath=.//*[@data-crlat="betslipBalanceButton"]'
    _user_balance_label = 'xpath=.//*[@data-crlat="labelUserBalance"]'
    _betslip_login_message = 'xpath=.//*[@data-crlat="labelNoLoginUserBalance"]'
    _freebet_icon = 'xpath=.//*[@data-crlat="freeBetIcon"]'

    @property
    def has_user_balance(self):
        return self._find_element_by_selector(selector=self._user_balance, timeout=1) is not None

    @property
    def user_balance_label(self):
        return self._get_webelement_text(selector=self._user_balance_label, context=self._we, timeout=1)

    @property
    def user_balance_amount(self):
        return self._get_webelement_text(selector=self._user_balance, timeout=2)

    @property
    def betslip_login_message(self):
        return self._get_webelement_text(selector=self._betslip_login_message, context=self._we)

    @property
    def parsed_amount(self):
        matched = re.match(u'^(£|\$|€|Kr)([0-9.,]+)$', self.user_balance_amount, re.U)
        if matched is not None and matched.group(2) is not None:
            currency_symbol = matched.group(1)
            amount = float(matched.group(2))
            return currency_symbol, amount
        else:
            raise VoltronException('Failed parsing amount string: "%s"' % self.user_balance_amount)

    @property
    def currency_symbol(self):
        return self.parsed_amount[0]

    @property
    def user_balance(self):
        user_balance = self.parsed_amount[1]
        return user_balance
