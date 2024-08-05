import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.liveserv_updates
@pytest.mark.high
@pytest.mark.safari
@pytest.mark.desktop
@vtest
class Test_C29049_Bet_Placement_Stake_Error(BaseBetSlipTest):
    """
    TR_ID: C29049
    VOL_ID: C9697731
    NAME: Place a Bet when user is Logged in but stake errors appears
    """
    keep_browser_open = True
    selection_id = None
    dialog = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.__class__.selection_ids1 = self.ob_config.add_autotest_premier_league_football_event().selection_ids

    def test_001_open_betslip_via_deep_link(self):
        """
        DESCRIPTION: Open betslip via deeplink
        """
        self.__class__.selection_id = self.selection_ids['Draw']
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()

    def test_002_verify_login_dialog_appears(self):
        """
        DESCRIPTION: Check if login dialog shows up
        EXPECTED: Check if you are still on BetSlip page
        """
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg='No login dialog present on page')

    def test_003_use_betplacement_user_to_login(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and **NO** pop-ups are expected after login
        DESCRIPTION: Tap 'Log In and Place Bet' and right after that trigger error occurrence (e.g. suspension, price change)
        EXPECTED: Bet placement process starts automatically after login, however it is interrupted by corresponding message about error
        EXPECTED: Betslip is NOT refreshed
        EXPECTED: Bet is not placed
        EXPECTED: User needs to make changes in the Betslip to be able to place a bet
        EXPECTED: After user will deal with error then **'Bet Now' button** will be enabled within Betslip
        """
        self.dialog.username = tests.settings.betplacement_user
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login(spinner_wait=False)
        self.dialog.wait_dialog_closed()
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)
        self.site.close_all_dialogs(async_close=False)

        page_title = self.get_betslip_content().betslip_title.upper()
        expected_bet_slip_page_title = self.expected_bet_slip_page_title.title().upper()
        self.assertEqual(page_title, expected_bet_slip_page_title,
                         msg=f'Page title "{page_title}" doesn\'t match expected text "{expected_bet_slip_page_title}"')
        betslip_sections = self.get_betslip_content().betslip_sections_list
        self.assertTrue(betslip_sections, msg='*** No bets found in BetSlip')
        btn_enabled = self.get_betslip_content().bet_now_button.is_enabled(expected_result=False)
        self.assertFalse(btn_enabled, msg='Bet Now button is not disabled')

        stake = self.get_betslip_sections().Singles.values()[0]
        self.assertTrue(stake.is_suspended(), msg='Stake is not suspended')

    def test_004_go_to_the_betslip_multiples_section(self):
        """
        DESCRIPTION: Go to the Betslip -> 'Multiples' section
        EXPECTED: Betslip is opened
        EXPECTED: Added multiple selections are present
        """
        self.site.close_betslip()
        self.site.logout()
        self.site.wait_content_state_changed()
        self.site.open_betslip()
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=True)
        self.open_betslip_with_selections(selection_ids=self.selection_ids1['Draw'])
        self.place_multiple_bet()
        self.test_002_verify_login_dialog_appears()
        self.test_003_use_betplacement_user_to_login()
