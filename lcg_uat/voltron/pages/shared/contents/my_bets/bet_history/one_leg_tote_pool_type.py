from voltron.pages.shared.components.bet_receipt_info import BetReceiptInfo
from voltron.pages.shared.contents.my_bets.cashout import BetDetails
from voltron.pages.shared.contents.my_bets.open_bets.open_bets_one_leg_pool import OneLegTotePool
from voltron.utils.waiters import wait_for_result


class BetHistoryOneLegTotePool(OneLegTotePool):
    # _bet_receipt_info = 'xpath=.//*[@data-crlat="betReceiptInfo"]'
    _bet_receipt_info = 'xpath=.//*[contains(@class,"betDetailsAccordion-lads")] | .//*[contains(@class,"betDetailsAccordion-coral")]/*[@data-crlat="accordion"]'

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
