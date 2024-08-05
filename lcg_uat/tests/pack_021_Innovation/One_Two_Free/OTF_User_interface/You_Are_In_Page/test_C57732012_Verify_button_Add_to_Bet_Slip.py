import pytest
import tests
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common
from time import sleep


# @pytest.mark.lad_stg2 # one two free is not available in lower env
# @pytest.mark.lad_tst2 # one two free is not available in lower env
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.one_two_free
@pytest.mark.other
@vtest
class Test_C57732012_Verify_button_Add_to_Bet_Slip(Common):
    """
    TR_ID: C57732012
    NAME: Verify button 'Add to Bet Slip'
    DESCRIPTION: This test case verifies 'Add to Slip' button
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: for Qubit version (deprecated) https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: for Oxygen version: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. User on 'Current Tab'
    PRECONDITIONS: 2. Events with 3 markets configured
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: user logged in
        """
        self.site.login(tests.settings.betplacement_user)
        self.navigate_to_page('1-2-free')

    def test_001_set_scores_and_tap_on_submit_button_on_current_tab(self):
        """
        DESCRIPTION: Set scores and Tap on 'Submit' button on 'Current Tab'
        EXPECTED: - 'You are in' page opened successfully
        EXPECTED: - Upsell Market options displayed
        """
        one_two_free = self.site.one_two_free
        wait_for_result(lambda: one_two_free.one_two_free_welcome_screen.play_button.is_displayed(),
                        timeout=15)
        one_two_free.one_two_free_welcome_screen.play_button.click()
        submit_button = wait_for_result(lambda:
                                        one_two_free.one_two_free_current_screen.submit_button.is_enabled(
                                            expected_result=True),
                                        timeout=15)
        self.assertTrue(submit_button, msg='"Submit Button" is not active')
        match = list(one_two_free.one_two_free_current_screen.items_as_ordered_dict.values())
        for score in match:
            score_switchers = score.score_selector_container.items
            for score_switcher in score_switchers:
                self.assertTrue(score_switcher.increase_score_up_arrow.is_displayed(),
                                msg=f'Upper arrow not displayed for "{score.name}".')
                score_switcher.increase_score_up_arrow.click()
                sleep(1)
                actual_score = score_switcher.score
                self.assertEqual(actual_score, '1',
                                 msg=f'Actual Score "{actual_score}" is not the same as expected "1"')
                break

        self.assertTrue(submit_button, msg='"Submit Button" is not active')
        one_two_free.one_two_free_current_screen.submit_button.click()
        self.__class__.one_two_free_you_are_in = one_two_free.one_two_free_you_are_in
        self.assertTrue(self.one_two_free_you_are_in, msg=f'"1-2 free you are in" is not displayed')
        self.assertTrue(self.one_two_free_you_are_in.items_as_ordered_dict,
                        msg=f'Upsell Market options is not displayed')

    def test_002_tap_on_add_to_slip_button_for_any_of_the_available_upsell_markets(self):
        """
        DESCRIPTION: Tap on 'Add to Slip' button for any of the available UpSell markets
        EXPECTED: - "One-Two-Free" widget is closed
        EXPECTED: - Betslip opened in the same window
        EXPECTED: (eg. https://m.ladbrokes.com/en-gb/?externalSelectionId=670266374,670338200,670266442#!slip)
        EXPECTED: - User see Bets in Betslip according to selected market (check market and selections in the POST predictions response)
        """
        list(self.one_two_free_you_are_in.items_as_ordered_dict.values())[0].add_to_betslip_button.click()
        betslip_sections = wait_for_result(lambda: self.get_betslip_content().betslip_sections_list,
                                           timeout=1,
                                           name='Betslip sections to load')
        self.assertTrue(self.site.has_betslip_opened(),
                        msg='"Betslip not opened and One-Two-Free" widget is not closed')
        self.assertTrue(len(betslip_sections) > 0, msg='No bets found')
        result = vec.betslip.MULTIPLES in betslip_sections
        self.assertEqual(result, True,
                         msg=f'Multiples presence status "{result}" is not the same as expected "{True}"')
