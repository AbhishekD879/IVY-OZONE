import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
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
class Test_C62933323_Verify_horse_selection_when_user_selects_Surprise_Me_option_for_3_questions(Common):
    """
    TR_ID: C62933323
    NAME: Verify horse selection, when user selects 'Surprise Me' option for 3 questions
    DESCRIPTION: This test case verifies horse selection, when user selects 'Surprise Me' option for 3 questions
    PRECONDITIONS: CMS:Below specifics are configured in cms
    PRECONDITIONS: 1.Splash Page
    PRECONDITIONS: 2.Questions and Options(Free Ride -Campaign ->Questions)
    PRECONDITIONS: FE:
    PRECONDITIONS: 1.Eligible user logins to ladbrokes application
    PRECONDITIONS: Click on 'Launch Banner' in Homepage
    PRECONDITIONS: Click on CTA Button in Splash Page
    PRECONDITIONS: User should be on First question as Step 1 of 3 page
    """
    keep_browser_open = True
    expected_color = 'rgba(222, 43, 0, 1)'

    def check_color(self, options):
        option = options.get(vec.free_ride.OPTIONS_LIST.surprise_me)
        option.click()
        color = option.value_of_css_property('background-color')
        self.assertEqual(color, self.expected_color, msg=f'Actual color "{color}" is not same as '
                                                         f'Expected color "{self.expected_color}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: CMS:Below specifics are configured in cms
        DESCRIPTION: 1.Splash Page
        DESCRIPTION: 2.Questions and Options(Free Ride -Campaign ->Questions)
        DESCRIPTION: FE:
        DESCRIPTION: 1.Eligible user logins to ladbrokes application
        DESCRIPTION: Click on 'Launch Banner' in Homepage
        DESCRIPTION: Click on CTA Button in Splash Page
        DESCRIPTION: User should be on First question as Step 1 of 3 page
        """
        username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=username)
        self.update_spotlight_events_price(class_id=223)
        campaign_id = self.cms_config.check_update_and_create_freeride_campaign()
        self.__class__.response = self.cms_config.get_freeride_campaign_details(freeride_campaignid=campaign_id)
        self.__class__.pots = self.cms_config.get_pots(freeride_campaignid=campaign_id)
        self.site.login(username=username)
        self.site.home.free_ride_banner().click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_RIDE, timeout=10, verify_name=False)
        dialog.cta_button.click()
        first_question = wait_for_result(lambda: self.site.free_ride_overlay.first_question is not None,
                                         timeout=10, name='Waiting for First Question to be displayed')
        self.assertTrue(first_question, msg='Question is not displayed yet')

    def test_001_verify_the_display_of_first_question(self):
        """
        DESCRIPTION: Verify the display of first question
        EXPECTED: User can view the first question with below options
        EXPECTED: 1. Top Player
        EXPECTED: 2. Dark Horse
        EXPECTED: 3. Surprise Me!
        """
        first_question_options_list = [vec.free_ride.OPTIONS_LIST.top_player, vec.free_ride.OPTIONS_LIST.dark_horse, vec.free_ride.OPTIONS_LIST.surprise_me]
        options = self.site.free_ride_overlay.answers.items_as_ordered_dict
        self.assertListEqual(list(options.keys()), first_question_options_list,
                             msg=f'Actual option {list(options.keys())} is not same as '
                                 f'Expected options {first_question_options_list}')
        self.check_color(options=options)

    def test_002_select_surprise_me_from_the_options(self):
        """
        DESCRIPTION: select 'Surprise Me' from the options
        EXPECTED: Selected Option is highlighted in Red.
        """
        # covered in above step

    def test_003_verify_the_display_of_selected_option(self):
        """
        DESCRIPTION: Verify the display of second question
        EXPECTED: Second Question is displayed with below options
        EXPECTED: 1.Big and Strong
        EXPECTED: 2.Small & Nimble
        EXPECTED: 3.Surprise Me
        """
        second_question = wait_for_result(lambda: self.site.free_ride_overlay.second_question is not None,
                                          timeout=10, name='Waiting for Second Question to be displayed')
        self.assertTrue(second_question, msg='Question is not displayed yet')
        second_question_options_list = [vec.free_ride.OPTIONS_LIST.big_strong, vec.free_ride.OPTIONS_LIST.small_nimble, vec.free_ride.OPTIONS_LIST.surprise_me]
        options = self.site.free_ride_overlay.answers.items_as_ordered_dict
        self.assertListEqual(list(options.keys()), second_question_options_list,
                             msg=f'Actual option {list(options.keys())} is not same as '
                                 f'Expected options {second_question_options_list}')
        self.check_color(options=options)

    def test_004_Select_surprise_me_from_the_options(self):
        """
        DESCRIPTION: Select 'Surprise Me' from the options
        EXPECTED: Selected Option is highlighted in Red
        """
        # covered in above step

    def test_005_verify_the_display_of_third_question(self):
        """
        DESCRIPTION: Verify the display of third question
        EXPECTED: Third Question is displayed with below options
        EXPECTED: 1.Good Chance
        EXPECTED: 2.Nice Price
        EXPECTED: 3.Surprise Me
        """
        third_question = wait_for_result(lambda: self.site.free_ride_overlay.third_question is not None,
                                         timeout=10, name='Waiting for Second Question to be displayed')
        self.assertTrue(third_question, msg='Question is not displayed yet')
        third_question_options_list = [vec.free_ride.OPTIONS_LIST.good_chance, vec.free_ride.OPTIONS_LIST.nice_price, vec.free_ride.OPTIONS_LIST.surprise_me]
        options = self.site.free_ride_overlay.answers.items_as_ordered_dict
        self.assertListEqual(list(options.keys()), third_question_options_list,
                             msg=f'Actual option {list(options.keys())} is not same as '
                                 f'Expected options {third_question_options_list}')
        self.check_color(options=options)

    def test_006_select_surprise_me_from_the_options(self):
        """
        DESCRIPTION: Select 'Surprise Me' from the options
        EXPECTED: Selected Option is highlighted in Red
        """
        # covered in above step

    def test_007_verify_the_summary_message(self):
        """
        DESCRIPTION: Verify the summary message
        EXPECTED: Summary message is displayed to the user, with below fields
        EXPECTED: Rate: Surprise Me
        EXPECTED: Horse: Surprise Me
        EXPECTED: Odds: Surprise Me
        """
        summary_details_list = self.site.free_ride_overlay.summary.split('\n')
        summary_message = summary_details_list[0]
        expected_message = self.response['questionnarie']['summaryMsg']
        self.assertEqual(summary_message, expected_message,
                         msg=f'Actual Summary Message "{summary_message}" is not same '
                             f'as Expected Summary Message "{expected_message}"')
        expected_summary_fields = 'Rating: Surprise me!Horse: Surprise me!Odds: Surprise me!'
        self.assertEqual(summary_details_list[1], expected_summary_fields,
                         msg=f'Actual Summary Message "{summary_details_list[1]}" is not same '
                             f'as Expected Summary Message "{expected_summary_fields}"')

    def test_008_verify_the_allocated_horse_details_in_cms(self):
        """
        DESCRIPTION: Verify the allocated horse details in cms
        EXPECTED: Allocated horse should be from the below pot - DarkHorse + Small & Nimble+ Nice Price
        """
        pot_id = vec.bma.EXPECTED_FREE_RIDE_POTS.DarkHorseSurpriseMe_SmallNimbleSurpriseMe_NicePriceSurpriseMe
        horses = self.pots[pot_id]['horses']
        horses_list = []
        for horse in horses:
            horses_list.append(horse['horseName'])
        results = self.site.free_ride_overlay.results_container.split('\n')
        actual_horse = results[1]
        self.assertIn(actual_horse, horses_list, msg=f'Actual horse "{actual_horse}" is not'
                                                     f' in the Expected list "{horses_list}"')
