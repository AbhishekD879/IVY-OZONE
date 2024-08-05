import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2297656_Verify_showing_Upgrade_your_account_dialog_for_the_in_shop_users_first_login_only(Common):
    """
    TR_ID: C2297656
    NAME: Verify showing 'Upgrade your account' dialog for the in-shop user's first login only
    DESCRIPTION: This test case verifies showing upgrade dialog for first login only
    DESCRIPTION: To emulate the first log in for existing user: clean Local Storage and Cookies
    DESCRIPTION: In-shop user: 5000000000979448/ 1234
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: Load SB app
    """
    keep_browser_open = True

    def test_001_log_in_with_in_shop_user_for_the_first_time_with_card_number_and_pin(self):
        """
        DESCRIPTION: Log in with In-Shop user for the first time (with Card number and PIN)
        EXPECTED: * User is logged in
        EXPECTED: * Upgrade dialog is shown
        """
        pass

    def test_002_tap_close_button_x(self):
        """
        DESCRIPTION: Tap close button 'X'
        EXPECTED: The upgrade dialog has been closed
        """
        pass

    def test_003_log_out_of_the_app(self):
        """
        DESCRIPTION: Log out of the app
        EXPECTED: A user is logged out
        """
        pass

    def test_004_log_in_with_the_same_in_shop_user(self):
        """
        DESCRIPTION: Log in with the same in-shop user
        EXPECTED: The upgrade dialog box hasn't appeared
        """
        pass
