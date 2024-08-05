import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870164_Check_user_sees_message_as_Please_log_in_to_see_your_Open_Bets_when_not_logged_in_to_system_and_on_Betslip__Openebst_section_Log_in_button_is_available(Common):
    """
    TR_ID: C44870164
    NAME: Check user sees message as 'Please log in to see your Open Bets.' when not logged in to system and on Betslip -> Openebst section. Log in button is available
    DESCRIPTION: Check user sees message as 'Please log in to see your Open Bets.' when not logged in to system and on Betslip -> Openebst section. Log in button is available
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_for_desktop_navigate_to_my_bets_section____open_bets_tabfor_mobiletablet_navigate_to_my_bets_open_bets_via_cashout_from_the_footer_menu(self):
        """
        DESCRIPTION: For Desktop: Navigate to My Bets section --> Open Bets tab
        DESCRIPTION: For mobile/tablet: Navigate to 'My Bets'->'Open bets' via 'Cashout' from the Footer menu
        EXPECTED: User navigated to Open Bets tab
        """
        pass

    def test_003_verify_please_login_to_see_your_open_bets_message_once_user_navigated_to_cashout_tab(self):
        """
        DESCRIPTION: Verify 'Please login to see your Open bets message once user navigated to cashout tab
        EXPECTED: Message is displayed
        """
        pass

    def test_004_verify_login_button_available_and_users_can_log_in_to_view_open_bets_tab(self):
        """
        DESCRIPTION: Verify Login button available and users can log in to view Open Bets tab
        EXPECTED: User logs in to Openbets tab and can see all avalibale open bets
        """
        pass
