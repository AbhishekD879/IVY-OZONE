import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870409_Check_that_Inplay_events_are_available_on_Football__matches_page_on_right_side_Check_the_behaviour_when_one_events_is_available_Check_the_behaviour_when_multiple_events_are_available_and_user_can_scroll_thr_all_of_them_Check_user_can_expand_an(Common):
    """
    TR_ID: C44870409
    NAME: "Check that Inplay events are available on Football -> matches page on right side  Check the behaviour when one events is available  Check the behaviour when multiple events are available and user can scroll thr' all of them  Check user can expand an
    DESCRIPTION: "Check that Inplay events are available on Football -> matches page on right side
    DESCRIPTION: Check the behaviour when one events is available
    DESCRIPTION: Check the behaviour when multiple events are available and user can scroll thr' all of them
    DESCRIPTION: Check user can expand and collapse the section
    DESCRIPTION: Check user can navigate to In play page on click of link available below section
    DESCRIPTION: Check event details are correct on section with odds and score if applicable
    DESCRIPTION: CHeck all the details are updating with PUSH
    DESCRIPTION: Check all above steps on multiple sports say Tennis, Basketball
    DESCRIPTION: - Verify 'Live now' and 'Upcoming Events' counters on In-play page when move to mode on Desktop (updated counters should be shown after unlocking)
    """
    keep_browser_open = True

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched
        """
        self.site.wait_content_state('HomePage')

    def test_002_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: User should be navigated to the Football landing page with the Inplay, matches, competitions,accumulators, outrights and Specials tab
        """
        self.site.open_sport(name='FOOTBALL')
        expected_football_tab_list = list(vec.sb.SPORT_TABS_INTERNAL_NAMES._asdict().values())
        expected_football_tab_list.append(vec.Inplay.BY_IN_PLAY.lower())
        if self.brand == 'ladbrokes':
            expected_football_tab_list.append(vec.SB.TABS_NAME_COUPONS.lower())
        football_tab_list = list(self.site.football.tabs_menu.get_items().keys())
        for tab in football_tab_list:
            self.assertIn(tab.lower(), expected_football_tab_list, msg=f'Tab: "{tab}"'
                                                                       f'is not listed in Expected tabs: "{expected_football_tab_list}"')

    def test_003_verify_the_user_can_expand_and_collapse_the_section(self):
        """
        DESCRIPTION: Verify the user can expand and collapse the section
        EXPECTED: User should be able to expand or collapse
        """
        accordions_list = list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(accordions_list, msg='No event section found on Football page')
        accordions_list_length = len(accordions_list) if len(accordions_list) < 5 else 5  # added this condition to
        # reduce the execution time
        for i in range(accordions_list_length):
            if accordions_list[i].is_expanded():
                accordions_list[i].collapse()
                accordions_list = list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.values())
                self.assertFalse(accordions_list[i].is_expanded(), msg=f'Event "{accordions_list[i]}" is not collapsed')
            else:
                accordions_list[i].expand()
                accordions_list = list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.values())
                self.assertTrue(accordions_list[i].is_expanded(), msg=f'Event "{accordions_list[i]}" are not expanded')

    def test_004_verify_the_user_can_navigate_to_in_play_page_on_click_of_link_available_below_section(self):
        """
        DESCRIPTION: Verify the user can navigate to Inplay page on click of link available below section
        EXPECTED: user should be navigated to the inplay section
        """
        self.site.football.tabs_menu.click_button(vec.Inplay.BY_IN_PLAY.upper())
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab.lower(), vec.Inplay.BY_IN_PLAY.lower(),
                         msg=f'In-Play tab is not active, active is "{active_tab}"')

    def test_005_verify_the_event_details_are_correct_on_the_section_with_odds_and_score_if_applicable(self):
        """
        DESCRIPTION: Verify the event details are correct on the section with odds and score if applicable
        EXPECTED: Event details with the odds (score if available) should be displayed
        """
        if self.device_type == 'mobile':
            in_play_events = self.site.inplay.tab_content.live_now.items_as_ordered_dict
        else:
            in_play_events = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(in_play_events, msg='No events found')
        for event_name, event in in_play_events.items():
            if not event.is_expanded():
                event.expand()
            first_event = list(event.items)[0]
            odds = first_event.template.get_available_prices
            self.assertTrue(odds, msg=f'No odds found for event "{first_event}" ')

    def test_006_verify_Live_now_upcoming_events_counters_on_in_play_page_when_move_to_mode_on_desktop(self):
        """
        DESCRIPTION: Verify 'Live now' and 'Upcoming Events' counters on In-play page when move to mode on Desktop
        EXPECTED: Live now' and 'Upcoming Events' sections should be displayed under In-play tab.
        """
        if self.device_type == 'mobile':
            flag_live_now = self.site.inplay.tab_content.live_now
            self.assertTrue(flag_live_now.is_displayed(), msg='Live Now Counter NOT shown under In-Play tab')
            flag_upcoming = self.site.inplay.tab_content.upcoming
            self.assertTrue(flag_upcoming.is_displayed(), msg='Upcoming Counter NOT shown under In-Play tab')
        else:
            sections = list(self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict.keys())
            expected_sections = [vec.Inplay.LIVE_NOW_SWITCHER, vec.Inplay.UPCOMING_SWITCHER]
            self.assertEqual(sections, expected_sections, msg=f'Actual sections: "{sections}" are not same as' +
                                                              f'Expected sections: "{expected_sections}"')
