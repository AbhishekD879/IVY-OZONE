import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod #Cannot create offers in Prod
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.horseracing
@pytest.mark.free_ride
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C62921605_Verify_display_of_Third_question_in_Free_Ride_Overlay(Common):
    """
    TR_ID: C62921605
    NAME: Verify display of Third question in Free Ride Overlay
    DESCRIPTION: This test case verifies display of Third question in Free Ride Overlay
    PRECONDITIONS: CMS:
    PRECONDITIONS: 1: Campaign should be created(Currently running)
    PRECONDITIONS: 2: Make sure First, Second and Third questions are configured
    PRECONDITIONS: 3: Answer options for Question 1 and 2 are configured
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1: Campaign should be created(Currently running)
        PRECONDITIONS: 2: Make sure First, Second and Third questions are configured
        PRECONDITIONS: 3: Answer options for Question 1 and 2 are configured
        """
        username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=username)
        self.update_spotlight_events_price(class_id=223)
        campaign_id = self.cms_config.check_update_and_create_freeride_campaign()
        details = self.cms_config.get_freeride_campaign_details(campaign_id)
        option_values = details['questionnarie']['questions'][2]['options']
        options_key = 'optionText'
        self.__class__.cms_options = [option[options_key] for option in option_values]
        self.site.login(username=username)

    def test_001_login_to_ladbrokes_application_with_eligible(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible
        EXPECTED: User should be able to login successfully
        """
        # covered in above step

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

    def test_005_select_answer_for_second_question(self):
        """
        DESCRIPTION: Select Answer for second question
        EXPECTED: Selected Answer should be displayed below to Step 2 of 3
        """
        second_question = wait_for_result(lambda: self.site.free_ride_overlay.second_question is not None,
                                          timeout=10, name='Waiting for second Question to be displayed')
        self.assertTrue(second_question,
                        msg='Second question is not displayed below to step 2 of 3')
        answers = wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                                  timeout=20, name='Waiting for options to be displayed')
        self.assertTrue(answers,
                        msg='Answers are not displayed for first question')
        options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.values())
        options[0].click()

    def test_006_verify_display_of_third_question(self):
        """
        DESCRIPTION: Verify display of Third Question
        EXPECTED: Third Question should be displayed in Free Ride Overlay screen
        """
        third_question = wait_for_result(lambda: self.site.free_ride_overlay.third_question is not None,
                                         timeout=10, name='Waiting for third Question to be displayed')
        self.assertTrue(third_question,
                        msg='Third question is not displayed in overlay')

    def test_007_verify_the_content_in_third_question(self):
        """
        DESCRIPTION: Verify the content in Third Question
        EXPECTED: Content in Third Question should be displayed as per the CMS configurations from 'Question3' field in Questions section in campaign
        """
        answers = wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                                  timeout=20, name='Waiting for options to be displayed')
        self.assertTrue(answers,
                        msg='Answers are not displayed for third question')
        ui_options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.keys())
        self.assertListEqual(list1=self.cms_options, list2=ui_options,
                             msg=f'Actual List "{self.cms_options}" is not same as'
                                 f'Expected List of "{ui_options}".')
