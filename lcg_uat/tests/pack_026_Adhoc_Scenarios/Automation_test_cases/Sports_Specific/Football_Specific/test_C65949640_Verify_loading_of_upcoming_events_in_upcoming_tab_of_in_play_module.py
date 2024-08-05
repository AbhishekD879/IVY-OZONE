import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import get_inplay_sports_by_section
from voltron.utils.waiters import wait_for_result, wait_for_haul
from voltron.utils.helpers import normalize_name

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.sports_specific
@pytest.mark.football_specific
@pytest.mark.adhoc_suite
@vtest
class Test_C65949640_Verify_loading_of_upcoming_events_in_upcoming_tab_of_in_play_module(Common):
    """
    TR_ID: C65949640
    NAME: Verify loading of upcoming events in upcoming tab of in-play module
    DESCRIPTION: This Testcase verifies the loading of upcoming events in upcoming tab of in-play module
    PRECONDITIONS: Data display under upcoming tab
    """
    keep_browser_open = True
    enable_bs_performance_log = True

    def get_upcoming_event_name(self):
        upcoming_event_ids = get_inplay_sports_by_section(type='UPCOMING_EVENT').get('eventsByTypeName')[0].get('eventsIds')
        event_id = upcoming_event_ids[0]
        selections = self.ss_req.ss_event_to_outcome_for_event(event_id)
        event_name = normalize_name(selections[0].get('event').get('name'))
        drilldown_Tag_Names = selections[0].get('event').get('drilldownTagNames')
        return event_name, drilldown_Tag_Names

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application
        EXPECTED: Application should be loaded successfully.
        """
        #=========================open home page ==========================
        self.site.go_to_home_page()
        self.site.wait_content_state(state_name='HomePage')

    def test_002_navigate_to_football_and_switch_to_inplay__ampgtupcoming_tab(self):
        """
        DESCRIPTION: Navigate to Football and switch to Inplay--&amp;gt;Upcoming tab
        EXPECTED: If events are available,
        EXPECTED: Upcoming header along with count should be displayed.
        EXPECTED: ex- Upcoming (**)
        EXPECTED: Event Card body should show with
        EXPECTED: *event1 vs event2
        EXPECTED: * fixture headers (home,draw,away)
        EXPECTED: * Odd buttons
        EXPECTED: * Favourite icon (Star icon)
        EXPECTED: *Time,date
        EXPECTED: * More markets link
        EXPECTED: *Signposting
        EXPECTED: *SEE ALL in mobile mode.
        EXPECTED: If no events are available, below message should be displayed.
        EXPECTED: There are no upcoming events.
        """
        #===================================================== open football slp page ===================================================
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(vec.siteserve.FOOTBALL_TAB)
        current_tab = self.site.football.tabs_menu.current
        inplay_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                             self.ob_config.football_config.category_id)
        if current_tab.upper() != inplay_tab.upper():
            self.site.football.tabs_menu.click_button(inplay_tab)
        if self.device_type != 'mobile':
            self.site.football.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
        wait_for_haul(5)
        # ======================================= validating upcoming event availability ========================================
        upcoming_events = get_inplay_sports_by_section(type='UPCOMING_EVENT')
        if upcoming_events and upcoming_events.get('eventsIds'):
            expected_counter = upcoming_events.get('eventCount')
        else:
            raise SiteServeException(f'There are no upcoming events in football')

        if self.device_type == 'mobile':
            upcoming = self.site.football.tab_content.upcoming
            self.assertTrue(upcoming, msg='upcoming section is not available in homepage')
            upcoming_count_label = upcoming.events_count_label
            upcoming_label_name = upcoming.name
            # ============================================ Validating upcoming header along with count =============================================
            actual_upcoming_label_name = f'{upcoming_label_name} {upcoming_count_label}'
            expected_upcoming_label_name = f'{vec.inplay.UPCOMING_EVENTS_SECTION} ({expected_counter})'
            self.assertAlmostEqual(int(upcoming_count_label.strip('()')), expected_counter, delta=3,
                                   msg=f'actual upcoming event count {int(upcoming_count_label.strip("()"))} is not equal to '
                                       f'expected upcoming event count {expected_counter}')
            self.assertEqual(actual_upcoming_label_name.upper(), expected_upcoming_label_name.upper(),
                             msg=f'actual label {actual_upcoming_label_name} is not equal to expected label'
                                 f'{expected_upcoming_label_name}')

            #************************************************* valiating event card body ***********************************************
            self.__class__.upcoming_sections = wait_for_result(lambda :self.site.football.tab_content.upcoming.items_as_ordered_dict, timeout=120)
            self.assertTrue(self.upcoming_sections, msg='upcoming events are not available in upcoming section')
            upcoming_section = list(self.upcoming_sections.values())[0]
            upcoming_section.scroll_to_we()
            upcoming_section.click()
        else:
            upcoming = self.site.football.tab_content.grouping_buttons.items_as_ordered_dict.get(vec.inplay.UPCOMING_SWITCHER)
            self.assertTrue(upcoming, msg='upcoming events are not available in FE')
            upcoming_name = upcoming.name
            upcoming_counter = upcoming.counter
            self.assertAlmostEqual(int(upcoming_counter), expected_counter, delta=3, msg=f'actual upcoming event count {int(upcoming_counter)} is not equal to '
                                                                                                    f'expected upcoming event count {expected_counter}' )
            #============================================ Validating upcoming header along with count =============================================
            expected_upcoming_header = f'{vec.inplay.UPCOMING_SWITCHER} ({expected_counter})'
            actual_upcoming_header = f'{upcoming_name} ({upcoming_counter})'
            self.assertEqual(actual_upcoming_header, expected_upcoming_header, msg=f'actual upcoming header {actual_upcoming_header} '
                                                                               f'is not equal to expected upcoming header {expected_upcoming_header}')
            #************************************************* valiating event card body ***********************************************
            self.__class__.upcoming_sections = self.site.football.tab_content.accordions_list.n_items_as_ordered_dict()
            self.assertTrue(self.upcoming_sections, msg='event is not available')
            upcoming_section = list(self.upcoming_sections.values())[0]
        #============================================== validating fixture headers =================================================
        actual_header1 = upcoming_section.fixture_header.header1
        actual_header2 = upcoming_section.fixture_header.header2
        actual_header3 = upcoming_section.fixture_header.header3
        self.assertEqual(actual_header1, vec.sb.HOME,
                     msg=f'actual fixture header name {actual_header1} not equal to expected fixture header name {vec.sb.HOME}')
        self.assertEqual(actual_header2, vec.sb.DRAW,
                     msg=f'actual fixture header name {actual_header2} not equal to expected fixture header name {vec.sb.DRAW}')
        self.assertEqual(actual_header3, vec.sb.AWAY,
                     msg=f'actual fixture header name {actual_header3} not equal to expected fixture header name {vec.sb.AWAY}')
        #================================================ validating event1 vs event2 ================================================
        expected_event_name, drilldown_Tag_Names = self.get_upcoming_event_name()
        events = list(key.upper() for key in upcoming_section.items_as_ordered_dict.keys())
        self.assertTrue(upcoming_section.count_of_items, msg='leagues are not available')
        first_event = upcoming_section.first_item[1]
        actual_event_name = first_event.template.name
        self.assertIn(expected_event_name.upper(),events, msg=f'expected event name {expected_event_name.upper()} is not present in {events}')
        #================================================= validating odd buttons ======================================
        self.assertTrue(len(first_event.template.items_names) is not 0, msg=f'odd buttons is not present in {actual_event_name} as {first_event.template.items_names}')
        #================================================= validating Favourite icon (Star icon) ==============================
        if self.device_type != 'mobile':
            has_favourite_icon = first_event.template.has_favourite_icon
            self.assertTrue(has_favourite_icon, msg='favourite icon is not available')
        #================================================= validating Time,date ==========================================
        event_time = first_event.template.event_time
        self.assertTrue(event_time, msg=f'event time and date {event_time} is not displayed')
        #================================================ validate more markets link =====================================
        has_more_market_ink = first_event.template.has_markets
        self.assertTrue(has_more_market_ink, msg='more markets link is not available')
        #================================================ validaing signposting ===========================================
        drilldown_Tag_Name_list = drilldown_Tag_Names.split(',')
        if self.brand == 'ladbrokes' and 'EVFLAG_BL' in drilldown_Tag_Name_list and 'EVFLAG_PB' in drilldown_Tag_Name_list:
            sign_posting = first_event.template.promotion_icons
            self.assertTrue(sign_posting, msg='signposting is not available')
        elif self.brand == 'bma' and 'EVFLAG_BL' in drilldown_Tag_Name_list:
            sign_posting = first_event.template.has_byb_icon
            self.assertTrue(sign_posting, msg='signposting is not available')

    def test_003_click_on_any_unexpanded_competition_name_and_observe(self):
        """
        DESCRIPTION: Click on any unexpanded competition name and observe
        EXPECTED: Competition section should expand and all the events should be displayed.
        """
        for competition_name, competition in self.upcoming_sections.items():
            if not competition.is_expanded():
                competition.expand()
                self.assertTrue(competition.is_expanded(),
                                msg=f'{competition_name} section is not expanded after clicking')

    def test_004_for_mobileverify_see_all_link_navigation(self):
        """
        DESCRIPTION: For Mobile:
        DESCRIPTION: Verify SEE ALL Link navigation.
        EXPECTED: Mobile:
        EXPECTED: On clicking SEE ALL link should navigate to
        EXPECTED: respective competitions details page
        """
        if self.device_type == 'mobile':
            section_name,section = list(self.upcoming_sections.items())[0]
            if not section.is_expanded():
                section.expand()
            has_see_all_link = section.group_header.has_see_all_link
            self.assertTrue(has_see_all_link, msg='SEE ALL link is not available')
            see_all_link = section.group_header.see_all_link
            see_all_link.click()
            self.site.wait_content_state('CompetitionLeaguePage')
            actual_section_name = self.site.competition_league.title_section.type_name.name.upper()
            self.assertEqual(section_name.upper(), actual_section_name,
                             msg=f'Expected section name is {section_name.upper()} but Actual is {actual_section_name}')
            self._logger.info(f'=====> Verified SEE ALL link for mobile')


