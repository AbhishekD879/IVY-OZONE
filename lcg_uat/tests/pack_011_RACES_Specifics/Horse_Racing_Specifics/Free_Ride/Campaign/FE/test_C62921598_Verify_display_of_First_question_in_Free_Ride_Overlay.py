import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod # Cannot grant free ride in prod env
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.free_ride
@pytest.mark.races
@vtest
class Test_C62921598_Verify_display_of_First_question_in_Free_Ride_Overlay(Common):
    """
    TR_ID: C62921598
    NAME: Verify display of First question in Free Ride Overlay
    DESCRIPTION: This test case verifies display of First question in Free Ride Overlay
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Campaign should be created(Currently running) in Free Ride and First Question should be configured in CMS
        """
        self.__class__.username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=self.username)
        self.update_spotlight_events_price(class_id=223)
        campaign_id = self.cms_config.check_update_and_create_freeride_campaign()
        self.__class__.response = self.cms_config.get_freeride_campaign_details(freeride_campaignid=campaign_id)

    def test_001_login_to_Ladbrokes_Application_with_eligible_customer(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible customer
        EXPECTED: User should be able to login successfully
        """
        self.site.login(username=self.username)

    def test_002_Click_on_Launch_Free_Ride_Banner(self):
        """
        DESCRIPTION: Click on 'Launch Free Ride Banner'
        EXPECTED: Splash page with CTA button should be displayed
        """
        self.site.home.free_ride_banner().click()
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_RIDE, verify_name=False)
        self.assertTrue(self.dialog.cta_button.is_displayed(), msg='cta button not displayed')

    def test_003_Click_on_CTA_button_in_Splash_Page(self):
        """
        DESCRIPTION: Click on CTA button in Splash Page
        EXPECTED: Free Ride overlay should be displayed
        """
        self.dialog.cta_button.click()
        self.assertTrue(self.site.free_ride_overlay.is_displayed(), msg="Free Ride overlay is not displayed")

    def test_004_Verify_display_of_First_Question(self):
        """
        DESCRIPTION: Verify display of First Question
        EXPECTED: First Question should be displayed in Free Ride Overlay screen
        """
        first_question = wait_for_result(lambda: self.site.free_ride_overlay.first_question is not None,
                                         timeout=10, name='Waiting for First Question to be displayed')
        self.assertTrue(first_question, msg='Question is not displayed yet')

    def test_005_Verify_the_content_in_First_Question(self):
        """
        DESCRIPTION: Verify the content in First Question
        EXPECTED: Content in First Question should be displayed as per the CMS
        EXPECTED: configurations from 'Question1' field in Questions section in campaign
        """
        expected_response = self.response['questionnarie']['questions'][0]['quesDescription']
        actual_response = self.site.free_ride_overlay.first_question
        self.assertEqual(actual_response, expected_response, msg=f'Actual response "{actual_response}" is not same as '
                                                                 f'Expected response {expected_response}')
