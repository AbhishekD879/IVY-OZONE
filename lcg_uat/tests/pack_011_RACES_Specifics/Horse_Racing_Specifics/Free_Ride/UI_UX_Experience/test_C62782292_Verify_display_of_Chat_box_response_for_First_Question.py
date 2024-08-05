import pytest
import tests
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


# @pytest.mark.lad_prod # cannot automate on prod
# @pytest.mark.lad_hl
@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.high
@pytest.mark.homepage_featured
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.free_ride
@vtest
class Test_C62782292_Verify_display_of_Chat_box_response_for_First_Question(Common):
    """
    TR_ID: C62782292
    NAME: Verify display of Chat box response for First Question
    DESCRIPTION: This test case verifies display of Chat box response as per the CMS configurations for First Question
    PRECONDITIONS: 1. First question with Answers(option1,Option2 and Option3) are configured in CMS (Free Ride-&gt; campaign -&gt; Questions)
    PRECONDITIONS: 2. Login to Ladbrokes application with eligible customers for Free Ride
    PRECONDITIONS: 3. Click on 'Launch Banner' in Homepage
    PRECONDITIONS: 4. Click on CTA Button in Splash Page
    PRECONDITIONS: 5. User should be on First question as Step 1 of 3 page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: First question with Answers(option1,Option2 and Option3) are configured in CMS (Free Ride-> campaign -> Questions)
        DESCRIPTION: Login to Ladbrokes application with eligible customers for Free Ride
        DESCRIPTION: Click on 'Launch Banner' in Homepage
        DESCRIPTION: Click on CTA Button in Splash Page
        DESCRIPTION: User should be on First question as Step 1 of 3 page
        """
        self.update_spotlight_events_price(class_id=223)
        campaign_id = self.cms_config.check_update_and_create_freeride_campaign()
        campaign_questions_details = self.cms_config.get_freeride_campaign_details(campaign_id)
        self.__class__.first_question_response = campaign_questions_details['questionnarie']['questions'][0][
            'chatBoxResp']
        username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(username=username, offer_id=offer_id)
        self.site.login(username=username)
        self.site.home.free_ride_banner().click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_RIDE, timeout=10,
                                           verify_name=False)
        dialog.cta_button.click()
        wait_for_result(lambda: self.site.free_ride_overlay.welcome_message is not None,
                        timeout=10, name='Waiting for Welcome message to be displayed')
        result = wait_for_result(lambda: self.site.free_ride_overlay.first_question is not None,
                                 timeout=10, name='Waiting for First Question to be displayed')
        self.assertTrue(result, msg='Unable to display first question')

    def test_001_verify_the_display_of_first_question_with_3_options(self):
        """
        DESCRIPTION: Verify the display of First question with 3 options
        EXPECTED: First question with below 3 answer options should be displayed
        EXPECTED: * Top Player
        EXPECTED: * Dark Horse
        EXPECTED: * Surprise me!
        """
        question_1 = self.site.free_ride_overlay.first_question
        self.assertTrue(question_1, msg='question_1 is not displaying')
        options_name = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.keys())
        expected_option = [vec.free_ride.OPTIONS_LIST.top_player, vec.free_ride.OPTIONS_LIST.dark_horse,
                           vec.free_ride.OPTIONS_LIST.surprise_me]
        self.assertEqual(options_name, expected_option,
                         msg=f'First question option in UI "{options_name}" is not same as "{expected_option}"')

    def test_002_select_1_option_from_the_above_3_options(self):
        """
        DESCRIPTION: Select 1 option from the above 3 options
        EXPECTED: * Selected option should be highlighted with 'Red color'
        EXPECTED: * Another 2 options should be in disabled mode
        """
        options = self.site.free_ride_overlay.answers.items_as_ordered_dict.get(vec.free_ride.OPTIONS_LIST.top_player)
        options.click()

    def test_003_verify_the_display_of_selected_option(self):
        """
        DESCRIPTION: Verify the display of selected option
        EXPECTED: Only selected one option should be displayed to the user
        """
        selected_option = self.site.free_ride_overlay.first_selected_answer
        self.assertEqual(selected_option, vec.free_ride.OPTIONS_LIST.top_player,
                         msg=f'Selected first option "{selected_option}" is not same as "{vec.free_ride.OPTIONS_LIST.top_player}"')

    def test_004_verify_the_display_of_chat_box_response(self):
        """
        DESCRIPTION: Verify the display of chat box response
        EXPECTED: Chat box response should be displayed as per the CMS configurations from 'Chat box Q1 response' field
        """
        first_chat_bot_response = self.site.free_ride_overlay.chat_bot_response_one
        self.assertEqual(first_chat_bot_response, self.first_question_response,
                         msg=f'First chatbot response on UI "{first_chat_bot_response}" is not same as in cms "{self.first_question_response}"')

    def test_005_verify_the_ui_experience_of_chat_box(self):
        """
        DESCRIPTION: Verify the UI experience of chat box
        EXPECTED: Interactive chat bot session should be displayed as per Zeplin
        """
        # Above step is not applicable for automation
