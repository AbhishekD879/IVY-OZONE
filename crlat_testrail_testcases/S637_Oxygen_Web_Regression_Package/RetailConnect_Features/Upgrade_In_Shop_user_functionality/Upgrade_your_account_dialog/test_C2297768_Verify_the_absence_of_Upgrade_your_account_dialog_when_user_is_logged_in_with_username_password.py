import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2297768_Verify_the_absence_of_Upgrade_your_account_dialog_when_user_is_logged_in_with_username_password(Common):
    """
    TR_ID: C2297768
    NAME: Verify the absence of 'Upgrade your account' dialog when user is logged in with username/password
    DESCRIPTION: This test case verifies the absence of upgrade dialog for not in-shop user's first login
    DESCRIPTION: Online user: digital account registered in SB, has username and password
    DESCRIPTION: Multi-channel user: has online account in SB (username and password) and Connect card number (Card number and PIN) (you can use: bluerabbit/ password)
    DESCRIPTION: To upgrade your online user to multi-channel:
    DESCRIPTION: * Download attached postman collection
    DESCRIPTION: * Run get_token request
    DESCRIPTION: * Run Upgrade Online to MC request: set username with valid username of existing online user; set mobile with phone number of this user
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    """
    keep_browser_open = True

    def test_001_log_in_under_the_online_user_for_the_first_time_with_username_and_password(self):
        """
        DESCRIPTION: Log in under the online user for the first time (with username and password)
        EXPECTED: * User is logged in
        EXPECTED: * The upgrade dialog box hasn't appeared
        """
        pass

    def test_002_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: A user is logged out
        """
        pass

    def test_003_log_in_under_the_multichannel_user_for_the_first_time_with_username_and_password(self):
        """
        DESCRIPTION: Log in under the multichannel user for the first time (with username and password)
        EXPECTED: * User is logged in
        EXPECTED: * The upgrade dialog box hasn't appeared
        """
        pass
