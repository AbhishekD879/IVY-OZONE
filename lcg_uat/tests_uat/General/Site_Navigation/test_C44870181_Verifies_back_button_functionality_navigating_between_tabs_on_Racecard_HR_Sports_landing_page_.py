import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.p2
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44870181_Verifies_back_button_functionality_navigating_between_tabs_on_Racecard_HR_Sports_landing_page_(Common):
    """
    TR_ID: C44870181
    NAME: "Verifies back button functionality navigating between tabs on Racecard ,HR ,Sports landing page "
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: BETA Application is loaded
        PRECONDITIONS: User is on Home page
        """
        self.site.wait_content_state("HomePage")

    def test_001_tap_on_horse_racing_from_sports_ribbon_on_mobile__tablet(self):
        """
        DESCRIPTION: Tap on 'Horse Racing' from Sports ribbon on mobile / Tablet
        EXPECTED: Horse Racing Landing page is loaded with Meeting tab opened by default
        """
        self.navigate_to_page('horse-racing')
        self.site.wait_content_state(state_name='Horseracing')
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Current tab "{current_tab}" is not the same as expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')
        # verifying meetings availability
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Failed to display sections on Horse Racing Landing page')

    def test_002_tap_on__back_button_on_the_header(self):
        """
        DESCRIPTION: tap on '< Back' button on the header
        EXPECTED: User is navigated back to the Home Page
        """
        self.site.back_button.click()
        self.site.wait_content_state("HomePage")

    def test_003_tap_on_horse_racing_from_header_menu_on_desktop(self):
        """
        DESCRIPTION: Tap on 'HORSE RACING' from header menu on Desktop
        EXPECTED: Horse Racing Landing page is loaded with Meeting tab opened by default
        """
        # This step is covered in test step 1

    def test_004_click_on____chvron_on_the_sub_header(self):
        """
        DESCRIPTION: click on ' < ' chvron on the sub header
        EXPECTED: User is navigated back to the Home Page
        """
        # This step is covered in test step 2

    def test_005_repeat_steps_1_4_for_other_racing_events(self):
        """
        DESCRIPTION: Repeat steps 1-4 for other Racing events
        """
        self.navigate_to_page('greyhound-racing')
        self.site.wait_content_state(state_name='Greyhounds')
        current_tab = self.site.greyhound.tabs_menu.current
        if self.brand == 'ladbrokes':
            self.assertEqual(current_tab, vec.racing.RACING_NEXT_RACES_NAME.upper(),
                             msg=f'Current tab "{current_tab}" is not the same as expected "{vec.racing.RACING_NEXT_RACES_NAME.upper()}"')
        else:
            self.assertEqual(current_tab, vec.sb.SPORT_DAY_TABS.today.upper(),
                             msg=f'Current tab "{current_tab}" is not the same as expected "{vec.sb.SPORT_DAY_TABS.today.upper()}"')

    def test_006_tap_on_football_from_sports_ribbon_on_mobile__tablet(self):
        """
        DESCRIPTION: Tap on Football from Sports ribbon on mobile / Tablet
        EXPECTED: Football sports Landing page is loaded with Matches tab expanded by default
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        self.assertEqual(self.site.football.tabs_menu.current.lower(), vec.SB.SPORT_TABS_INTERNAL_NAMES.matches,
                         msg=f'"{vec.SB.SPORT_TABS_INTERNAL_NAMES.matches}" tab is not active by default. Active tab is "{self.site.football.tabs_menu.current}"')

    def test_007_click_on__back_button_on_the_header(self):
        """
        DESCRIPTION: Click on '< Back' button on the header
        EXPECTED: User is navigated back to the Home Page
        """
        self.site.back_button.click()
        self.site.wait_content_state("HomePage")

    def test_008_tap_on_football_from_header_menu_on_desktop(self):
        """
        DESCRIPTION: Tap on 'FOOTBALL' from header menu on Desktop
        EXPECTED: Football Sports Landing Page is loaded with Matches tab opened by default
        """
        # This step is covered in test step 6

    def test_009_click_on____chvron_on_the_sub_header(self):
        """
        DESCRIPTION: click on ' < ' chvron on the sub header
        EXPECTED: User is navigated back to the Home Page
        """
        # This step is covered in test step 7
