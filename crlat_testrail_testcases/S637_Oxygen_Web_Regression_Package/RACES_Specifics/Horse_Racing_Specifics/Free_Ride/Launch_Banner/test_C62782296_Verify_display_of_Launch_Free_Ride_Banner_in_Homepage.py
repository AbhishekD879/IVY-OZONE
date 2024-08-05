import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.homepage_featured
@vtest
class Test_C62782296_Verify_display_of_Launch_Free_Ride_Banner_in_Homepage(Common):
    """
    TR_ID: C62782296
    NAME: Verify display of Launch Free Ride Banner in Homepage
    DESCRIPTION: This test case verifies display of  free ride banner in homepage of the application
    PRECONDITIONS: Qualified customer details are uploaded in Opti move /OB. (TBC)
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to ladbrokes application
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_verify_display_of_launch_banner(self):
        """
        DESCRIPTION: Verify display of Launch Banner
        EXPECTED: Free Ride Launch Banner should displayed in the homepage as below:
        EXPECTED: * Mobile - Launch banner should be displayed as Inline banner
        EXPECTED: * Desktop: Launch banner should be displayed as Inline banner just below the 'Today' tab.
        """
        pass

    def test_003_logout_from_the_application(self):
        """
        DESCRIPTION: Logout from the application
        EXPECTED: user should be successfully logged out
        """
        pass

    def test_004_login_with_user_credentials_that_are_not_uploaded_in_optimove(self):
        """
        DESCRIPTION: Login with user credentials that are not uploaded in Optimove
        EXPECTED: * User should successfully login to the application
        EXPECTED: * Launch banner should not be displayed in the homepage
        """
        pass
