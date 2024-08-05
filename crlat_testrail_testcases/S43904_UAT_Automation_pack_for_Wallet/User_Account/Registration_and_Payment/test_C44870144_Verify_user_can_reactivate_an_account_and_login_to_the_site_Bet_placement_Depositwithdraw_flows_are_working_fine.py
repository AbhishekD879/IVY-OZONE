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
class Test_C44870144_Verify_user_can_reactivate_an_account_and_login_to_the_site_Bet_placement_Depositwithdraw_flows_are_working_fine(Common):
    """
    TR_ID: C44870144
    NAME: Verify user can reactivate an account and login to the site. Bet placement, Deposit,withdraw flows are working fine.
    DESCRIPTION: 
    PRECONDITIONS: User's Account is closed (Navigate to Right Menu -> My Account -> select Responsible Gambling item -> Tap/click 'I want to close my Account' link within 'Account Closure' section)
    PRECONDITIONS: User is logged
    PRECONDITIONS: Reactivation' page is opened
    PRECONDITIONS: Only for external works(doesn't work with test users)
    """
    keep_browser_open = True

    def test_001_enter_valid_password_in_password_fieldclicktap_confirm_button(self):
        """
        DESCRIPTION: Enter valid password in 'Password' field
        DESCRIPTION: Click/tap 'CONFIRM' button
        EXPECTED: Accout Reactivation' confirmation pop-up is shown
        EXPECTED: User remains logged in
        """
        pass

    def test_002_verify_the_pop_up_content(self):
        """
        DESCRIPTION: Verify the pop up content
        EXPECTED: Successful Reactivation pop up consists of:
        EXPECTED: Message: 'Your account has been successfully reactivated.'
        EXPECTED: 'OK' button active by default
        """
        pass

    def test_003_clicktap_ok(self):
        """
        DESCRIPTION: Click/tap 'OK'
        EXPECTED: Pop up is closed
        EXPECTED: User remains logged in and navigated to home page
        """
        pass
