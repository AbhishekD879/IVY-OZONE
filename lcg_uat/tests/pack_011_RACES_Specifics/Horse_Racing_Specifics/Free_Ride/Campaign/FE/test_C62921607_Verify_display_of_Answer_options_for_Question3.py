import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
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
class Test_C62921607_Verify_display_of_Answer_options_for_Question3(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C62921607
    NAME: Verify display of Answer options for Question3
    DESCRIPTION: This test case verifies display of Answer options for Question3
    PRECONDITIONS: CMS 1: Campaign should be created and in currently running status
    PRECONDITIONS: 2: First ,Second and Third questions with Answer options(Option1, Option2 and option3) are configured
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: CMS 1: Campaign should be created and in currently running status
        PRECONDITIONS: 2: First ,Second and Third questions with Answer options(Option1, Option2 and option3) are configured
        """
        username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=username)
        self.update_spotlight_events_price(class_id=223)
        self.cms_config.check_update_and_create_freeride_campaign()
        self.site.login(username=username)

    def test_001_Login_to_Ladbrokes_Application_with_eligible(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible
        EXPECTED: - User should be able to login successfully
        """
        # Note:- Covered in preconditions

    def test_002_Click_on_Launch_Free_Ride_Banner(self):
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

    def test_005_Select_Answer_for_Second_question(self):
        """
        DESCRIPTION: Select Answer for Second question
        EXPECTED: Selected Answer should be displayed below to Step 2 of 3
        """
        second_question = wait_for_result(lambda: self.site.free_ride_overlay.second_question is not None,
                                          timeout=10, name='Waiting for second Question to be displayed')
        self.assertTrue(second_question,
                        msg='Second question is not displayed below to step 2 of 3')
        answers = wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                                  timeout=20, name='Waiting for options to be displayed')
        self.assertTrue(answers,
                        msg='Answers are not displayed for second question')
        options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.values())
        options[0].click()

    def test_006_Verify_display_of_Third_Question(self):
        """
        DESCRIPTION: Verify display of Third Question
        EXPECTED: Third Question should be displayed in Free Ride Overlay screen
        """
        third_question = wait_for_result(lambda: self.site.free_ride_overlay.third_question is not None,
                                         timeout=10, name='Waiting for third Question to be displayed')
        self.assertTrue(third_question,
                        msg='Third question is not displayed in overlay')

    def test_007_Verify_display_of_Answer_Options_for_Third_Question(self):
        """
        DESCRIPTION: Verify display of Answer Options for Third Question
        EXPECTED: Answer Options should be displayed below to Step 3 of 3 as below
        EXPECTED: Good Chance
        EXPECTED: Nice price
        EXPECTED: Surprise Me!
        EXPECTED: Note: 3 options are configured in CMS
        """
        answers = wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                                  timeout=20, name='Waiting for options to be displayed')
        self.assertTrue(answers,
                        msg='Answers are not displayed for third question')
        actual_options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.keys())
        expected_list = [vec.free_ride.OPTIONS_LIST.good_chance,
                         vec.free_ride.OPTIONS_LIST.nice_price,
                         vec.free_ride.OPTIONS_LIST.surprise_me]
        self.assertListEqual(list1=actual_options, list2=expected_list,
                             msg=f'Actual List "{actual_options}" is not same as'
                                 f'Expected List "{expected_list}".')