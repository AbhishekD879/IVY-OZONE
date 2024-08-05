import pytest
import tests
from tests.Common import Common
from tests.base_test import vtest
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
class Test_C62921617_Verify_user_is_able_to_close_and_relaunch_the_Free_Ride_overlay_before_answering_3rd_ques(Common):
    """
    TR_ID: C62921617
    NAME: Verify user is able to close and relaunch the Free Ride overlay before answering 3rd ques
    DESCRIPTION: This test case verifies user is able to close and relaunch the Free Ride overlay before answering 3rd ques
    PRECONDITIONS: Campaign should be created and questions are configured in cms
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Campaign should be created and questions are configured in cms
        """
        self.update_spotlight_events_price(class_id=223)
        campaign_id = self.cms_config.check_update_and_create_freeride_campaign()
        campaign_questions_details = self.cms_config.get_freeride_campaign_details(campaign_id)
        self.__class__.first_question_response = campaign_questions_details['questionnarie']['questions'][0][
            'chatBoxResp']
        self.__class__.username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=self.username)

    def test_001_login_to_ladbrokes_application_with_eligible_customer(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible customer
        EXPECTED: User should be able to login successfully and Free Ride Banner should be displayed
        """
        self.site.login(username=self.username)

    def test_002_click_on_launch_free_ride_banner_in_homepage(self):
        """
        DESCRIPTION: Click on 'Launch Free Ride Banner' in Homepage
        EXPECTED: * Splash page with CTA button should be displayed
        EXPECTED: * close button (X on the top right side) should be displayed
        """
        free_ride_banner = self.site.home.free_ride_banner()
        if self.device_type == 'mobile':
            self.site.home.scroll_to()
        free_ride_banner.click()
        self.__class__.free_ride_dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_RIDE,
                                                                    timeout=20,
                                                                    verify_name=False)
        self.assertTrue(self.free_ride_dialog.cta_button.is_displayed(),
                        msg='Splash page with CTA button not displayed')
        self.assertTrue(self.free_ride_dialog.close_icon.is_displayed(),
                        msg='Splash page with close button not displayed')

    def test_003_click_close_button_x_on_the_top_right_side(self):
        """
        DESCRIPTION: Click close button (X on the top right side)
        EXPECTED: Free Ride overlay should be closed
        """
        self.free_ride_dialog.close_icon.click()
        free_ride_overlay_result = wait_for_result(lambda: self.site.free_ride_overlay is None,
                                                   timeout=20, name='Waiting for free ride overlay is not be displayed')
        self.assertFalse(free_ride_overlay_result, msg='free ride overlay is still displaying after clicking on close button.')

    def test_004_repeat_step2_and_click_on_cta_button_in_splash_page(self):
        """
        DESCRIPTION: Repeat step2 and Click on CTA button in Splash Page
        EXPECTED: * Free Ride overlay with Welcome message should be displayed
        EXPECTED: * close button (X on the top right side) should be displayed
        """
        self.test_002_click_on_launch_free_ride_banner_in_homepage()
        self.free_ride_dialog.cta_button.click()
        free_ride_overlay_result = wait_for_result(lambda: self.site.free_ride_overlay is not None,
                                                   timeout=20, name='Waiting for free ride overlay to be displayed')
        self.assertTrue(free_ride_overlay_result, msg='free ride overlay is not displayed')
        self.assertTrue(self.site.free_ride_overlay.close_icon.is_displayed(),
                        msg='Splash page with close button not displayed')

    def test_005_click_close_button_x_on_the_top_right_side(self):
        """
        DESCRIPTION: Click close button (X on the top right side)
        EXPECTED: Free Ride overlay should be closed
        """
        self.site.free_ride_overlay.close_icon.click()
        free_ride_overlay_result = wait_for_result(lambda: self.site.free_ride_overlay is None,
                                                   timeout=20, name='Waiting for free ride overlay is not be displayed')
        self.assertFalse(free_ride_overlay_result,
                         msg='free ride overlay is still displaying after clicking on close button.')

    def test_006_repeat_step_4_and_select_answer_option_for_question1(self):
        """
        DESCRIPTION: Repeat step 4 and select answer option for question1
        EXPECTED: * Selected answer option should be highlighted in Red color in First question answer page
        EXPECTED: * close button (X on the top right side) should be displayed
        """
        self.test_004_repeat_step2_and_click_on_cta_button_in_splash_page()
        first_question = wait_for_result(lambda: self.site.free_ride_overlay.first_question is not None,
                                         timeout=20, name='Waiting for First Question to be displayed')
        self.assertTrue(first_question,
                        msg='First question is not displayed below to step 1 of 3')

        answers = wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                                  timeout=20, name='Waiting for options to be displayed')
        self.assertTrue(answers,
                        msg='Answers are not displayed for first question')
        options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.values())
        options[0].click()

    def test_007_click_close_button_x_on_the_top_right_side(self):
        """
        DESCRIPTION: Click close button (X on the top right side)
        EXPECTED: Free Ride overlay should be closed
        """
        self.test_005_click_close_button_x_on_the_top_right_side()

    def test_008_repeat_step_6_and_wait_for_chat_box_response_for_question1(self):
        """
        DESCRIPTION: Repeat step 6 and wait for chat box response for question1
        EXPECTED: * Chat box response for question1 should be displayed
        EXPECTED: * close button (X on the top right side) should be displayed
        """
        self.test_006_repeat_step_4_and_select_answer_option_for_question1()
        first_chat_bot_response = self.site.free_ride_overlay.chat_bot_response_one
        self.assertEqual(first_chat_bot_response, self.first_question_response,
                         msg=f'First chatbot response on UI "{first_chat_bot_response}" is not same as in cms "{self.first_question_response}"')

    def test_009_click_close_button_x_on_the_top_right_side(self):
        """
        DESCRIPTION: Click close button (X on the top right side)
        EXPECTED: Free Ride overlay should be closed
        """
        self.test_005_click_close_button_x_on_the_top_right_side()

    def test_010_repeat_steps_6_9_for_question2(self):
        """
        DESCRIPTION: Repeat steps 6-9 for question2
        EXPECTED:
        """
        self.test_008_repeat_step_6_and_wait_for_chat_box_response_for_question1()
        second_question = wait_for_result(lambda: self.site.free_ride_overlay.second_question is not None,
                                         timeout=20, name='Waiting for First Question to be displayed')
        self.assertTrue(second_question,
                        msg='Second question is not displayed below to step 2 of 3')
        self.test_005_click_close_button_x_on_the_top_right_side()

    def test_011_repeat_step4_and_select_answer_options_for_question12(self):
        """
        DESCRIPTION: Repeat step4 and select answer options for question1,2
        EXPECTED: * Free Ride overlay with question3 page should be displayed
        EXPECTED: * close button (X on the top right side) should be displayed
        """
        self.test_008_repeat_step_6_and_wait_for_chat_box_response_for_question1()
        second_question = wait_for_result(lambda: self.site.free_ride_overlay.second_question is not None,
                                          timeout=20, name='Waiting for First Question to be displayed')
        self.assertTrue(second_question,
                        msg='Second question is not displayed below to step 2 of 3')
        answers = wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                                  timeout=20, name='Waiting for options to be displayed')
        self.assertTrue(answers,
                        msg='Answers are not displayed for second question')
        options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.values())
        options[0].click()

    def test_012_click_close_button_x_on_the_top_right_side(self):
        """
        DESCRIPTION: Click close button (X on the top right side)
        EXPECTED: Free Ride overlay should be closed
        """
        self.test_005_click_close_button_x_on_the_top_right_side()

    def test_013_repeat_step2(self):
        """
        DESCRIPTION: Repeat step2
        EXPECTED:
        """
        self.test_002_click_on_launch_free_ride_banner_in_homepage()
