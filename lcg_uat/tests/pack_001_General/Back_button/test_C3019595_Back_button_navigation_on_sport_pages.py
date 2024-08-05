import pytest
import tests
from tests.base_test import vtest
from selenium.common.exceptions import StaleElementReferenceException
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.mobile_only
@pytest.mark.navigation
@vtest
class Test_C3019595_Back_button_navigation_on_sport_pages(Common):
    """
    TR_ID: C3019595
    NAME: Back button navigation on sport pages
    DESCRIPTION: This test case verifies back button functionality on sports pages, on event details pages and after switching between tabs
    PRECONDITIONS: You should be on a Home page
    """
    keep_browser_open = True

    def clicking_event(self):
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        for section_name, section in list(sections.items()):
            section.expand()
            try:
                events = section.items_as_ordered_dict
            except StaleElementReferenceException:
                sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
                events = sections[section_name].items_as_ordered_dict
            self.assertTrue(events, msg='No events found')
            for event_name, event in list(events.items()):
                event.click()
                break
            break

    def test_001___tap_on_any_sport_in_sports_ribbon_eg_football_basketball__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any sport in sports ribbon (e.g. Football, Basketball)
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to Home page
        """

        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_premier_league_football_event()
        self.site.open_sport(name='FOOTBALL')
        self.site.back_button_click()
        self.site.wait_content_state(state_name='HomePage')

    def test_002___tap_on_any_sport_in_sports_ribbon_and_switch_between_tabs_on_sport_landing_page_eg_in_play_matches_outrights__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any sport in sports ribbon and switch between tabs on sport landing page (e.g In-Play, Matches, Outrights)
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to Home page
        """
        self.site.open_sport(name='FOOTBALL')
        inplay_tab = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play, self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(inplay_tab)
        competitions_tab = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions, self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(competitions_tab)
        self.site.back_button_click()
        self.site.wait_content_state("HomePage")

    def test_003___tap_on_any_sport_in_sports_ribbon_and_open_any_event__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any sport in sports ribbon and open any event
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to the previous page (e.g. sport landing page)
        """
        self.site.open_sport(name='FOOTBALL')
        self.clicking_event()
        self.site.back_button_click()
        self.site.wait_content_state("football")

    def test_004___tap_on_any_sport_in_sports_ribbon_and_open_any_event_and_switch_between_tabs_on_edp_eg_all_markets_main_markets__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any sport in sports ribbon and open any event and switch between tabs on EDP (e.g. All Markets, Main Markets)
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to the previous page (e.g. sport landing page)
        """
        self.clicking_event()
        markets_tabs_list = self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict
        for tab_name, tab in markets_tabs_list.items():
            if not tab.is_selected():
                tab.click()
        self.site.back_button_click()
        self.site.wait_content_state("football")
