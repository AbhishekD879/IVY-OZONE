import pytest
import tests
from tests.Common import Common
from tests.base_test import vtest
import voltron.environments.constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod     # Cannot grant free ride in prod env
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.races
@pytest.mark.free_ride
@vtest
class Test_C62782281_Verify_display_of_Splash_Page_in_FE_as_per_CMS_config(Common):
    """
    TR_ID: C62782281
    NAME: Verify display of Splash Page in FE as per CMS config
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create a campaign and grant free ride for a user
        """
        self.update_spotlight_events_price(class_id=223)
        self.cms_config.check_update_and_create_freeride_campaign()
        self.__class__.free_ride_splash_page = self.cms_config.get_freeride_splash_page()
        username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=username)
        self.site.login(username=username)

    def test_001_click_on_the_launch_banner_for_freeride_in_homepage(self):
        """
        DESCRIPTION: Click on 'Launch Banner' for Free Ride in Homepage
        EXPECTED: * Free Ride Splash page should be displayed
        """
        free_ride_launch_banner = self.site.home.free_ride_banner()
        self.assertTrue(free_ride_launch_banner, msg='Launch banner is not displayed')
        free_ride_launch_banner.click()
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_RIDE, timeout=10, verify_name=False)
        self.assertTrue(self.dialog, msg="Free Ride Splash page is not shown")

    def test_002_verify_the_data_for_Splash_page_welcome_message_TandC_and_button_Title(self):
        """
        DESCRIPTION: Verify the data: Splash page welcome message, T&C and Button Title
        EXPECTED: Data of these fields should be displayed as per the CMS configuration
        """
        cms_welcome_msg = self.free_ride_splash_page['welcomeMsg']
        cms_TandC_text = self.free_ride_splash_page['termsAndConditionHyperLinkText']
        cms_button_text = self.free_ride_splash_page['buttonText']
        welcome_msg = self.dialog.welcome_message
        terms_and_conditions = self.dialog.terms_and_conditions_text
        cta_button = self.dialog.cta_button_text
        self.assertEqual(cms_welcome_msg, welcome_msg,
                         msg=f'Actual msg "{welcome_msg}" is not same as Expected msg "{cms_welcome_msg}"')
        self.assertEqual(cms_TandC_text, terms_and_conditions,
                         msg=f'Actual msg "{terms_and_conditions}" is not same as Expected msg "{cms_TandC_text}"')
        self.assertEqual(cms_button_text, cta_button,
                         msg=f'Actual msg "{cta_button}" is not same as Expected msg "{cms_button_text}"')

    def test_003_verify_the_image_uploads_of_launch_banner_Splash_page_image_and_Free_ride_text_image_in_splash_page(self):
        """
        DESCRIPTION: Verify these image uploads in Splash page: Launch Banner, Splash Page Image and Free Ride Text Image
        EXPECTED: Uploaded images should be displayed as per the CMS configurations
        """
        # Rest covered in above steps
        free_ride_text_image = self.dialog.free_ride_text_image
        self.assertTrue(free_ride_text_image.is_displayed(), msg='Free ride text image is not displayed')
