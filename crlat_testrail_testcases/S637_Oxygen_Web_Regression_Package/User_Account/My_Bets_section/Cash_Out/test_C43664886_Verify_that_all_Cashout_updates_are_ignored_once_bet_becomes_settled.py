import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C43664886_Verify_that_all_Cashout_updates_are_ignored_once_bet_becomes_settled(Common):
    """
    TR_ID: C43664886
    NAME: Verify that all Cashout updates are ignored once bet becomes settled
    DESCRIPTION: This test case verified that there are no updates in Cashout EventStream (cashout V4) when bet becomes settled
    DESCRIPTION: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    DESCRIPTION: - WS connection to Cashout MS is created when user lands on myBets page
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User have at least one open bet (Single / Multiple)
    PRECONDITIONS: - Cashout isV4Enabled = true in system-configuration/structure
    PRECONDITIONS: NB! CMS config will be removed when [BMA-55051 [OxygenUI] Remove support of old cashout flow][1] is released
    PRECONDITIONS: [1]:https://jira.egalacoral.com/browse/BMA-55051
    """
    keep_browser_open = True

    def test_001___navigate_to_open_bets__in_devtools_open_cashout_eventstream_requestfrom_release_xxxxxin_devtools_open_websocket_connection_to_cashout_ms(self):
        """
        DESCRIPTION: - Navigate to Open Bets
        DESCRIPTION: - In Devtools open Cashout EventStream request
        DESCRIPTION: **From release XXX.XX:**
        DESCRIPTION: In Devtools open Websocket connection to Cashout MS
        EXPECTED: - Open Bets are displayed
        EXPECTED: - In Cashout EventStream within "initial" type we received Data for open bet (selection) from preconditions
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * WebSocket connection to Cashout MS is created
        EXPECTED: * Within "initial" type we received Data for open bet (selection) from preconditions
        """
        pass

    def test_002_in_ti_settle_marketselections_on_which_you_have_placed_bet(self):
        """
        DESCRIPTION: In TI settle market(selections) on which you have placed bet
        EXPECTED: - Bet is settled (Win/Lose icon appeared)
        EXPECTED: - betUpdate is received from Cashout MS
        """
        pass

    def test_003_in_ti_make_updates_pricestatusdisplay_changes_on_settled_marketeventselection_levels(self):
        """
        DESCRIPTION: In TI make updates (price/status/display changes) on settled market/event/selection levels
        EXPECTED: No updates are received from Cashout MS
        """
        pass

    def test_004_repeat_steps_1_3_for_multiple_bet_where_at_least_1_legselection_is_lost(self):
        """
        DESCRIPTION: Repeat steps 1-3 for Multiple bet where at least 1 leg(selection) is lost
        EXPECTED: No updates are received from Cashout MS
        """
        pass
