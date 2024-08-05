import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod #Can't create offers in Prod
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.races
@pytest.mark.free_ride
@vtest
class Test_C62921596_Verify_display_of_Welcome_message_in_Free_Ride_Overlay(Common):
    """
    TR_ID: C62921596
    NAME: Verify display of Welcome message in Free Ride Overlay
    DESCRIPTION: This test case verifies display of Welcome message in Free Ride Overlay
    PRECONDITIONS: Campaign should be created in Free Ride and Welcome Message should be configured in CMS
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Campaign should be created in CMS and Offer should be assigned to the user in OB
        """
        self.__class__.username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=self.username)
        self.update_spotlight_events_price(class_id=223)
        campaign_id = self.cms_config.check_update_and_create_freeride_campaign()
        self.__class__.campaign_questions_response = self.cms_config.get_freeride_campaign_details(campaign_id)

    def test_001_login_to_ladbrokes_application_with_eligible_customer(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible customer
        EXPECTED: User should be able to login successfully and Free Ride Banner is displayed to the user
        """
        self.site.login(username=self.username)
        self.__class__.free_ride_banner = self.site.home.free_ride_banner()

    def test_002_click_on_launch_free_ride_banner(self):
        """
        DESCRIPTION: Click on 'Launch Free Ride Banner'
        EXPECTED: Splash page with CTA button should be displayed
        """
        self.free_ride_banner.click()
        self.__class__.free_ride_dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_RIDE,
                                                                    timeout=10,
                                                                    verify_name=False)
        self.assertTrue(self.free_ride_dialog.cta_button.is_displayed(),
                        msg='Splash page with CTA button not displayed')

    def test_003_click_on_cta_button_in_splash_page(self):
        """
        DESCRIPTION: Click on CTA button in Splash Page
        EXPECTED: Free Ride overlay should be displayed
        """
        self.free_ride_dialog.cta_button.click()
        free_ride_overlay_result = wait_for_result(lambda: self.site.free_ride_overlay is not None,
                                                   timeout=10, name='Waiting for free ride overlay to be displayed')
        self.assertTrue(free_ride_overlay_result, msg='free ride overlay is not displayed')

    def test_004_verify_display_of_welcome_message(self):
        """
        DESCRIPTION: Verify display of welcome Message
        EXPECTED: welcome Message should be displayed in Free Ride Overlay screen
        """
        self.assertTrue(self.site.free_ride_overlay.welcome_message,
                        msg="welcome Message is not displayed in Free Ride Overlay screen")

    def test_005_verify_the_content_in_welcome_message(self):
        """
        DESCRIPTION: Verify the content in welcome Message
        EXPECTED: Content in Welcome Message should be displayed as per the CMS configurations from 'Welcome Message' field in Questions section in campaign
        """
        welcome_msg_CMS = self.campaign_questions_response['questionnarie']['welcomeMessage']
        self.assertEqual(self.site.free_ride_overlay.welcome_message, welcome_msg_CMS,
                         msg=f'Welcome Message content is different from UI {self.site.free_ride_overlay.welcome_message} and CMS text {welcome_msg_CMS}')
