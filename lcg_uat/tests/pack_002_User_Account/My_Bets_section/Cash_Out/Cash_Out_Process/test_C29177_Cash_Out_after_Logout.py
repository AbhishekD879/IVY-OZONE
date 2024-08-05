import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.user_account
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.cash_out
@pytest.mark.medium
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29177_Cash_Out_after_Logout(BaseUserAccountTest, BaseCashOutTest):
    """
    TR_ID: C29177
    NAME: Cash Out after Logout
    DESCRIPTION: This test scenario verifies that user is logged out by server automatically when his/her session is over on the server.
    """
    keep_browser_open = True

    def test_001_make_steps_from_preconditions(self):
        """
        DESCRIPTION: User should be logged in, but session should be OVER on the server
        DESCRIPTION: User has placed a bet on Pre Match or In-Play match (Singles and Multiple bets) where Cash Out and Partial Cash Out offers are available (on SS see cashoutAvail="Y" on Event and Market level to be sure whether COMB option is available).
        DESCRIPTION: To trigger event when session is over on the server please perform the following steps:
        DESCRIPTION: Login to Oxygen in one browser tab, open 'Cash Out' tab
        DESCRIPTION: Login to Oxygen in second browser tab, logout -> session is over on the server
        DESCRIPTION: Navigate back to the first browser tab where user is still logged in, however there is no active session already
        """
        event = self.ob_config.add_autotest_premier_league_football_event(cashout=True)

        username = tests.settings.betplacement_user
        self.site.login(username=username)
        self.open_betslip_with_selections(event.selection_ids[event.team1])
        self.place_single_bet()
        self.site.bet_receipt.close_button.click()

        self.site.open_my_bets_cashout()
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No bets found on Cashout page')

        self.logout_in_new_tab()

    def test_002_verify_cash_out_page(self):
        """
        DESCRIPTION: Verify 'Cash Out' page
        EXPECTED: Popup message about logging out appears.
        EXPECTED: User is logged out from the application performing any actions
        EXPECTED: User is not able to see Cash Out bet lines and to perform Cash Out operations
        EXPECTED: User is redirected to the Homepage
        """
        self.verify_logged_out_state()
