from voltron.pages.shared.components.bet_receipt_info import BetReceiptInfo
from voltron.pages.shared.contents.my_bets.cashout import BetDetails
from voltron.pages.shared.contents.my_bets.open_bets.open_bets import OpenBet
from voltron.utils.waiters import wait_for_result


class BetHistoryOpenBet(OpenBet):
    # _bet_receipt_info = 'xpath=.//*[@data-crlat="betReceiptInfo"]'
    _bet_receipt_info = 'xpath=.//*[contains(@class,"betDetailsAccordion-lads")] | .//*[contains(@class,"betDetailsAccordion-coral")]/*[@data-crlat="accordion"]'
    _extra_bog = 'xpath=.//*[contains(@class, "bog-extra-earnings-label")]'

    @property
    def extra_bog(self):
        return self._get_webelement_text(selector=self._extra_bog)

    @property
    def bet_receipt_info(self):
        if not self.bet_details.is_expanded():
            self.bet_details.chevron_arrow.click()
            wait_for_result(lambda: self.bet_details.is_expanded is True,
                            name='Bet Details Expanded',
                            expected_result=True,
                            timeout=10)
        return BetDetails(selector=self._bet_receipt_info, context=self._we)
        # return BetReceiptInfo(selector=self._bet_receipt_info, context=self._we)
