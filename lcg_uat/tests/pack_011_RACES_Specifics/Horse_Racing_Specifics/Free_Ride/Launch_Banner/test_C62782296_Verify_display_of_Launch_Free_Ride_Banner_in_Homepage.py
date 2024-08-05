import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod # Cannot grant free ride in prod env
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.races
@pytest.mark.free_ride
@vtest
class Test_C62782296_Verify_display_of_Launch_Free_Ride_Banner_in_Homepage(Common):
    """
    TR_ID: C62782296
    NAME: Verify display of Launch Free Ride Banner in Homepage
    DESCRIPTION: This test case verifies display of  free ride banner in homepage of the application
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Qualified customer details are uploaded in Opti move /OB. (TBC)
        """
        username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=username)
        self.update_spotlight_events_price(class_id=223)
        self.cms_config.check_update_and_create_freeride_campaign()
        self.site.login(username=username)

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to ladbrokes application
        EXPECTED: * User should be able to login successfully
        """
        # covered in above step

    def test_002_verify_display_of_launch_Banner(self):
        """
        DESCRIPTION: Verify display of Launch Banner
        EXPECTED: Free Ride Launch Banner should displayed in the homepage as below:
        Mobile - Launch banner should be displayed as Inline banner
        Desktop: Launch banner should be displayed as Inline banner just below the 'Today' tab.
        """
        launch_banner = self.site.home.free_ride_banner()
        self.assertTrue(launch_banner, msg="Launch banner is not displayed")

    def test_003_logout_from_the_application(self):
        """
        DESCRIPTION: Logout from the application
        EXPECTED: * user should be successfully logged out
        """
        self.site.logout()

    def test_004_login_with_user_credentials_that_are_not_uploaded_in_Optimove(self):
        """
        DESCRIPTION: Login with user credentials that are not uploaded in Optimove
        EXPECTED: * User should successfully login to the application
        EXPECTED: * Launch banner should not be displayed in the homepage
        """
        self.site.login()
        launch_banner = self.site.home.free_ride_banner()
        self.assertFalse(launch_banner, msg="Launch banner is displayed")
