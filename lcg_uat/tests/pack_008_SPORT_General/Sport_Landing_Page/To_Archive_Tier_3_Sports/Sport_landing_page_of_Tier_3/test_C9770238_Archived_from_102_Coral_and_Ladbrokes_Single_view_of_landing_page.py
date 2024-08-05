import pytest
import voltron.environments.constants as vec
import tests
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.frequent_blocker
@vtest
class Test_C9770238_Archived_from_102_Coral_and_Ladbrokes_Single_view_of_landing_page(Common):
    """
    TR_ID: C9770238
    NAME: [Archived from 102 Coral and Ladbrokes] Single view of landing page
    DESCRIPTION: This test case verifies the Tier 3 Sport landing page content
    DESCRIPTION: **It will be archived from 102 Coral and Ladbrokes**
    PRECONDITIONS: The list of sports that are tier I/II/III is available here: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs
    PRECONDITIONS: Oxygen app is running
    PRECONDITIONS: User is on home page
    """
    keep_browser_open = True
    expected_date_tabs_list = [vec.sb.TABS_NAME_TODAY, vec.sb.TABS_NAME_TOMORROW, vec.sb.TABS_NAME_FUTURE]
    expected_modules_list = [vec.sb.IN_PLAY.upper(), vec.sb.MATCHES.upper(), vec.sb.OUTRIGHTS.upper(),
                             vec.sb.TABS_NAME_COMPETITIONS.upper(), vec.sb.TABS_NAME_SPECIALS.upper(),
                             vec.sb.TABS_NAME_COUPONS, vec.sb.TABS_NAME_RESULTS, vec.bma.GAME.upper()]

    def test_001_click_on_sport_icon_of_tier_3_type_sport_in_menu_ribbon(self):
        """
        DESCRIPTION: Click on sport icon of Tier 3 type sport in menu ribbon
        EXPECTED: User is redirected to <sport> single view page
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_hockey_event_to_olympics_specials(
                start_time=self.get_date_time_formatted_string(hours=2))
            self.ob_config.add_hockey_event_to_olympics_specials(
                start_time=self.get_date_time_formatted_string(days=1, hours=2))
            self.ob_config.add_baseball_event_to_autotest_league(
                start_time=self.get_date_time_formatted_string(hours=2))
            self.ob_config.add_baseball_event_to_autotest_league(
                start_time=self.get_date_time_formatted_string(days=1, hours=2))

        self.site.wait_content_state('Homepage')
        self.navigate_to_page('sport/hockey')
        try:
            self.site.wait_content_state('hockey')
        except VoltronException:
            current_url = self.device.get_current_url()
            if 'sport/hockey' not in current_url:
                raise SiteServeException('No events available for hockey sport')

    def test_002_check_the_view_of_landing_page(self):
        """
        DESCRIPTION: Check the view of landing page
        EXPECTED: - sub tabs 'Today/Tomorrow/Future' are available
        EXPECTED: - All events are displayed in separate modules like: In-Play/Upcoming/Outright/Specials/Coupons/etc. (if available)
        EXPECTED: - Types accordions (Each Type should act as a separate header i.e. La Liga below last Premier league event)
        EXPECTED: - Events with standard event cards
        EXPECTED: - If no events are available for the definite section than message 'No events found' is displayed
        EXPECTED: - 'See all' links are displayed on the single view page as user should see all the available events on one page.
        """
        leagues = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        date_tab_title = list(leagues.values())[0].fixture_header.date.text
        self.assertIn(date_tab_title, self.expected_date_tabs_list,
                      msg=f'Date tab: "{date_tab_title}" is not present in the expected list: "{self.expected_date_tabs_list}"')
        modules = self.site.sports_page.tabs_menu.items_names
        for module in modules:
            self.assertIn(module, self.expected_modules_list,
                          msg=f'Actual module: "{module}" is not present in the modules list: "{self.expected_modules_list}"')
        for i in range(len(list(leagues.keys()))):
            self.assertTrue(list(leagues.values())[i], msg='Each Type is not acting as a separate header')
        if not self.site.sports_page.tab_content.has_no_events_label():
            events = wait_for_result(lambda: leagues[list(leagues.values())[0].name].items_as_ordered_dict, timeout=5)
            self.assertTrue(events, msg=f'No events found for the league: "{list(leagues.values())[0].name} and No events lable is not present"')
        else:
            self._logger.info('No events lable is present as No events are available')
        if not list(leagues.values())[0].group_header.has_see_all_link():
            self._logger.info('See all link is not displayed')

    def test_003_navigate_to_another_tier_3_sport(self):
        """
        DESCRIPTION: Navigate to another tier 3 sport
        EXPECTED: Same view is displayed as described above
        """
        self.navigate_to_page('sport/baseball')
        try:
            self.site.wait_content_state(state_name='Baseball')
        except VoltronException:
            current_url = self.device.get_current_url()
            if 'sport/baseball' not in current_url:
                raise SiteServeException('No events available for baseball sport')
        self.test_002_check_the_view_of_landing_page()
