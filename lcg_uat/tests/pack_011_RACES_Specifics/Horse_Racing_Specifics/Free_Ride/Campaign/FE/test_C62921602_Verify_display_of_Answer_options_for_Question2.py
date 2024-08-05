import tests
import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


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
class Test_C62921602_Verify_display_of_Answer_options_for_Question2(Common):
    """
    TR_ID: C62921602
    NAME: Verify display of Answer options for Question2
    DESCRIPTION: This test case verifies display of Answer options for Question2
    PRECONDITIONS: CMS
    PRECONDITIONS: 1: Campaign should be created and in currently running status
    PRECONDITIONS: 2: First and second questions with Answer options(Option1, Option2 and option3) are configured
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1: Campaign should be created and in currently running status
        PRECONDITIONS: 2: First and second questions with Answer options(Option1, Option2 and option3) are configured
        """
        self.__class__.username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=self.username)
        self.update_spotlight_events_price(class_id=223)
        freeride_campaign = self.cms_config.check_update_and_create_freeride_campaign()
        self.__class__.second_question_cms = self.cms_config.get_freeride_campaign_details(freeride_campaignid=freeride_campaign)['questionnarie']['questions'][1]

    def test_001_login_to_ladbrokes_application_with_eligible(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible
        EXPECTED: User should be able to login successfully
        """
        self.site.login(username=self.username)

    def test_002_click_on_launch_free_ride_banner(self):
        """
        DESCRIPTION: Click on 'Launch Free Ride Banner'
        EXPECTED: Splash page with CTA button should be displayed
        """
        free_ride_banner = self.site.home.free_ride_banner()
        free_ride_banner.click()
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

    def test_004_select_answer_for_first_question(self):
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
        self.assertEqual(vec.free_ride.OPTIONS_LIST[0], options[0].text, msg=f'Actual option "{options[0].text}" is not same as'
                                                                             f'Expected option "{vec.free_ride.OPTIONS_LIST[0]}"')

    def test_005_verify_display_of_second_question(self):
        """
        DESCRIPTION: Verify display of Second Question
        EXPECTED: Second Question should be displayed in Free Ride Overlay screen
        """
        second_question = wait_for_result(lambda: self.site.free_ride_overlay.second_question is not None,
                                          timeout=10, name='Waiting for second Question to be displayed')
        self.assertTrue(second_question,
                        msg='Second question is not displayed below to step 2 of 3')
        answers = wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                                  timeout=20, name='Waiting for options to be displayed')
        self.assertTrue(answers,
                        msg='Answers are not displayed for second question')

    def test_006_verify_display_of_answer_options_for_second_question(self):
        """
        DESCRIPTION: Verify display of Answer Options for Second Question
        EXPECTED: Answer Options should be displayed below to Step 2 of 3 as below
        EXPECTED: * Big & Strong
        EXPECTED: * Small & Nimble
        EXPECTED: * Surprise Me!
        EXPECTED: Note: 3 options are configured in CMS
        """
        second_question = self.site.free_ride_overlay.second_question
        self.assertEqual(second_question, self.second_question_cms['quesDescription'],
                         msg=f'Actual second question: "{second_question}" is not '
                             f'equal: "{self.second_question_cms}" from CMS')
        options_ui = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.keys())
        second_question_option = [self.second_question_cms['options'][0]['optionText'],
                                  self.second_question_cms['options'][1]['optionText'],
                                  self.second_question_cms['options'][2]['optionText']]
        self.assertListEqual(options_ui, second_question_option,
                             msg=f'Actual options list "{options_ui}" is not same as'
                                 f'Expected options list "{second_question_option}"')
