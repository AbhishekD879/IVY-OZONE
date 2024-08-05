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
class Test_C59150044_Verify_recreation_of_bet_details_connection_after_succesful_full_cashout_with_bet_updates_meanwhile(Common):
    """
    TR_ID: C59150044
    NAME: Verify recreation of  bet-details connection after succesful full cashout with bet updates meanwhile
    DESCRIPTION: This test case verifies the successful recreation of bet-details connection after successful full cashout and receiving bet/cashout updates in the same time.
    DESCRIPTION: Note: After release BMA-51071 - no New bet-details connection will be created,  "updateBet" message with betId after successful full cashout is sent to CashoutMS to remove bet from memory and stop handling Saf updates for bet.
    PRECONDITIONS: Actual from Release 103 for both brands according to https://jira.egalacoral.com/browse/BMA-53741
    PRECONDITIONS: New Cashout is enabled in CMS: (System config -> Cashout-> 'isV4Enabled') **From version XXX.XX (according to BMA-55051): toggle should be deleted**
    PRECONDITIONS: OB TIs:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+OpenBet+System
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User is on Cashout/Open Bets tabs
    PRECONDITIONS: - User has placed single/multiple bets with cashout available
    PRECONDITIONS: - 'EventStream connection' is created to Cash Out MS in 'bet-details' request
    PRECONDITIONS: **From release XXX.XX:**
    PRECONDITIONS: * WS connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: * initial bets data will be returned after establishing connection
    """
    keep_browser_open = True

    def test_001_click_on_cashout_button_on_any_bet_singlemultiple(self):
        """
        DESCRIPTION: Click on 'Cashout' button on any bet (single/multiple)
        EXPECTED: - Full cashout is triggered
        """
        pass

    def test_002_hange_price_in_ti_for_the_given_bet_or_set_suspended_status(self):
        """
        DESCRIPTION: Сhange price in TI for the given bet or set suspended status
        EXPECTED: * Full cashout is susccessful
        EXPECTED: * Bet is displayed as cashed out and stays displayed in this state
        EXPECTED: * after successful full cashout old connection to Cashout MS should be closed and new one should be established to update bets states
        EXPECTED: * no requests to BPP getBetDetails and getBetDetail should be performed on cashout page
        EXPECTED: * only one current connection to cashout MS should be active on cashout page
        EXPECTED: After release BMA-51071:
        EXPECTED: * No new Cashout MS is created
        EXPECTED: * "updateBet" message with betId is received
        EXPECTED: * No price updates are received for this bet
        EXPECTED: * Updates for other bets still received by this Cashout MS connection
        """
        pass

    def test_003_in_ti_trigger_bet_update_price_changesuspend_again_for_any_other_bet_and_check_the_connection(self):
        """
        DESCRIPTION: In TI trigger bet update (price change/suspend) again for any other bet and check the connection
        EXPECTED: - No new EventStream connection is created
        EXPECTED: - Updates like cashout/bet updates are received in same active 'bet-details' connection
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Cashout MS will send betUpdate message with an updated bet after event/market/selection update
        EXPECTED: * Cashout MS will send cashoutUpdate message with updated cashout value after price update
        """
        pass

    def test_004_repeat_steps_above_for_the_open_betscashout_tabs_in_widgetsdesktop(self):
        """
        DESCRIPTION: Repeat steps above for the Open bets/Cashout tabs in widgets/desktop
        EXPECTED: Results are the same
        EXPECTED: Note: each time user opens the Cashout/Open Bets page or widget new 'bet-details' connection is created to cashout MS.
        EXPECTED: **From release XXX.XX**
        EXPECTED: * Results are the same
        EXPECTED: * WS connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
        """
        pass
