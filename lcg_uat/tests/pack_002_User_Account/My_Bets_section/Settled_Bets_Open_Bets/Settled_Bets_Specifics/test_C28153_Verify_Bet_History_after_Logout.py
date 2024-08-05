import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.user_account
@pytest.mark.bet_history
@pytest.mark.bet_history_open_bets
@pytest.mark.portal_dependant
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.login
@vtest
class Test_C28153_Verify_Bet_History_after_Logout(BaseUserAccountTest):
    """
    TR_ID: C28153
    NAME: Verify Settled Bets after Logout
    """
    keep_browser_open = True

    def test_001_make_steps_from_preconditions(self):
        """
        DESCRIPTION:
        EXPECTED: User should be logged in, but session should be OVER on the server
        EXPECTED: To trigger event when session is over on the server please perform the following steps:
        EXPECTED: Login to Invictus in one browser tab and open 'Settled Bets' tab (on 'My Bets' page/'Bet Slip' widget)
        EXPECTED: Login to Invictus in second browser tab, logout -> session is over on the server
        EXPECTED: Navigate back to the first browser tab where user is still logged in, however there is no active session already
        """
        self.site.login(async_close_dialogs=False)
        self.site.open_my_bets_settled_bets()

        self.logout_in_new_tab()

    def test_002_verify_bet_history_page(self):
        """
        DESCRIPTION: Verify 'Settled Bets' page
        EXPECTED: * User is logged out from the application without performing any action
        EXPECTED: * User is not able to see the content of 'Settled Bets' tab
        EXPECTED: * User is redirected to the Homepage
        """
        self.verify_logged_out_state()
