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
class Test_C832561_Auto_login_when_moving_from_the_GCI_Casino_to_the_Oxygen_app(Common):
    """
    TR_ID: C832561
    NAME: Auto-login when moving from the GCI Casino to the Oxygen app
    DESCRIPTION: This test case verifies moving of the automatically logged user from the GCI Casino to Oxygen application.
    DESCRIPTION: Note: logged user should be under the global domain – coral.co.uk, not under the specific sub-domain
    PRECONDITIONS: If the cookies exist and contain values then the Oxygen should make an OpenAPI login request (33036) using an existing Session Token.
    PRECONDITIONS: Check for the existence of the following cookies:
    PRECONDITIONS: **sportsbookToken** - the temp token received from OpenAPI’s login response
    PRECONDITIONS: **sportsbookUsername** - the username of logged in user
    PRECONDITIONS: **userLoginTime** - the login successful timestamp (in UNIX)
    PRECONDITIONS: If the cookies don't exist or have no values then follow the standard login process using the login form.
    """
    keep_browser_open = True

    def test_001_open_gci_casino(self):
        """
        DESCRIPTION: Open GCI Casino
        EXPECTED: 
        """
        pass

    def test_002_log_in_with_valid_credentials(self):
        """
        DESCRIPTION: Log in with valid credentials
        EXPECTED: 
        """
        pass

    def test_003_proceed_to_oxygen_applicationvia_direct_link_or_by_pressing_on_appropriate_button(self):
        """
        DESCRIPTION: Proceed to Oxygen application
        DESCRIPTION: (via direct link or by pressing on appropriate button)
        EXPECTED: The user is automatically logged into the Oxygen application with the same credentials
        """
        pass
