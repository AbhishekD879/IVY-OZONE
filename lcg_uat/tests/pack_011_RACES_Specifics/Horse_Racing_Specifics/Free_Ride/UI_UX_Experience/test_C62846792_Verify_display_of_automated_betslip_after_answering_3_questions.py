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
class Test_C62846792_Verify_display_of_automated_betslip_after_answering_3_questions(Common):
    """
    TR_ID: C62846792
    NAME: Verify display of automated betslip after answering 3 questions
    DESCRIPTION: This test case verifies display of Chat box response as per the CMS configurations for First Question
    PRECONDITIONS: 1. First question with Answers(option1,Option2 and Option3) are configured in CMS (Free Ride-&gt; campaign -&gt; Questions)
    PRECONDITIONS: 2. Login to Ladbrokes application with eligible customers for Free Ride
    PRECONDITIONS: 3. Click on 'Launch Banner' in Homepage
    PRECONDITIONS: 4. Click on CTA Button in Splash Page
    PRECONDITIONS: 5. User should select answers for First, Second and Third questions
    """
    keep_browser_open = True
    options = [vec.free_ride.OPTIONS_LIST.top_player,
               vec.free_ride.OPTIONS_LIST.big_strong,
               vec.free_ride.OPTIONS_LIST.good_chance]

    def selecting_options(self, question, option):
        self.assertTrue(question, msg='Question is not displayed yet')
        wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                        timeout=20, name='Waiting for options to be displayed')
        answer = self.site.free_ride_overlay.answers.items_as_ordered_dict.get(option)
        answer.click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: First question with Answers(option1,Option2 and Option3) are configured in CMS (Free Ride-> campaign -> Questions)
        DESCRIPTION: Login to Ladbrokes application with eligible customers for Free Ride
        DESCRIPTION: Click on 'Launch Banner' in Homepage
        DESCRIPTION: Click on CTA Button in Splash Page
        DESCRIPTION: User should select answers for First, Second and Third questions
        """
        self.update_spotlight_events_price(class_id=223)
        campaign_id = self.cms_config.check_update_and_create_freeride_campaign()
        self.__class__.campaign_questions_details = self.cms_config.get_freeride_campaign_details(freeride_campaignid=campaign_id)
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
        first_question = wait_for_result(lambda: self.site.free_ride_overlay.first_question is not None,
                                         timeout=10, name='Waiting for First Question to be displayed')
        self.selecting_options(question=first_question, option=self.options[0])

        second_question = wait_for_result(lambda: self.site.free_ride_overlay.second_question is not None,
                                          timeout=10, name='Waiting for Second Question to be displayed')
        self.selecting_options(question=second_question, option=self.options[1])

        third_question = wait_for_result(lambda: self.site.free_ride_overlay.third_question is not None,
                                         timeout=10, name='Waiting for Third Question to be displayed')
        self.selecting_options(question=third_question, option=self.options[2])

    def test_001_verify_the_display_of_third_question_with_selected_options(self):
        """
        DESCRIPTION: Verify the display of third question with selected options
        EXPECTED: Third question with selected answer should be displayed to the user
        """
        actual_selected_answer = self.site.free_ride_overlay.third_selected_answer
        self.assertEqual(actual_selected_answer, vec.free_ride.OPTIONS_LIST.good_chance,
                         msg=f'Actual selected answer "{actual_selected_answer}" is not same as Expected selected answer "{vec.free_ride.OPTIONS_LIST.good_chance}"')

    def test_002_Verify_display_of_Summary_message_in_Free_Ride_Overlay(self):
        """
        DESCRIPTION: Verify display of Summary message in Free Ride Overlay
        EXPECTED: Summary message with Rate, Horse and Odds information should be displayed
        """
        summary_details_list = self.site.free_ride_overlay.summary.split('\n')
        expected_message = self.campaign_questions_details['questionnarie']['summaryMsg']
        self.assertEqual(summary_details_list[0], expected_message,
                         msg=f'Actual Summary Message "{summary_details_list[0]}" is not same '
                             f'as Expected Summary Message "{expected_message}"')
        expected_summary_fields = f'Rating: {self.options[0]}Horse: {self.options[1]}Odds: {self.options[2]}'
        self.assertEqual(summary_details_list[1], expected_summary_fields,
                         msg=f'Actual Summary Message "{summary_details_list[1]}" is not same '
                             f'as Expected Summary Message "{expected_summary_fields}"')

    def test_003_Verify_display_of_automated_betslip(self):
        """
        DESCRIPTION: Verify display of automated betslip
        EXPECTED: Automated betslip should be successfully generated in Free Ride Overlay
        """
        automated_betslip = self.site.free_ride_overlay.results_container.split('\n')
        self.assertTrue(automated_betslip, msg="Automated betslip is not generated")
        self.assertTrue(automated_betslip[0], msg="Message is not shown on the automated betslip")
        self.assertTrue(automated_betslip[1], msg="Horse name is not shown on the automated betslip")
        self.assertTrue(automated_betslip[2], msg="Jockey name is not shown on the automated betslip")
        self.assertTrue(automated_betslip[3], msg="Event time and Meeting place name is not shown on the automated betslip")
        jockey_logo = self.site.free_ride_overlay.jockey_logo
        self.assertTrue(jockey_logo.is_displayed(), msg="Jockey Logo is not displayed on automated betlsip")
        CTA_to_racecard = self.site.free_ride_overlay.CTA_button
        self.assertTrue(CTA_to_racecard.is_displayed(), msg="CTA TO RACECARD is not displayed")

    def test_004_Verify_the_fields_in_automated_betslip(self):
        """
        DESCRIPTION:Verify the fields in automated betslip
        EXPECTED: Below information should be displayed:
        EXPECTED: That’s it! We made something for you:
        EXPECTED: Name of the Horse:
        EXPECTED: Name of the Jockey
        EXPECTED: Event Time, Meeting place name
        EXPECTED: Jockey(kits and crests) logo below to summary details
        EXPECTED: "CTA TO RACECARD" CTA should be displayed
        """
        # Covered in above step
