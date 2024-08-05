import voltron.environments.constants as vec
import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.open_bets
@pytest.mark.bet_history_open_bets
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29210_Verify_Open_Bets_tab_when_user_is_logged_out(BaseBetSlipTest):
    """
    TR_ID: C29210
    VOL_ID: C18352512
    NAME: Verify 'Open Bets' tab when user is logged out
    DESCRIPTION: This test case verifies 'Open Bets' tab when the user is logged out.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen application, navigate to 'Open Bets' tab
        EXPECTED: "****Please log in to see your Open Bets." message is displayed
        EXPECTED: 'Log In' button is shown below the message
        """
        self.navigate_to_page(name='open-bets')
        self.site.wait_content_state('OpenBets')
        open_bets = self.site.open_bets.tab_content
        self.assertTrue(open_bets.please_login_text, msg='"Please login" text is not shown')
        self.assertEqual(open_bets.please_login_text, vec.bet_history.OPEN_BETS_PLEASE_LOGIN_MESSAGE)
        if self.brand != 'ladbrokes':
            self.assertTrue(open_bets.has_login_button(), msg='"Log In" button is not shown')

    def test_002_log_in_from_open_bets_tab(self):
        """
        DESCRIPTION: Log in from 'Open Bets' tab
        EXPECTED: User is logged in
        EXPECTED: Content of page is visible
        """
        if self.brand != 'ladbrokes':
            self.site.open_bets.tab_content.login_button.click()
            self.site.login(username=tests.settings.betplacement_user, timeout_wait_for_dialog=2)
            self.assertTrue(self.site.open_bets.tab_content.accordions_list,
                            msg='Open Bets content is not visible after login')
