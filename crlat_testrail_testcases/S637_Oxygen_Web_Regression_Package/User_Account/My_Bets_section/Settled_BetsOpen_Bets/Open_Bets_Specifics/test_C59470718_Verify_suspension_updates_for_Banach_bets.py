import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C59470718_Verify_suspension_updates_for_Banach_bets(Common):
    """
    TR_ID: C59470718
    NAME: Verify suspension updates for Banach bets
    DESCRIPTION: This test case verifies that only Event (sEVENT) level suspension updates are displayed on UI for open Banach (BYB/5-A-Side/Bet Builder) bets
    PRECONDITIONS: 0. User is logged in and have placed Banach bet(s) with 2 or more different markets/selections
    PRECONDITIONS: 1. Updates have to be tested on all levels: Event (sEVENT) / Market (sEVMKT) / Selection (sSELCN)
    PRECONDITIONS: 2. We receive statuses from:
    PRECONDITIONS: - current state and details of Bet from Cashout MS (EventStream) - when we open Open Bets page
    PRECONDITIONS: - current state of selections by making request to SiteServer for selections(outcomes) which we have in Open Bets
    PRECONDITIONS: - subscribing and receiving updates from LiveServ MS (websocket)
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_page(self):
        """
        DESCRIPTION: Navigate to Open Bets page
        EXPECTED: - Banach bet(s) details displayed
        EXPECTED: - Bet is active
        """
        pass

    def test_002___in_ti_trigger_suspensionun_suspension_on_event_level_that_is_present_in_banach_bet__validate_ui_behaviour(self):
        """
        DESCRIPTION: - In TI trigger suspension/un-suspension on event level that is present in Banach bet
        DESCRIPTION: - Validate UI behaviour
        EXPECTED: Bet is displayed as Suspended/Active each time corresponding update is received from LiveServ MS
        """
        pass

    def test_003___in_ti_trigger_suspensionun_suspension_on_selectionmarket_levels_one_by_one_for_all_selections_and_markets_that_is_present_in_banach_bet__validate_ui_behaviour(self):
        """
        DESCRIPTION: - In TI trigger suspension/un-suspension on selection/market levels one by one for ALL selection(s) and market(s) that is present in Banach bet
        DESCRIPTION: - Validate UI behaviour
        EXPECTED: UI does not change event status if update for Market/Selection is received from LiveServ MS
        """
        pass
