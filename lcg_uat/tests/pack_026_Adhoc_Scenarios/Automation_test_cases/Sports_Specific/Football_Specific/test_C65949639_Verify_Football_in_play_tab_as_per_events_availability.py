import pytest
import voltron.environments.constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.helpers import get_inplay_sports_by_section, normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.sports_specific
@pytest.mark.football_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65949639_Verify_Football_in_play_tab_as_per_events_availability(Common):
    """
    TR_ID: C65949639
    NAME: Verify Football in-play tab as per events availability
    DESCRIPTION: This test case verifies Football Inplay tab events  availability
    PRECONDITIONS: 1. Football sport should be
    PRECONDITIONS: configured in CMS
    PRECONDITIONS: 2. The set of markets should be created in OB system using the following marketTemplates:
    PRECONDITIONS: |Match Betting| - "Match Result"
    PRECONDITIONS: |Next Team to Score| - "Next Team to Score"
    PRECONDITIONS: |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score"
    PRECONDITIONS: |Total Goals Over/Under| - "Total Goals Over/Under 1.5"
    PRECONDITIONS: |Total Goals Over/Under| - "Total Goals Over/Under 2.5"
    PRECONDITIONS: |Total Goals Over/Under| - "Total Goals Over/Under 3.5"
    PRECONDITIONS: |Total Goals Over/Under| - "Total Goals Over/Under 4.5"
    PRECONDITIONS: |To Qualify| - "To Qualify"
    PRECONDITIONS: |Penalty Shoot-Out Winner| - "Penalty Shoot-Out Winner"
    PRECONDITIONS: |Extra-Time Result| - "Extra Time Result"
    PRECONDITIONS: |Draw No Bet| - "Draw No Bet"
    PRECONDITIONS: |First-Half Result| - "1st Half Result"
    PRECONDITIONS: 3. Be aware that market switching using 'Market Selector' is applied only for events from the 'Live Now' section.
    """
    keep_browser_open = True
    enable_bs_performance_log = True

    def get_live_event_name(self):
        upcoming_event_ids = get_inplay_sports_by_section(type='LIVE_EVENT').get('eventsByTypeName')[0].get('eventsIds')
        event_id = upcoming_event_ids[0]
        selections = self.ss_req.ss_event_to_outcome_for_event(event_id)
        event_name = normalize_name(selections[0].get('event').get('name'))
        return event_name

    def test_001_launch_application(self):
        """
        DESCRIPTION: Launch application
        EXPECTED: Application should be launched successfully
        """
        # ****************************** Navigating to Home page ************************
        self.site.wait_content_state(state_name="Homepage")
        self._logger.info(f'=====> Launched application and Home page loaded successfully')

    def test_002_navigate_to_football_and_switch_to_inplay__gtlive_now_tab(self):
        """
        DESCRIPTION: Navigate to Football and switch to Inplay--&gt;Live Now tab
        EXPECTED: Desktop and Mobile:
        EXPECTED: Inplay tab should load successfully
        EXPECTED: Under Inplay tab, Live Now and Upcoming sub tabs should be displayed.
        EXPECTED: By default Live now sub tab opened with inplay event count display and first competition  leguea in expanded mode
        EXPECTED: ex: LIVE NOW(*)
        EXPECTED: Event Card body should show with
        EXPECTED: *market switcher
        EXPECTED: *event1 vs event2
        EXPECTED: * fixture headers (home,draw,away)
        EXPECTED: * Odd buttons
        EXPECTED: * Score display in live now section
        EXPECTED: * Favourite icon (Star icon)
        EXPECTED: * Live/watch live labels
        EXPECTED: *Timer (time, HT, FT) in live now section
        EXPECTED: * More markets link
        EXPECTED: *SEE ALL in mobile mode.
        """
        # ****************************** Navigating to Football >> In Play >> LIVE NOW tab ************************
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(vec.siteserve.FOOTBALL_TAB)
        current_tab = self.site.football.tabs_menu.current
        inplay_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                             self.ob_config.football_config.category_id)
        if current_tab.upper() != inplay_tab.upper():
            self.site.football.tabs_menu.click_button(inplay_tab)
        if self.device_type == 'mobile':
            live_now = self.site.football.tab_content.live_now
        else:
            self.site.football.tab_content.grouping_buttons.click_button(vec.inplay.LIVE_NOW_SWITCHER)
        self._logger.info(f'=====> Navigated to Football In Play LIVE NOW tab')
        # ****************************** Verification of Football live events ************************
        live_events = get_inplay_sports_by_section(type='LIVE_EVENT')
        if live_events and live_events.get('eventsIds'):
            number_of_live_events = live_events.get('eventCount')
        else:
            raise SiteServeException(f'There are no live events in football')
        self._logger.info(f'=====> Verified football live events are available')
        # ****************************** Verification of Live Now header with event count ************************
        expected_live_now_tab_header = f'{vec.inplay.LIVE_NOW_SWITCHER} ({number_of_live_events})'.upper()
        if self.device_type != 'mobile':
            live_now_tab = self.site.football.tab_content.grouping_buttons.items_as_ordered_dict.get(
                vec.inplay.LIVE_NOW_SWITCHER)
            actual_live_now_tab_header = f'{live_now_tab.name} ({live_now_tab.counter})'.upper()

            self.assertEqual(expected_live_now_tab_header, actual_live_now_tab_header,
                            msg=f'Expected live now header is {expected_live_now_tab_header}'
                             f'but Actual is  {actual_live_now_tab_header}')
        self._logger.info(f'=====> Verified Live Now header with event count')
        # ****************************** Verification of Market Selector ************************
        has_market_selector = self.site.football.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg='"Market selector" is not available under Football live now tab')
        self._logger.info(f'=====> Market Selector verified successfully')
        # ****************************** Verification of Fixture Headers ************************
        sections = wait_for_result(
            lambda: self.site.football.tab_content.accordions_list.items_as_ordered_dict.values(), timeout=120)
        self.assertTrue(sections, msg='event is not available')
        actual_header1 = list(sections)[0].fixture_header.header1.upper()
        actual_header2 = list(sections)[0].fixture_header.header2.upper()
        actual_header3 = list(sections)[0].fixture_header.header3.upper()
        self.assertEqual(actual_header1, vec.sb.HOME,
                         msg=f'actual fixture header name {actual_header1} not equal to expected fixture header name {vec.sb.HOME}')
        self.assertEqual(actual_header2, vec.sb.DRAW,
                         msg=f'actual fixture header name {actual_header2} not equal to expected fixture header name {vec.sb.DRAW}')
        self.assertEqual(actual_header3, vec.sb.AWAY,
                         msg=f'actual fixture header name {actual_header3} not equal to expected fixture header name {vec.sb.AWAY}')
        self._logger.info(f'=====> Verified fixture header')
        # ****************************** Verification of event1 vs event2 ******************************
        expected_event_name = self.get_live_event_name().upper()
        events = list(sections)[0].items_as_ordered_dict.values()
        self.assertTrue(events, msg='leagues are not available')
        first_event = list(events)[0]
        actual_event_name = first_event.template.name.upper()
        self.assertEqual(actual_event_name, expected_event_name,
                         msg=f'actual event name {actual_event_name} is not equal to '
                             f'expected event name {expected_event_name}')
        self._logger.info(f'=====> Verified event name')
        # ****************************** Verification of odd buttons ******************************
        self.assertTrue(len(first_event.template.items_names) is not 0,
                        msg=f'odd buttons is not present for event {actual_event_name}')
        self._logger.info(f'=====> Verified Odds buttons for event')
        # ****************************** Verification of Live Score ******************************
        self.assertTrue(len(first_event.template.score_table.items_names) is not 0,
                        msg=f'Live Score is not present for event {actual_event_name}')
        self._logger.info(f'=====> Verified Live Score for event')
        # ****************************** Verification of Favourite Icon ******************************
        if self.brand == 'bma':
            self.assertTrue(first_event.template.favourite_icon,
                            msg=f'Favourite Icon is not present for event {actual_event_name}')
            self._logger.info(f'=====> Verified Favourite Icon for event')
        # ****************************** Verification of Live/Watch Live ******************************
        self.assertTrue(first_event.template.is_live_now_event,
                        msg=f'Live/Watch Live not present for event {actual_event_name}')
        self._logger.info(f'=====> Verified Live/Watch Live')
        # ****************************** Verification of Event Time ******************************
        self.assertTrue(first_event.template.event_time is not None,
                        msg=f'Event time is not present for event {actual_event_name}')
        self._logger.info(f'=====> Verified event time')
        # ****************************** Verification of More Markets link ******************************
        self.assertTrue(first_event.template.more_markets_link,
                        msg=f'More Markets Link is not present for event {actual_event_name}')
        self._logger.info(f'=====> Verified More Markets Link')

    def test_003_verify_the_display_of_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify the display of Market selector drop down.
        EXPECTED: Desktop:
        EXPECTED: The 'Market Selector' is displayed below the 'Live Now' (n) switcher
        EXPECTED: 'Main Markets' option is selected by default
        EXPECTED: 'Change Market' button is placed next to  'Main Markets' name with the chevron pointing downwards (for Ladbrokes)
        EXPECTED: 'Market' title is placed before 'Main Markets' name and the chevron pointing downwards is placed at the right side of dropdown (for Coral)
        EXPECTED: Mobile:
        EXPECTED: The 'Market Selector' is displayed below the 'Live Now (n)' header
        EXPECTED: 'Main Markets' option is selected by default
        EXPECTED: 'Change' button is placed next to 'Main Markets' name with the chevron pointing downwards and list of markets will be displayed.
        """
        # ****************************** Verification of Default Selected Market ************************
        if self.device_type == 'mobile':
            default_selected_market_name = self.site.football.tab_content.dropdown_market_selector.items_names[0].upper()
        else:
            default_selected_market_name = self.site.football.tab_content.selected_market_name.upper()
        expected_market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.main_markets.upper()
        self.assertEqual(default_selected_market_name, expected_market_name, msg=f'Expected default market name is {expected_market_name} but actual market name is {default_selected_market_name}')
        self._logger.info(f'=====> Verified default selected market name is {default_selected_market_name}')

    def test_004_verify_live_now_accordians_in_collapsable_and_expandable_mode(self):
        """
        DESCRIPTION: Verify live now accordians in collapsable and expandable mode
        EXPECTED: Live now  accordians should be collapsable and expandable
        """
        # ****************************** Verify of accordions are expandable and Collapsable  ************************
        self.__class__.all_sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        sections = self.all_sections.values()
        sections = list(sections)[:5] if len(list(sections)) > 5 else list(sections)
        for section in sections:
            if section.is_expanded():
                section.collapse()
                self.assertFalse(section.is_expanded(), msg=f'Accordian is not collapsed')
                section.expand()
                self.assertTrue(section.is_expanded(), msg=f'Accordian is not expanded')
            else:
                section.expand()
                self.assertTrue(section.is_expanded(), msg=f'Accordian is not expanded')
                section.collapse()
                self.assertFalse(section.is_expanded(), msg=f'Accordian is not collapsed')
        self._logger.info(f'=====> Verified accordions are expandable and Collapsable')

    def test_005_for_mobileverify_see_all_link_navigation(self):
        """
        DESCRIPTION: For Mobile:
        DESCRIPTION: Verify SEE ALL Link navigation.
        EXPECTED: Mobile:
        EXPECTED: On clicking SEE ALL link should navigate to
        EXPECTED: respective competitions details page
        """
        # ****************************** Verification of See All link ************************
        if self.device_type == 'mobile':
            section_name, section = next(((section_name.upper(), section) for section_name, section in self.all_sections.items() if section_name is not None), (None, None))
            self.site.football.tab_content.dropdown_market_selector.click()
            section.group_header.see_all_link.click()
            self.site.wait_content_state('CompetitionLeaguePage')
            actual_section_name = self.site.competition_league.title_section.type_name.name.upper()
            self.assertEqual(section_name, actual_section_name, msg=f'Expected section name is {section_name} but Actual is {actual_section_name}')
            self._logger.info(f'=====> Verified SEE ALL link for mobile')
