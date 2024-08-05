import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C18258215_Vanilla_Log_in_after_time_out_ends(Common):
    """
    TR_ID: C18258215
    NAME: [Vanilla] Log in after time-out ends
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User was timed-out for selected period of time and that time has ended recently
    """
    keep_browser_open = True

    def test_001_click_on_login_button(self):
        """
        DESCRIPTION: Click on 'LOGIN' button
        EXPECTED: Login popup appears
        """
        pass

    def test_002_log_in_with_credentials_of_a_user_that_was_timed_out_but_time_out_time_has_ended(self):
        """
        DESCRIPTION: Log in with credentials of a user that was timed out but time-out time has ended
        EXPECTED: User is successfully logged in
        """
        pass

    def test_003_verify_deposit_page___click_the_deposit_button_in_header(self):
        """
        DESCRIPTION: Verify deposit page - click the DEPOSIT button in header
        EXPECTED: Deposit page is successfully open
        EXPECTED: ![](index.php?/attachments/get/35957)
        """
        pass

    def test_004_verify_time_out_page__go_to_my_accounts___gambling_controls___account_management___select_the_last_option(self):
        """
        DESCRIPTION: Verify time-out page -
        DESCRIPTION: Go to My Accounts -> Gambling Controls -> Account Management -> Select the last option
        EXPECTED: User sees the time-out page
        """
        pass
