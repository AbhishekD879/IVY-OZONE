from time import sleep

import pytest
from selenium.common.exceptions import StaleElementReferenceException
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.helpers import get_inplay_ls_structure
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.other
@pytest.mark.module_ribbon
@pytest.mark.adhoc_suite
@vtest
class Test_C65940566_MRT__Verify_the_Live_Stream_tab_display__Live_now_and_upcoming_section_display_with_price_and_score_updates(
    Common):
    """
    TR_ID: C65940566
    NAME: MRT - Verify the Live Stream tab display - Live now and upcoming section display with price and score updates
    DESCRIPTION: This test case is to verify the Live Stream tab display
                - Live now and upcoming section display with price and score updates
    """
    keep_browser_open = True
    enable_bs_performance_log = True
    mandatory_fields_for_live_stream = \
        {
            'title': 'Live Stream',
            'directiveName': 'LiveStream',
            'internalId': 'tab-live-stream',
            'url': '/home/live-stream',
            'universalSegment': True,
            'devices': {
                'android': True,
                'ios': True,
                'wp': True
            },
            'visible': True
        }
    # other mandatory field "showTabOn" is either 'both' or 'mobtablet'
    msg_for_tab_available = 'Live Stream Tab is already present in CMS but properties are not Proper.' \
                            'we are going to delete Live Stream Tab from CMS,' \
                            ' and Creating new one with proper Properties'
    msg_for_tab_unavailable = 'Live Stream Tab is not available in CMS'

    def get_live_stream_data(self, max_attempts=3, type="liveStream"):
        """ type : 'liveStream', 'upcomingLiveStream' """
        sleep(5)
        data = wait_for_result(lambda: get_inplay_ls_structure(), timeout=10).get(type, {}).get('eventsBySports', {})
        if not data and max_attempts > 0:
            return self.get_live_stream_data(max_attempts=max_attempts - 1)
        return data

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: 1) User should have oxygen CMS access
        PRECONDITIONS: 2) Configuration for module ribbon tab in the cms
        PRECONDITIONS: 2a)  -click on module ribbon tab option from left menu in Main navigation
        PRECONDITIONS: 2b) Click on "+ Create Module ribbon tab" button to create new MRT.
        PRECONDITIONS: 2c) Enter All mandatory Fields and click on save button:
        PRECONDITIONS: -Module ribbon tab title as "live stream"
        PRECONDITIONS: - Select Directive name of "LiveStream" option from dropdown
        PRECONDITIONS: -id as "tab-live-stream"
        PRECONDITIONS: -URL  as "/home/live-stream"
        PRECONDITIONS: -Click on "Create" CTA button
        PRECONDITIONS: 2d)Check and select below required fields in module ribbon tab configuration:
        PRECONDITIONS: -Active
        PRECONDITIONS: -IOS
        PRECONDITIONS: -Android
        PRECONDITIONS: -Windows Phone
        PRECONDITIONS: -Select Show tab on option from dropdown like Both, Desktop ,Mobile/tablet
        PRECONDITIONS: -Select radiobutton either Universal or segment(s)           inclusion.
        PRECONDITIONS: -Click on "Save changes" button
        PRECONDITIONS: 3) configuration for event expanded count
        PRECONDITIONS: 3a) System configuration > structure >search in "search for configuration" box as
                            "InPlayCompetitionsExpanded"
        PRECONDITIONS: 3b) Enter field value for "competitionCount" field.
        """
        live_stream_tab = next(
            (tab_data for tab_data in self.cms_config.module_ribbon_tabs.all_tabs_data if
             tab_data['title'].upper() == self.mandatory_fields_for_live_stream['title'].upper()),
            None)

        is_tab_data_meets_criteria = next((False for field in self.mandatory_fields_for_live_stream
                                           if not str(self.mandatory_fields_for_live_stream[field]).upper() == str(live_stream_tab[field]).upper()),
                                          True) if live_stream_tab else False

        is_tab_data_meets_criteria = False if is_tab_data_meets_criteria and not live_stream_tab['showTabOn'] in ['both', 'mobtablet'] else is_tab_data_meets_criteria

        if not is_tab_data_meets_criteria:
            msg = self.msg_for_tab_available if live_stream_tab else self.msg_for_tab_unavailable
            self._logger.info(msg)
            self.cms_config.module_ribbon_tabs.create_tab(
                title=self.mandatory_fields_for_live_stream['title'],
                directive_name=self.mandatory_fields_for_live_stream['directiveName'],
                internal_id=self.mandatory_fields_for_live_stream['internalId'],
                url=self.mandatory_fields_for_live_stream['url'],
                universalSegment=True
            )
            self.cms_config.module_ribbon_tabs._created_tabs.pop()

        system_config = self.get_initial_data_system_configuration()

        in_play_competitions_expanded = system_config.get('InPlayCompetitionsExpanded', {})

        if not in_play_competitions_expanded:
            in_play_competitions_expanded = self.cms_config.get_system_configuration_item('InPlayCompetitionsExpanded')

        self.__class__.expected_max_competitions_expanded = int(in_play_competitions_expanded.get('competitionsCount'))

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should be loaded successfully
        """
        self.site.go_to_home_page()

    def test_002_verify__live_stream_tab_present_in_mrt(self):
        """
        DESCRIPTION: Verify  Live stream tab present in MRT
        EXPECTED: Live stream tab should be present at MRT
        """
        all_tabs = self.site.home.tabs_menu.items_as_ordered_dict
        live_stream_status_in_fe = next((tab for tab_name, tab in all_tabs.items() if
                                         tab_name.upper() == self.mandatory_fields_for_live_stream['title'].upper()),
                                        None)
        self.assertIsNotNone(live_stream_status_in_fe,
                             f'{self.mandatory_fields_for_live_stream["title"]} is not displayed')
        self.__class__.live_stream_tab_fe = live_stream_status_in_fe

    def test_003_click_on_live_stream_tab(self):
        """
        DESCRIPTION: Click on live stream tab
        EXPECTED: Live stream events page need to be open with watch live events count  on the top and followed by the
                  upcoming events count
        """
        self.live_stream_tab_fe.click()
        wait_for_haul(3)
        selected_tab_in_fe = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(self.mandatory_fields_for_live_stream["title"].upper(), selected_tab_in_fe,
                         f'Actual Selected Tab after Clicking on Live Stream is : "{selected_tab_in_fe}" '
                         f'Expected Tab is "Live Stream"')
        # live_now_counter_status = self.site.live_stream.has_live_now_counter()
        # self.assertTrue(live_now_counter_status, f'LIVE NOW counter is not present')

        live_now_tab = self.site.live_stream.live_now_tab
        # self.assertEqual(live_now_tab.text.upper(), vec.inplay.LIVE_NOW_SWITCHER.upper(),
        #                  msg=f'Actual text: "{live_now_tab.text.upper()}" is not same as'
        #                      f'Expected text: "{vec.inplay.LIVE_NOW_SWITCHER.upper()}"')

        upcoming_tab = self.site.live_stream.upcoming_tab
        self.assertEqual(upcoming_tab.text.upper(), vec.inplay.UPCOMING_EVENTS_SECTION.upper(),
                         msg=f'Actual text: "{upcoming_tab.text.upper()}" is not same as'
                             f'Expected text: "{vec.inplay.UPCOMING_EVENTS_SECTION.upper()}"'
                         )
        upcoming_events_counter_status = self.site.live_stream.has_upcoming_counter()
        self.assertTrue(upcoming_events_counter_status, f'UPCOMING EVENT counter is not present')

        tabs_order = ['LIVE NOW', 'UPCOMING EVENTS'] if upcoming_tab.location.get('y') > live_now_tab.location.get(
            'y') else ['UPCOMING EVENTS', 'LIVE NOW']
        self.assertEqual(tabs_order, ['LIVE NOW', 'UPCOMING EVENTS'],
                         msg=f'Order of Tabs is not correct. '
                             f'expected order is : "["LIVE NOW", "UPCOMING EVENTS"]"..'
                             f'Actual order on fe is : "{tabs_order}"')

    def test_004_verify__the_default_expanded_mode_of_sport_in_live_stream_events__page(self):
        """
        DESCRIPTION: verify  the default expanded mode of sport in live stream events  page
        EXPECTED: First sport category need to be in expanded mode and rest need to be in collapsed mode
        """
        self.__class__.live_now_data = self.get_live_stream_data()
        self.softAssert(self.assertTrue, self.live_now_data,
                        msg=f'events are not found for live now in live stream')
        if self.live_now_data:
            sports = self.site.live_stream.live_now.items_as_ordered_dict
            self.assertEqual(len(sports), len(self.live_now_data), f'live now sports length on fe: "{len(sports)}" '
                                                                   f'expected sport length : "{len(self.live_now_data)}"')
            self.__class__.first_sport_name, self.__class__.first_sport = next(iter(list(sports.items())))
            self.assertTrue(self.first_sport.is_expanded(), f'"{self.first_sport_name}" accordian is not expended')
            for sport_name, sport in sports.items():
                if sport_name == self.first_sport_name:
                    continue
                self.assertFalse(sport.is_expanded(), f'"{sport}" accordian is in expended mode.'
                                                      f' but it is not a first sport in the list of sports under '
                                                      f'"LIVE NOW" section')

            self.__class__.default_competitions_displayed = self.first_sport.items_as_ordered_dict
            self.assertLessEqual(len(self.default_competitions_displayed), self.expected_max_competitions_expanded,
                                 f'default events displayed in fe is : "{len(self.default_competitions_displayed)}" is '
                                 f'greater than expected in play competitions count of system configurations in CMS.'
                                 f'Expected competitions displayed is : {self.expected_max_competitions_expanded}')

    def test_005_verify__the_signpostings_for_the_live_events(self):
        """
        DESCRIPTION: Verify  the signposting for the live events
        EXPECTED: Watch live icon should be display
        """
        if self.live_now_data:
            for competition_name, competition in self.default_competitions_displayed.items():
                events = competition.items_as_ordered_dict
                for event_name, event in events.items():
                    self.assertTrue(event.template.has_watch_live_icon(), f'"{competition_name} >> {event_name}" is not have "Watch Live" Icon')
                    if self.brand == "bma":
                        self.assertEqual(event.watch_live_label.upper(), "WATCH LIVE",
                                         f'Actual Label "{event.watch_live_label.upper()}" is not same as'
                                         f'Expected Label "WATCH LIVE" for "{event_name}"')
                    else:
                        self.assertTrue(event.template.is_live_now_event, f'Live Now Label is not available for event : "{event_name}"')

    def test_006_verify_the_expanded_sport_into_collapse_mode(self):
        """
        DESCRIPTION: Verify the expanded sport into collapse mode
        EXPECTED: Displayed events needs to be collapsed with downward chevron icon
        """
        if self.live_now_data:
            self.first_sport.collapse()
            self.assertFalse(self.first_sport.is_expanded(),
                             msg=f'"{self.first_sport_name}" is not collapsed '
                                 f'after clicking on "{self.first_sport_name}"')
            down_arrow = self.first_sport if self.brand != "bma" else self.first_sport.chevron_arrow

            self.assertIsNotNone(down_arrow, 'downward chevron icon is not displayed after sport collapsed')
            for competition_name, competition in self.default_competitions_displayed.items():
                try:
                    status_of_competitions = competition.is_displayed()
                except StaleElementReferenceException:
                    status_of_competitions = False
                self.assertFalse(status_of_competitions, f'"{competition_name}" is displayed after collapsing '
                                                         f'"{self.first_sport_name}"')

    def test_007_verify_the_prize_updates_and_color_changes_in_slp(self):
        """
        DESCRIPTION: Verify the prize updates and color changes in SLP
        EXPECTED: Prizes updates and color changes need to changed
        """
        pass

    def test_008_verify_upcoming_events(self):
        """
        DESCRIPTION: Verify upcoming events
        EXPECTED: It should be in collapse mode by default
        """
        self.__class__.upcoming_events = self.get_live_stream_data(type='upcomingLiveStream')
        self.softAssert(self.assertTrue, self.upcoming_events,
                        msg=f'events are not found for upcoming events in live stream')
        if self.upcoming_events:
            sports = self.site.live_stream.upcoming.items_as_ordered_dict
            self.assertEqual(len(sports), len(self.upcoming_events),
                             msg=f'upcoming sports length on fe: "{len(sports)}" '
                                 f'expected sport length : "{len(self.upcoming_events)}"')
            for sport_name, sport in sports.items():
                self.assertFalse(sport.is_expanded(), f'"{sport_name}" is in expanded mode.')
            self.__class__.first_sport_name, self.__class__.first_sport = next(iter(list(sports.items())))

    def test_009_verify_the_signpostings_for_the_upcoming_events(self):
        """
        DESCRIPTION: Verify the signposting for the upcoming events
        EXPECTED: Watch signposting need to be display
        """
        if self.upcoming_events:
            self.first_sport.expand()
            self.assertTrue(self.first_sport.is_expanded(), f'"{self.first_sport}" is not expanded..')
            self.__class__.default_competitions_displayed = self.first_sport.items_as_ordered_dict
            for competition_name, competition in self.default_competitions_displayed.items():
                events = competition.items_as_ordered_dict
                for event_name, event in events.items():
                    self.assertTrue(event.template.has_watch_live_icon(), f'"{competition_name} >> {event_name}" is not have Watch Icon')
                    self.assertEqual(event.template.watch_live_label.upper(), "WATCH",
                                     f'Actual Label "{event.template.watch_live_label.upper()}" is not same as'
                                     f'Expected Label "WATCH" for {event_name}')

    def test_010_verify_the_expanded_sport_into_collapse_mode(self):
        """
        DESCRIPTION: Verify the expanded sport into collapse mode
        EXPECTED: Displayed events needs to be collapsed with downward chevron icon
        """
        if self.upcoming_events:
            self.first_sport.collapse()
            self.assertFalse(self.first_sport.is_expanded(), f'"{self.first_sport_name}" is not collapsed..')
            down_arrow = self.first_sport if self.brand != "bma" else self.first_sport.chevron_arrow
            self.assertIsNotNone(down_arrow, 'downward chevron icon is not displayed after sport collapsed')
