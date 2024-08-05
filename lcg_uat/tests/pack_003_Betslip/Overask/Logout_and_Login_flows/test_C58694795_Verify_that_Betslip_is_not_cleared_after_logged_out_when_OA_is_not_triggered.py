import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create events
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C58694795_Verify_that_Betslip_is_not_cleared_after_logged_out_when_OA_is_not_triggered(BaseBetSlipTest):
    """
    TR_ID: C58694795
    NAME: Verify that Betslip is not cleared after logged out when OA is not triggered
    DESCRIPTION: This test case verifies that Betslip is not cleared after user is logged out when OA is not triggered
    PRECONDITIONS: Overask is enabled for User1 and for event which will be added to Betslip (see doc: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983)
    PRECONDITIONS: 1. Login with User1 (without 'Remember Me' option) and add selection available for Overask to Betslip
    PRECONDITIONS: Check parameters in Local Storage:
    PRECONDITIONS: OX.BetSelections
    PRECONDITIONS: ![](index.php?/attachments/get/106948322)
    """
    keep_browser_open = True
    max_bet = 0.05

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        """
        event_params_1 = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
        selection_id = list(event_params_1.selection_ids.values())[0]
        self.__class__.selection_name = event_params_1.team1

        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        self.open_betslip_with_selections(selection_ids=selection_id)

    def test_001_trigger_log_out_from_appon_desktop_tap_logout_button_in_account_menuon_web_mobile_refresh_page_then_tap_logout_button_in_the_account_menuon_wrappers_kill_and_reopen_the_app(self):
        """
        DESCRIPTION: Trigger log out from app:
        DESCRIPTION: On Desktop: Tap 'Logout' button in account menu
        DESCRIPTION: On Web mobile: Refresh page then tap 'Logout' button in the account menu
        DESCRIPTION: On wrappers: Kill and reopen the app
        EXPECTED: - User is logged out
        EXPECTED: - Homepage is shown (for mobile web and wrappers)
        """
        if self.device_type == 'mobile':
            self.device.refresh_page()
            self.site.wait_splash_to_hide(timeout=10)
        self.site.logout(timeout=20)
        self.assertTrue(self.site.wait_logged_out(), msg='User has not logged out!')

    def test_002_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: Selection added in preconditions is shown in Betslip
        """
        self.site.open_betslip()
        sections = self.get_betslip_sections().Singles
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        self.assertIn(self.selection_name, sections,
                      msg=f'Added selection "{self.selection_name}" is not present in Betslip sections "{sections}"')

    def test_003_check_local_storage(self):
        """
        DESCRIPTION: Check Local Storage
        EXPECTED: OX.BetSelections is NOT cleared
        """
        key_value1 = self.get_local_storage_cookie_value_as_dict('OX.betSelections')
        self.assertTrue(key_value1, msg=f'Value of cookie "OX.BetSelections" is blank')

    def test_004_tap_login_buttonlogin_with_user1_from_preconditions(self):
        """
        DESCRIPTION: Tap 'Login' button
        DESCRIPTION: Login with user1 from preconditions
        EXPECTED: - User is logged in
        EXPECTED: - Selection added in preconditions is shown in Betslip
        """
        if self.device_type == 'mobile':
            self.device.refresh_page()
            self.site.wait_splash_to_hide(timeout=10)
        self.site.login(username=self.username)
        self.assertTrue(self.site.wait_logged_in(timeout=1), msg='User is not logged in')
        self.site.open_betslip()
        sections = self.get_betslip_sections().Singles
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        self.assertIn(self.selection_name, sections,
                      msg=f'Added selection "{self.selection_name}" is not present in Betslip sections "{sections}"')
