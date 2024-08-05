from time import sleep

import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C44870196_Landing_page_displays_races_under_different_tabs_and_each_tab_respect_display_rules_under_Type_areas_are_expandable_meetings_carousel_are_scrollable_and_user_can_see_the_race_status_and_add_selections_to_bet_slip_as_per_requirements_GDs_Verify_Co(BaseRacing):
    """
    TR_ID: C44870196
    NAME: Landing page displays races under different tabs and each tab respect display rules under Type, areas are expandable, meetings carousel are scrollable and user can see the race status and add selections to bet slip as per requirements/GDs-Verify Co
    DESCRIPTION: "Landing page displays races under different tabs and each tab respect display rules under Type, areas are expandable, meetings carousel are scrollable and user can see the race status and add selections to bet slip as per requirements/GDs
    DESCRIPTION: -Verify Collapse/Expandable accordion
    DESCRIPTION: User is able to switch between the tabs or navigate back. to race landing page
    DESCRIPTION: Verify that the data is correct and completely displayed.
    DESCRIPTION: Verify the Components of the race card
    DESCRIPTION: -Each slide/event/card in the carousel will have below components
    DESCRIPTION: -Header with the Name, Time and More link navigating the user to the specific race card.
    DESCRIPTION: -E/W terms
    DESCRIPTION: -Display all selections with the silks and details same as production
    DESCRIPTION: -Display runners in chronological order
    DESCRIPTION: -Display unnamed favourite
    DESCRIPTION: -Watch Icon when the stream is available."
    PRECONDITIONS: App/Site is loaded
    PRECONDITIONS: User is on the Horse racing page
    """
    keep_browser_open = True
    section_skip_list = ['VIRTUAL RACING', 'VIRTUAL RACE CAROUSEL', 'ENHANCED RACES', 'NEXT RACES',
                         'OFFERS & FEATURED RACES', 'UK AND IRISH RACES', 'UK And Irish Races', 'EXTRA PLACE RACES']

    def test_001_verify_racing_landing_pages_display_different_tabshr_featured_future_specials_yourcall_etcgr_today_tomorrow_futureby_meeting_and_by_time(self):
        """
        DESCRIPTION: Verify Racing Landing pages display different tabs
        DESCRIPTION: HR: FEATURED FUTURE SPECIALS YOURCALL etc
        DESCRIPTION: GR: TODAY TOMORROW FUTURE/BY MEETING AND BY TIME
        EXPECTED: User should be able to see these tabs.
        EXPECTED: HR: FEATURED FUTURE SPECIALS YOURCALL etc
        EXPECTED: GR: TODAY TOMORROW FUTURE/BY MEETING AND BY TIME
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='Horseracing')
        actual_horseracing_tabs = self.site.horse_racing.tabs_menu.items_names
        self.assertEqual(actual_horseracing_tabs, vec.Racing.RACING_TAB_NAMES,
                         msg=f'Actual tabs: "{actual_horseracing_tabs}" is not equal with the'
                             f'Expected tabs: "{vec.Racing.RACING_TAB_NAMES}"')
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state(state_name='Greyhoundracing')
        actual_greyhound_tabs = self.site.greyhound.tabs_menu.items_names
        if self.brand == 'ladbrokes':
            for greyhound_tab in vec.Racing.GREYHOUND_TAB_NAMES:
                self.assertIn(greyhound_tab, actual_greyhound_tabs,
                              msg=f'Expected tab: "{greyhound_tab}" is not available in the'
                                  f'Actual tabs: "{actual_greyhound_tabs}"')
        else:
            for greyhound_tab in vec.sb.SPORT_DAY_TABS:
                self.assertIn(greyhound_tab, actual_greyhound_tabs, msg=f'Expected tab: "{greyhound_tab}" is not '
                                                                        f'available in the Actual tabs: "{actual_greyhound_tabs}"')
            actual_greyhound_sub_tabs = self.site.greyhound.tab_content.items_names
            self.assertEqual(actual_greyhound_sub_tabs, vec.Racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING,
                             msg=f'Actual sub tabs: "{actual_greyhound_sub_tabs}" is not equal with the'
                                 f'Expected sub tabs: "{vec.Racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING}"')

    def test_002_click_and_verify_all_accordions_are_expandablecollapsible(self):
        """
        DESCRIPTION: Click and Verify all accordions are Expandable/Collapsible.
        EXPECTED: User should be able Expand/Collapse accordions by clicking on them.
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='Horseracing')
        sleep(10)
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Failed to display any section')
        for section_name, section in sections.items():
            self.assertTrue(section.is_expanded(), msg=f'Event "{section_name}" is not Expanded by default')
            section.collapse()
            self.assertFalse(section.is_expanded(), msg=f'Event "{section_name}" is not Collapsed')

        found_event = False
        for section_name, section in sections.items():
            if section_name in self.section_skip_list or self.next_races_title in section_name:
                continue
            else:
                if not section.is_expanded():
                    section.expand()
                meetings = section.items_as_ordered_dict
                self.assertTrue(meetings, msg='Failed to display any meeting')
                for meeting_name, meeting in meetings.items():
                    events = meeting.items_as_ordered_dict
                    self.assertTrue(events, msg='Failed to display any event')
                    for event_name, event in events.items():
                        race_started = event.is_resulted or event.has_race_off()
                        if not race_started:
                            event.click()
                            found_event = True
                            self.__class__.expected_meeting_name = meeting_name.replace('-', '')
                            break
                    if found_event is True:
                        break
                    else:
                        continue
                if found_event is True:
                    break
                else:
                    continue

    def test_003_verify_the_components_of_the_race_card(self):
        """
        DESCRIPTION: Verify the Components of the race card
        EXPECTED: User should be able to see
        EXPECTED: Each slide/event/card in the carousel will have below components
        EXPECTED: -Header with the Name, Time and More link navigating the user to the specific race card.
        EXPECTED: -E/W terms
        EXPECTED: -Display all selections with the silks and details same as production
        EXPECTED: -Display runners in chronological order
        EXPECTED: -Display unnamed favourite
        EXPECTED: -Watch Icon when the stream is available.
        EXPECTED: -Display runners in chronological order by taking sort order as racecard
        EXPECTED: -Display Unnamed Favourite & Unnamed 2nd Favourite
        EXPECTED: -LIVE STREAM when the stream is available.
        """
        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(market_tabs, msg='Market tabs not present')
        market_tabs.get(vec.racing.RACING_EDP_MARKET_TABS_NAMES[0]).click()
        racing_details = self.site.racing_event_details
        if self.device_type == 'desktop':
            actual_meeting_name = racing_details.sub_header.meeting_name
            resulted_event_time = racing_details.sub_header.event_time
            self.assertTrue(self.expected_meeting_name.lower() in actual_meeting_name.lower(),
                            msg=f'Expected meeting name: "{self.expected_meeting_name}" '
                                f'not in Actual: "{actual_meeting_name}"')
            self.assertFalse(resulted_event_time is None, msg='Resulted event time is None')
        else:
            result = wait_for_result(
                lambda: racing_details.event_title is not None,
                name='Wait for Event title to display',
                timeout=20)
            self.assertTrue(result, msg='Event title is not displayed')
        self.assertTrue(racing_details.each_way_terms.is_displayed(), msg='E/W Terms is not displayed')
        event_markets_list = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(event_markets_list, msg=f'No Event markets available for the event {racing_details.event_title}')
        market = list(event_markets_list.values())[0]
        outcomes = market.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No Outcomes present under the selected Event markets '
                                      f'{list(event_markets_list.keys())[0]}')
        outcome = next((outcome for outcome in outcomes.values() if outcome.bet_button.is_enabled()), None)
        price = outcome.bet_button.name
        if price != 'SP':
            if self.brand == 'ladbrokes':
                racing_details.tab_content.choose_sorting_option(vec.Racing.CARD_SORTING_OPTION_SELECTED)
            else:
                racing_details.tab_content.choose_sorting_option(vec.Racing.CARD_SORTING_OPTION)
        for item in racing_details.items:
            self.assertTrue(item.horse_name, msg='Failed to display the horse name')
            if item.horse_name == 'Unnamed Favourite' or item.horse_name == 'Unnamed 2nd Favourite':
                if item.horse_name == 'Unnamed Favourite':
                    self.assertEqual(item.horse_name, "Unnamed Favourite",
                                     msg='Failed to display the Unnamed Favourite')
                else:
                    self.assertEqual(item.horse_name, "Unnamed 2nd Favourite",
                                     msg='Failed to display the Unnamed 2nd Favourite')
            elif not item.is_non_runner:
                self.assertTrue(item.bet_button.is_displayed(),
                                msg=f'Bet button is not displayed for the horse "{item.horse_name}"')
                self.assertTrue(item.runner_number,
                                msg=f'Runner number is not displayed for the horse "{item.horse_name}"')
                self.assertTrue(item.jockey_name,
                                msg=f'Jockey name is not displayed for the horse "{item.horse_name}"')
                self.assertTrue(item.has_silks,
                                msg=f'Silk is not displayed for the horse "{item.horse_name}"')
        if racing_details.tab_content.has_video_stream_button():
            self.assertTrue(racing_details.tab_content.has_video_stream_button(),
                            msg=f'Event has no "{vec.sb.WATCH}" icon or "{vec.live_stream.LIVESTREAM_TITLE.title()}" button')
