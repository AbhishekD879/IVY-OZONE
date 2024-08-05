import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.extra_place_icon
@pytest.mark.open_bets
@pytest.mark.bet_history
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.slow
@pytest.mark.bet_history_open_bets
@pytest.mark.login
@vtest
class Test_C2644241_Verify_Extra_Place_Icon_for_Single_Bet_on_OpenBets_BetHistory_Tabs(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C2644241
    NAME: Verify Extra Place icon for Single Bet on OpenBets/Settled Bets tabs
    DESCRIPTION: This test case verifies that the Extra Place icon for Single Bet is displayed on the OpenBets/Settled Bets tabs
    PRECONDITIONS: Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: USER is logged in
    PRECONDITIONS: - Extra Place promo is available for <Race> event on Market level, User has placed Single bet on this market
    PRECONDITIONS: - Extra Place promo is available for <Race> event on Market level, User has placed Single bet on this market and this **MARKET IS SETTLED**
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Signposting toggle is Turn ON in the CMS
        DESCRIPTION: User is logged in
        DESCRIPTION: Extra Place promo is available for <Race> event on Market level, User has placed Single bet on this market
        """
        event = self.ob_config.add_UK_racing_event(market_extra_place_race=True)

        self.__class__.selection_ids = [list(event.selection_ids.values())[0]]
        self.__class__.selections = [list(event.selection_ids.keys())[0]]
        self.__class__.event_id = event.event_id
        self.__class__.market_id = self.ob_config.market_ids[self.event_id]

        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()

    def test_001_navigate_to_the_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to the **Open Bets tab**
        EXPECTED: * Open Bets tab is opened
        EXPECTED: * Single bets from precondition are presents on OpenBet tab
        """
        self.site.open_my_bets_open_bets()
        self.__class__.bet_legs = self.verify_selections_displayed(tab=self.site.open_bets,
                                                                   selections=self.selections)

    def test_002_verify_extra_place_icon_on_the_single_bet_for_event_with_extra_place_promo_available_on_market_level(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the Single bet for event with Extra Place promo available on **Market level**
        EXPECTED: * 'Extra Place' icon and label are displayed between event name and Stake info
        EXPECTED: * 'Extra Place' icon and label are aligned to the left
        """
        self.verify_extra_place_icon_displayed(bet_leg=self.bet_legs[self.selections[0]])

    def test_003_navigate_to_the_settled_bets_tab(self):
        """
        DESCRIPTION: Navigate to the **Settled Bets tab**
        EXPECTED: * Settled Bets tab is opened
        EXPECTED: * **SETTLED** Single bets from precondition are presents on Settled Bets tab
        """
        # Result even to check Settled Bets tab
        self.result_event(selection_ids=self.selection_ids, market_id=self.market_id, event_id=self.event_id)
        self.site.open_my_bets_settled_bets()
        self.__class__.bet_legs = self.verify_selections_displayed(tab=self.site.bet_history,
                                                                   selections=self.selections)

    def test_004_verify_extra_place_icon_on_the_single_bet_for_event_with_extra_place_promo_available_on_market_level(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the Single bet for event with Extra Place promo available on **Market level**
        EXPECTED: * 'Extra Place' icon and label are displayed between event name and Stake info
        EXPECTED: * 'Extra Place' icon and label are aligned to the left
        """
        self.test_002_verify_extra_place_icon_on_the_single_bet_for_event_with_extra_place_promo_available_on_market_level()
