import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870163_Check_user_sees_message_as_Please_log_in_to_see_your_Cash_Out_bets_when_not_logged_in_to_system_and_on_Betslip__Cashout_section_Log_in_button_is_available(Common):
    """
    TR_ID: C44870163
    NAME: Check user sees message as 'Please log in to see your Cash Out bets.' when not logged in to system and on Betslip -> Cashout section. Log in button is available
    DESCRIPTION: Check user sees message as 'Please log in to see your Cash Out bets.' when not logged in to system and on Betslip -> Cashout section. Log in button is available
    PRECONDITIONS: User not logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_my_bets_section____cashout_tab(self):
        """
        DESCRIPTION: Navigate to My Bets section --> Cashout Tab
        EXPECTED: User navigated to Cashout tab
        """
        pass

    def test_003_verify__please_login_to_see_your_cash_out_bets_message_once_user_navigated_to_cashout_tab(self):
        """
        DESCRIPTION: Verify  'Please login to see your Cash Out bets message once user navigated to cashout tab
        EXPECTED: Message is displayed
        """
        pass

    def test_004_verify_login_button_available_and_use_can_log_in_to_view_cashout_tab(self):
        """
        DESCRIPTION: Verify Login button available and use can log in to view cashout tab
        EXPECTED: User logs in to cashout tab
        """
        pass
