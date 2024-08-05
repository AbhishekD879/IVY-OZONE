import pytest
import tests
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.Common import Common
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
class Test_C62834400_Verify_display_of_Summary_message_after_answering_3_questions(Common):
    """
    TR_ID: C62834400
    NAME: Verify display of Summary  message after answering 3 questions
    DESCRIPTION: This test case verifies display of Summary  message after answering 3 questions
    PRECONDITIONS: 1. Third question with Answers(option1,Option2 and Option3) and Summary message are configured in CMS (Free Ride-&gt; campaign -&gt; Questions)
    PRECONDITIONS: 2. Login to Ladbrokes application with eligible customers for Free Ride
    PRECONDITIONS: 3. Click on 'Launch Banner' in Homepage
    PRECONDITIONS: 4. Click on CTA Button in Splash Page
    PRECONDITIONS: 5. User should select answers for First, Second and Third questions
    """
    keep_browser_open = True
    answers_array = []

    def select_answers(self):
        wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                        timeout=20, name='Waiting for options to be displayed')
        options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.values())
        self.answers_array.append(options[0].text)
        options[0].click()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Creating campaign from cms and adding freeride to user from ob
        PRECONDITIONS: User should select answers for First, Second and Third questions
        """
        username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=username)
        self.site.login(username=username)
        self.update_spotlight_events_price(class_id=223)
        campaign_id = self.cms_config.check_update_and_create_freeride_campaign()
        self.__class__.campaign_questions_details = self.cms_config.get_freeride_campaign_details(campaign_id)
        self.site.home.free_ride_banner().click()
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_RIDE, timeout=10,
                                                          verify_name=False)
        self.assertTrue(self.dialog.cta_button.is_displayed(), msg=f'CTA Button is not displayed')
        self.dialog.cta_button.click()
        wait_for_result(lambda: self.site.free_ride_overlay.welcome_message is not None,
                        timeout=10, name='Waiting for Welcome message to be displayed')
        wait_for_result(lambda: self.site.free_ride_overlay.first_question is not None,
                        timeout=10, name='Waiting for First Question to be displayed')
        self.select_answers()
        wait_for_result(lambda: self.site.free_ride_overlay.second_question is not None,
                        timeout=10, name='Waiting for Second Question to be displayed')
        self.select_answers()
        wait_for_result(lambda: self.site.free_ride_overlay.third_question is not None,
                        timeout=10, name='Waiting for Third Question to be displayed')

    def test_001_verify_the_display_of_third_question_with_selected_option(self):
        """
        DESCRIPTION: Verify the display of Third question with selected option
        EXPECTED: Third question with selected answer should be displayed to the user
        """
        self.select_answers()
        self.assertEquals(self.site.free_ride_overlay.third_selected_answer, self.answers_array[2], msg=f'third selected answer {self.site.free_ride_overlay.third_selected_answer} is not same as {self.answers_array[2]} ')

    def test_002_verify_display_of_summary_message_in_free_ride_overlay(self):
        """
        DESCRIPTION: Verify display of Summary message in Free Ride Overlay
        EXPECTED: Summary message should be displayed as per the CMS configurations from 'Summary Message' field
        """
        summary_msg_CMS = self.campaign_questions_details['questionnarie']['summaryMsg']
        self.__class__.summary_details_list = self.site.free_ride_overlay.summary.split('\n')
        summary_message = self.summary_details_list[0]
        self.assertEqual(summary_message, summary_msg_CMS,
                         msg=f'Welcome Message content is different from UI {self.site.free_ride_overlay.welcome_message} and CMS text {summary_msg_CMS}')

    def test_003_verify_the_display_rate_horse_and_odds_fields_along_with_summary_message(self):
        """
        DESCRIPTION: Verify the display Rate, Horse and Odds fields along with summary message
        EXPECTED: Rate, Horse and Odds fields along with summary message should be displayed
        """
        expected_summary_fields = f'Rating: {self.answers_array[0]}Horse: {self.answers_array[1]}Odds: {self.answers_array[2]}'
        self.assertEqual(self.summary_details_list[1], expected_summary_fields,
                         msg=f'Actual Summary Message "{self.summary_details_list[1]}" is not same '
                             f'as Expected Summary Message "{expected_summary_fields}"')

    def test_004_verify_display_of_content_inrate_horse_and_odds_fields(self):
        """
        DESCRIPTION: Verify display of content in Rate, Horse and Odds fields
        EXPECTED: Content in Rate, Horse and Odds fields in free Ride overlay should display as below
        EXPECTED: * Rate: option selected by the user for question1
        EXPECTED: * Horse: option selected by the user for question2
        EXPECTED: * Odds: option selected by the user for question3
        """
        # covered in  step 3
