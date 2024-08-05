from voltron.pages.shared.components.byb_betslip import BYBBetslip
from voltron.pages.shared.components.quick_bet_quick_deposit_panel import GVCQuickDeposit


class CoralBYBBetslip(BYBBetslip):
    _info_panel = 'xpath=.//div[contains(@class,"qb-info-panel")]'

    @property
    def quick_deposit_panel(self):
        return GVCQuickDeposit(selector=self._quick_deposit_panel, context=self._we, timeout=2)
