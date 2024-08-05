import pytest
import tests
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common
from time import sleep


# @pytest.mark.lad_stg2 # one two free is not available in lower env
# @pytest.mark.lad_tst2 # one two free is not available in lower env
@pytest.mark.desktop
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.one_two_free
@pytest.mark.other
@vtest
class Test_C57732105_Verify_displaying_of_YAI_page_Desktop__Tablet(Common):
    """
    TR_ID: C57732105
    NAME: Verify displaying of YAI page [Desktop / Tablet]
    DESCRIPTION: This test case verifies displaying of YAI page [Desktop / Tablet]
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. User Do not have a prediction yet
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: user logged in
        """
        self.site.login(tests.settings.betplacement_user)
        self.navigate_to_page('1-2-free')

    def test_001_make_prediction_and_tap_on_submit_button(self):
        """
        DESCRIPTION: Make prediction and Tap on 'Submit' button
        EXPECTED: YAI page successfully opened and designed according to:
        EXPECTED: https://app.zeplin.io/project/5c471d82d6094838624e7232/dashboard?seid=5d11f9c15259df7049a86104
        """
        one_two_free = self.site.one_two_free
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

    def test_002_tap_on_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap on 'Add to Betslip' button
        EXPECTED: - Upsell selections successfully added to Betslip
        EXPECTED: - YAI should NOT close
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
        self.__class__.multiple_count = betslip_sections.multiple_selections_count

    def test_003_tap_on_add_to_betslip_button_again_for_previously_added_market(self):
        """
        DESCRIPTION: Tap on 'Add to Betslip' button again for previously added market
        EXPECTED: - Upsell selections should NOT duplicates
        EXPECTED: - YAI should NOT close
        """
        list(self.one_two_free_you_are_in.items_as_ordered_dict.values())[0].add_to_betslip_button.click()
        betslip_sections = wait_for_result(lambda: self.get_betslip_content().betslip_sections_list,
                                           timeout=1,
                                           name='Betslip sections to load')
        self.assertEqual(betslip_sections.multiple_selections_count, self.multiple_count,
                         msg=f'Multiples selections count "{betslip_sections.multiple_selections_count}" '
                             f'is not the equal as expected {self.multiple_count}"')

    def test_004_tap_on_back_to_betting_button(self):
        """
        DESCRIPTION: Tap on 'Back to Betting' button
        EXPECTED: - User redirects to the previously opened page
        """
        self.one_two_free_you_are_in.back_to_betting_button.click()
        self.site.wait_content_state('FOOTBALL')