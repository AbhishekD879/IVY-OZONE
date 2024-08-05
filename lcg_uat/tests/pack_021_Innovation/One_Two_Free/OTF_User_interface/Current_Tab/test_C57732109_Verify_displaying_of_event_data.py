import pytest
import tests
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.Common import Common


# @pytest.mark.lad_stg2 # one two free is not available in lower env
# @pytest.mark.lad_tst2 # one two free is not available in lower env
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.one_two_free
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.reg156_fix
@vtest
class Test_C57732109_Verify_displaying_of_event_data(Common):
    """
    TR_ID: C57732109
    NAME: Verify displaying of event data
    DESCRIPTION: This test case verifies displaying of event data
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. User expands '1-2-Free' section in the left menu
    PRECONDITIONS: 3. User opens 'Game view'
    PRECONDITIONS: 4. User open Detail View for existing game
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: logged in with ladbrokes
        PRECONDITIONS: navigate to '1-2-free' page
        EXPECTED:'1-2-free' page should be displayed
        """
        username = tests.settings.betplacement_user
        self.site.login(username)
        self.navigate_to_page('1-2-free')
        if self.device_type == 'mobile':
            self.assertTrue(self.site.one_two_free.one_two_free_welcome_screen.is_displayed(timeout=5),
                        msg='1-2-Free welcome screen is not shown')

    def test_001_populate_events_information_with_valid_data_and_save_it(self):
        """
        DESCRIPTION: Populate Events information with valid data and save it
        EXPECTED: All changes are saved successfully
        """
        cms_games_tab_details = self.cms_config.get_one_two_free_games_tab_details()[0]
        self.assertTrue(cms_games_tab_details,
                        msg=f'CMS games data is available.')

    def test_002_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: All data retrieved from CMS and displayed
        EXPECTED: Event block consist:
        EXPECTED: - Match Number
        EXPECTED: - Kick off time (Time format: 17:30 SAT, 19:30 SAT, 16:00 SUN)
        EXPECTED: - Score predictions arrows
        EXPECTED: - Teams t-shirts
        EXPECTED: - Teams names
        EXPECTED: - TV icon
        """
        one_two_free = self.site.one_two_free
        if self.device_type == 'mobile':
            wait_for_result(lambda: one_two_free.one_two_free_welcome_screen.play_button.is_displayed(),
                            timeout=15)
            one_two_free.one_two_free_welcome_screen.play_button.click()
        submit_button = wait_for_result(lambda:
                                        one_two_free.one_two_free_current_screen.submit_button.is_enabled(
                                            expected_result=True),
                                        timeout=15)
        self.assertTrue(submit_button, msg='"Submit Button" is not active')
        matches = list(one_two_free.one_two_free_current_screen.items_as_ordered_dict.values())
        for match in matches:
            self.assertTrue(match.match_start_date,
                            msg=f'match start time is not displayed for "{match.name}".')
            for shirt in list(match.items_as_ordered_dict.values()):
                self.assertTrue(shirt.silk_icon.is_displayed(),
                                msg=f' Teams t-shirts not displayed for "{match.name}".')
                self.assertTrue(shirt.name,
                                msg=f'Team names not displayed for "{match.name}".')

            score_switchers = match.score_selector_container.items
            for score_switcher in score_switchers:
                self.assertTrue(score_switcher.increase_score_up_arrow.is_displayed(),
                                msg=f'Upper arrow not displayed for "{match.name}".')
                self.assertTrue(score_switcher.decrease_score_down_arrow.is_displayed(),
                                msg=f'Down arrow not displayed for "{match.name}".')
                self.assertTrue(score_switcher.score,
                                msg=f'Score is not displayed for "{match.name}".')
