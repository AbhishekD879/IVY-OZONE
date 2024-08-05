import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod #cannot grant free ride to user in prod
# @pytest.mark.lad_hl  #and cannot create campaigns in prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.horseracing
@pytest.mark.free_ride
@vtest
class Test_C62921601_Verify_display_of_Second_question_in_Free_Ride_Overlay(Common):
    """
    TR_ID: C62921601
    NAME: Verify display of Second question in Free Ride Overlay
    DESCRIPTION: This test case verifies display of Second question in Free Ride Overlay
    PRECONDITIONS: CMS 1: Campaign should be created and in currently running status
    PRECONDITIONS: 2: Make sure First question & Answer options and second question is configured
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: CMS 1: Campaign should be created and in currently running status
        PRECONDITIONS: 2: Make sure First question & Answer options and second question is configured
        """
        self.__class__.username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=self.username)
        self.update_spotlight_events_price(class_id=223)
        freeride_campaign = self.cms_config.check_update_and_create_freeride_campaign()
        self.__class__.second_question_cms = \
            self.cms_config.get_freeride_campaign_details(freeride_campaignid=freeride_campaign)['questionnarie'][
                'questions'][1]

    def test_001_Login_to_Ladbrokes_Application_with_eligible(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible
        EXPECTED: - User should be able to login successfully
        """
        self.site.login(username=self.username)

    def test_002_Click_on_Launch_Free_Ride_Banner(self):
        """
        DESCRIPTION: Click on 'Launch Free Ride Banner'
        EXPECTED: Splash page with CTA button should be displayedsandhy
        """
        free_ride_banner = self.site.home.free_ride_banner()
        free_ride_banner.click()
        self.__class__.free_ride_dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_RIDE,
                                                                    timeout=10,
                                                                    verify_name=False)
        self.assertTrue(self.free_ride_dialog.cta_button.is_displayed(),
                        msg='Splash page with CTA button not displayed')

    def test_003_Click_on_CTA_button_in_Splash_Page(self):
        """
        DESCRIPTION: Click on CTA button in Splash Page
        EXPECTED: Free Ride overlay should be displayed
        """
        self.free_ride_dialog.cta_button.click()
        free_ride_overlay_result = wait_for_result(lambda: self.site.free_ride_overlay is not None,
                                                   timeout=10, name='Waiting for free ride overlay to be displayed')
        self.assertTrue(free_ride_overlay_result, msg='free ride overlay is not displayed')

    def test_004_Select_Answer_for_First_question(self):
        """
        DESCRIPTION: Select Answer for First question
        EXPECTED: Selected Answer should be displayed below to Step 1 of 3
        """
        first_question = wait_for_result(lambda: self.site.free_ride_overlay.first_question is not None,
                                         timeout=10, name='Waiting for First Question to be displayed')
        self.assertTrue(first_question,
                        msg='First question is not displayed below to step 1 of 3')

        answers = wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                                  timeout=20, name='Waiting for options to be displayed')
        self.assertTrue(answers,
                        msg='Answers are not displayed for first question')
        options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.values())
        options[0].click()

    def test_005_Select_display_of_Second_question(self):
        """
        DESCRIPTION: Select display of Second question
        EXPECTED: Second Question should be displayed in Free Ride Overlay screen
        """
        second_question = wait_for_result(lambda: self.site.free_ride_overlay.second_question is not None,
                                          timeout=10, name='Waiting for second Question to be displayed')
        self.assertTrue(second_question,
                        msg='Second question is not displayed below to step 2 of 3')

    def test_006_Verify_the_content_in_second_Question(self):
        """
        DESCRIPTION: Verify the content in Second Question
        EXPECTED: Content in Second Question should be displayed as per the CMS configurations from 'Question2' field in Questions section in campaign
        """
        answers = wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                                  timeout=20, name='Waiting for options to be displayed')
        self.assertTrue(answers, msg='Answers are not displayed for second question')
        second_question_des = self.site.free_ride_overlay.second_question
        self.assertEqual(second_question_des, self.second_question_cms['quesDescription'],
                         msg=f'Actual second question: "{second_question_des}" is not '
                             f'same as expected: "{self.second_question_cms}" from CMS')

        options_ui = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.keys())
        second_question_option = [self.second_question_cms['options'][0]['optionText'],
                                  self.second_question_cms['options'][1]['optionText'],
                                  self.second_question_cms['options'][2]['optionText']]
        self.assertListEqual(options_ui, second_question_option,
                             msg=f'Actual options list "{options_ui}" is not same as'
                                 f'Expected options list "{second_question_option}"')
