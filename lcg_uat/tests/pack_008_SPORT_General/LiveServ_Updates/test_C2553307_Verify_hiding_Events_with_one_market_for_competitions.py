import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.market_selector
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.cms
@pytest.mark.competitions
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C2553307_Verify_Event_Hiding_On_Competitions(BaseSportTest):
    """
    TR_ID: C2553307
    NAME: Verify hiding Events with one market depending on Displayed attribute for selections on Competitions
    DESCRIPTION: This test case verifies hiding Events with one market depending on 'Displayed' attribute for selections
    PRECONDITIONS: 1. To display/undisplay event/market/selection use http://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. To verify 'Displayed' attribute value check Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket
    PRECONDITIONS: 3. Create event that has only ONE market
    PRECONDITIONS: *NOTE:* *LiveServe pushes with updates also are received if selection is added to the betslip*
    """
    keep_browser_open = True
    market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default
    market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.to_qualify
    market_short_name = 'to_qualify'
    league = None

    def get_events_present_on_competitions_tab(self, section_name):
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found on page')
        self.assertIn(section_name, sections.keys(), msg=f'Section name "{section_name}"  is not found in "{", ".join(sections.keys())}')
        section = sections[section_name]
        self.assertTrue(section, msg=f'Section "{section_name}" is not found in "{", ".join(sections.keys())}')
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg='No event groups found on page')
        return events

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football event
        """
        self.ob_config.add_football_event_to_special_league()
        event = self.ob_config.add_football_event_to_special_league(
            markets=[(self.market_short_name, {'cashout': True})])
        self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = event.team1, event.team2, event.selection_ids
        self.__class__.event_name = f'{self.team1} v {self.team2}'
        market_short_name = self.ob_config.football_config. \
            autotest_class.special_autotest_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.ob_config.change_market_state(event_id=event.event_id,
                                           market_id=self.ob_config.market_ids[event.event_id][market_short_name],
                                           displayed=False, active=True)
        self._logger.info(f'*** Created Football event "{self.event_name}"')

    def test_002_tap_football_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap Football icon from the sports ribbon
        EXPECTED: * Football landing page is opened
        EXPECTED: * 'Today' tab is selected
        EXPECTED: * Events for current day are displayed
        EXPECTED: * Match Result value is selected by default in the Market Selector
        """
        self.site.open_sport(name='FOOTBALL')

        if self.device_type == 'desktop':
            market_dropdown = self.site.football.tab_content.dropdown_market_selector.selected_market_selector_item
            expected_result = self.market_selector_default_value.upper() if self.brand == 'ladbrokes' else self.market_selector_default_value
            self.assertEqual(market_dropdown, expected_result,
                             msg=f'"{expected_result}" value is not selected by default.'
                             f' Market selector value: "{market_dropdown}"')
        else:
            market_dropdown = self.site.football.tab_content.dropdown_market_selector
            self.assertEqual(market_dropdown.value, self.market_selector_default_value,
                             msg=f'"{self.market_selector_default_value}" value is not selected by default. '
                             f'Market selector value: "{market_dropdown.value}"')

    def test_003_tap_competition(self):
        """
        DESCRIPTION: Tap on Competition Module header
        """
        expected_sport_tab = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                    self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competition tab is not active, active is "{active_tab}"')

    def test_004_choose_market_and_verify_event_with_particular_market_is_available_on_the_page(self):
        """
        DESCRIPTION: Choose market from Preconditions in the Market Selector and make sure that only ONE event with
        particular market is available on the page
        EXPECTED: * Selected Market is displayed in Market selector
        EXPECTED: * Created event is displayed for selected market
        """
        self.site.wait_content_state_changed()
        self.__class__.today_section_name = vec.sb.TABS_NAME_TODAY.title() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else vec.sb.TABS_NAME_TODAY

        if self.device_type == 'desktop':
            self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[vec.sb_desktop.COMPETITIONS_SPORTS].click()
            competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        else:
            competitions = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
        self.assertTrue(competitions, msg='No competitions are present on page')
        self.__class__.competition = tests.settings.football_autotest_competition.title() if \
            self.brand == 'ladbrokes' and self.device_type == self.device_type == 'desktop' else tests.settings.football_autotest_competition
        self.assertIn(self.competition, competitions.keys())
        competition = competitions[self.competition]
        competition.expand()
        leagues = wait_for_result(lambda: competition.items_as_ordered_dict,
                                  name='Leagues list is loaded',
                                  timeout=5)
        competition_league = tests.settings.football_autotest_competition_special_league.title()
        self.assertTrue(leagues, msg='No leagues are present on page')
        self.assertTrue(competition_league in leagues,
                        msg=f'League "{competition_league}" is not found in "{leagues.keys()}"')
        self.__class__.league = leagues[competition_league]
        self.league.click()
        self.site.wait_content_state_changed()
        market_dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        market_dropdown.items_as_ordered_dict[self.market_name].click()
        if self.device_type == 'desktop':
            market_dropdown = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
            wait_for_result(lambda: self.market_name in market_dropdown, timeout=2)
            expected_name = self.market_name.upper() if self.brand == 'ladbrokes' else self.market_name
            self.assertEqual(market_dropdown, expected_name,
                             msg=f'"{expected_name}"" is not displayed in Market selector. '
                             f'Market selector value: "{market_dropdown}"')
        else:
            market_dropdown = self.site.competition_league.tab_content.dropdown_market_selector
            wait_for_result(lambda: self.market_name in market_dropdown.value, timeout=1)
            self.assertEqual(market_dropdown.value, self.market_name,
                             msg=f'"{self.market_name}"" is not displayed in Market selector. '
                             f'Market selector value: "{market_dropdown.value}"')
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        today_section = sections.get(self.today_section_name, None)
        self.assertTrue(today_section, msg=f'No events found in "{self.today_section_name}" section')
        events = today_section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found in section')
        placed_event = events.get(self.event_name)
        self.assertTrue(placed_event, msg=f'Event "{self.event_name}" is not displayed. Displayed events are "{events.keys()}"')
        events = self.get_events_present_on_competitions_tab(section_name=self.today_section_name)
        self.assertIn(self.event_name, events.keys(),
                      msg=f'Event "{self.event_name}" is not displaying in {events.keys()}')

    def test_005_in_ti_tool_undisplay_selections_for_the_event_from_preconditions_and_save_changes(self):
        """
        DESCRIPTION: In TI tool undisplay selections for the event from preconditions and save changes
        """
        self.ob_config.change_selection_state(self.selection_ids['to_qualify'][self.team1], displayed=False,
                                              active=True)
        self.ob_config.change_selection_state(self.selection_ids['to_qualify'][self.team2], displayed=False,
                                              active=True)

    def test_006_verify_market_selector(self):
        """
        DESCRIPTION: Verify Market Selector
        EXPECTED: * Chosen market stops to display within the Market selector
        EXPECTED: * Default value starts to display within the Market selector
        EXPECTED: * Events for default market starts to display on the page
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state_changed()
        if self.device_type == 'desktop':
            market_dropdown = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
            expected_result = self.market_selector_default_value.upper() if self.brand == 'ladbrokes' else self.market_selector_default_value
            self.assertEqual(market_dropdown, expected_result,
                             msg=f'Current value in Market selector "{market_dropdown}" is not the same as '
                             f'expected default value "{expected_result}"')
        else:
            market_dropdown = self.site.competition_league.tab_content.dropdown_market_selector
            self.assertEqual(market_dropdown.value, self.market_selector_default_value,
                             msg=f'Current value in Market selector "{market_dropdown.value}" is not the same as '
                             f'expected default value "{self.market_selector_default_value}"')

        events = self.get_events_present_on_competitions_tab(section_name=self.today_section_name)
        self.assertFalse(self.event_name in events.keys(),
                         msg=f'Event "{self.event_name}" is displaying in {events.keys()}')

    def test_007_in_ti_tool_display_selections_for_the_event_from_preconditions_and_save_changes(self):
        """
        DESCRIPTION: In TI tool display selections for the event from preconditions and save changes
        EXPECTED: Changes are saved successfully
        """
        self.ob_config.change_selection_state(self.selection_ids['to_qualify'][self.team1], displayed=True,
                                              active=True)
        self.ob_config.change_selection_state(self.selection_ids['to_qualify'][self.team2], displayed=True,
                                              active=True)

    def test_008_verify_event_not_displaying(self):
        """
        DESCRIPTION: Go to Oxygen application and verify event displaying
        EXPECTED: event does NOT start to display in real time
        """
        events = self.get_events_present_on_competitions_tab(section_name=self.today_section_name)
        self.assertFalse(self.event_name in events.keys(),
                         msg=f'Event "{self.event_name}" start to display in real time in {events.keys()}')

    def test_009_refresh_the_page_and_verify_the_event_displaying(self):
        """
        DESCRIPTION: Refresh the page and verify the event displaying
        DESCRIPTION: Verify Market Selector
        EXPECTED: Market for event from the previous steps is visible within Market Selector
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('CompetitionLeaguePage')
        self.site.wait_content_state_changed()
        market_dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        market_dropdown.items_as_ordered_dict[self.market_name].click()
        if self.device_type == 'desktop':
            market_dropdown = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
            wait_for_result(lambda: self.market_name in market_dropdown, timeout=1)
            expected_name = self.market_name.upper() if self.brand == 'ladbrokes' else self.market_name
            self.assertEqual(market_dropdown, expected_name,
                             msg=f'Current value in Market selector "{market_dropdown}" is not the same as '
                             f'expected default value "{expected_name}"')
        else:
            market_dropdown = self.site.competition_league.tab_content.dropdown_market_selector
            wait_for_result(lambda: self.market_name in market_dropdown.value, timeout=1)
            self.assertEqual(market_dropdown.value, self.market_name,
                             msg=f'Current value in Market selector "{market_dropdown.value}" is not the same as '
                             f'expected default value "{self.market_selector_default_value}"')
        events = self.get_events_present_on_competitions_tab(section_name=self.today_section_name)
        self.assertIn(self.event_name, events.keys(),
                      msg=f'Event "{self.event_name}" is not displaying in {events.keys()}')
