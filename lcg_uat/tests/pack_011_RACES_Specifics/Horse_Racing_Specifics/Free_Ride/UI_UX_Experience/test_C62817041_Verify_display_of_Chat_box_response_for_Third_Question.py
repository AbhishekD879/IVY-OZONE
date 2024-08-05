import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


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
class Test_C62817041_Verify_display_of_Chat_box_response_for_Third_Question(BaseRacing):
    """
    TR_ID: C62817041
    NAME: Verify display of Chat box response for Third Question
    DESCRIPTION: This test case verifies display of Chat box response as per the CMS configurations for Third Question
    PRECONDITIONS: Third question with Answers(option1,Option2 and Option3) are configured in CMS (Free Ride-> campaign -> Questions)
    PRECONDITIONS: Login to Ladbrokes application with eligible customers for Free Ride
    PRECONDITIONS: Click on 'Launch Banner' in Homepage
    PRECONDITIONS: Click on CTA Button in Splash Page
    PRECONDITIONS: User should select answers for First and Second questions
    PRECONDITIONS: User should on Third question as Step 3 of 3 page
    """
    keep_browser_open = True

    def selecting_options(self, question):
        self.assertTrue(question, msg='Question is not displayed yet')
        wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                        timeout=20, name='Waiting for options to be displayed')
        options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.values())
        options[0].click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Third question with Answers(option1,Option2 and Option3) are configured in CMS (Free Ride-> campaign -> Questions)
        DESCRIPTION: Login to Ladbrokes application with eligible customers for Free Ride
        DESCRIPTION: Click on 'Launch Banner' in Homepage
        DESCRIPTION: Click on CTA Button in Splash Page
        DESCRIPTION: User should select answers for First and Second questions
        DESCRIPTION: User should on Third question as Step 3 of 3 page
        """
        username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=username)
        self.update_spotlight_events_price(class_id=223)
        campaign_id = self.cms_config.check_update_and_create_freeride_campaign()
        self.__class__.response = self.cms_config.get_freeride_campaign_details(freeride_campaignid=campaign_id)
        self.site.login(username=username)
        self.site.home.free_ride_banner().click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_RIDE, timeout=10, verify_name=False)
        dialog.cta_button.click()
        first_question = wait_for_result(lambda: self.site.free_ride_overlay.first_question is not None,
                                         timeout=10, name='Waiting for First Question to be displayed')
        self.selecting_options(question=first_question)
        second_question = wait_for_result(lambda: self.site.free_ride_overlay.second_question is not None,
                                          timeout=10, name='Waiting for Second Question to be displayed')
        self.selecting_options(question=second_question)

    def test_001_verify_the_display_of_third_question_with_3_options(self):
        """
        DESCRIPTION: Verify the display of Third question with 3 options
        EXPECTED: Third question with below 3 answer options should be displayed
        EXPECTED: Good Chance
        EXPECTED: Nice Price
        EXPECTED: Surprise me!
        """
        self.__class__.third_question = wait_for_result(lambda: self.site.free_ride_overlay.third_question is not None,
                                                        timeout=10, name='Waiting for Third Question to be displayed')
        self.assertTrue(self.third_question, msg='Third question is not displayed')
        options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.keys())
        for option in options:
            self.assertIn(option, [vec.free_ride.OPTIONS_LIST.good_chance, vec.free_ride.OPTIONS_LIST.nice_price, vec.free_ride.OPTIONS_LIST.surprise_me],
                          msg=f'Actual option {option} is not in Expected options list'
                              f' {vec.free_ride.OPTIONS_LIST.good_chance, vec.free_ride.OPTIONS_LIST.nice_price, vec.free_ride.OPTIONS_LIST.surprise_me}')

    def test_002_select_1_option_from_the_above_3_options(self):
        """
        DESCRIPTION: Select 1 option from the above 3 options
        EXPECTED: Selected option should be highlighted with 'Red color'
        EXPECTED: Another 2 options should be in disabled mode
        """
        self.assertTrue(self.third_question, msg='Third Question is not displayed yet')
        wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                        timeout=20, name='Waiting for options to be displayed')
        option = self.site.free_ride_overlay.answers.items_as_ordered_dict.get(vec.free_ride.OPTIONS_LIST.good_chance)
        option.click()

    def test_003_verify_the_display_of_selected_option(self):
        """
        DESCRIPTION: Verify the display of selected option
        EXPECTED: Only selected one option should be displayed to the user
        """
        selected_answer = self.site.free_ride_overlay.third_selected_answer
        self.assertEqual(selected_answer, vec.free_ride.OPTIONS_LIST.good_chance,
                         msg=f'Actual selected option "{selected_answer}" is not same '
                             f'Expected option "{vec.free_ride.OPTIONS_LIST.good_chance}"')

    def test_004_verify_the_display_of_chat_box_response(self):
        """
        DESCRIPTION: Verify the display of chat box response
        EXPECTED: Chat box response should be displayed as per the CMS
        EXPECTED: configurations from 'Chat box Q3 response' field
        """
        chat_bot_response = self.site.free_ride_overlay.chat_bot_response_three
        expected_response = self.response['questionnarie']['questions'][2]['chatBoxResp'].replace('/', '')
        self.assertEqual(chat_bot_response, expected_response,
                         msg=f'Actual response "{chat_bot_response}" is not same as '
                             f'Expected response {expected_response}')

    def test_005_verify_the_ui_experience_of_chat_box(self):
        """
        DESCRIPTION: Verify the UI experience of chat box
        EXPECTED: Interactive chat bot session should be displayed as per Zeplin
        """
        result = wait_for_result(lambda: self.site.free_ride_overlay.summary is not None,
                                 timeout=10, name='Waiting for summary to be displayed')
        self.assertTrue(result, msg='Summary is not displayed')
        result = wait_for_result(lambda: self.site.free_ride_overlay.results_container is not None,
                                 timeout=10, name='Waiting for Results container to be displayed')
        self.assertTrue(result, msg='Results container is not displayed')
