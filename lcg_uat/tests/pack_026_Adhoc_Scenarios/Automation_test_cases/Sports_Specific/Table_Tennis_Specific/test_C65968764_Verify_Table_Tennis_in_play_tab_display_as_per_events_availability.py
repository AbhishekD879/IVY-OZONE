from collections import OrderedDict
import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_inplay_sports_by_section
from voltron.utils.waiters import wait_for_haul, wait_for_cms_reflection


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.sports_specific
@pytest.mark.table_tennis_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65968764_Verify_Table_Tennis_in_play_tab_display_as_per_events_availability(Common):
    """
    TR_ID: C65968764
    NAME: Verify Table Tennis in-play tab display as per events availability.
    DESCRIPTION: This test case needs to verify Table tennis in-play tab display as per events availability
    PRECONDITIONS: User must be logged in /logout
    PRECONDITIONS: Note: In mobile when no events are available table tennis sport is not displayed in A-Z sports menu and on clikcing table tennis  from Sports ribbon user is navigated back to the sports homepage.
    """
    keep_browser_open = True
    home_breadcrumb = 'Home'
    sport_name = 'table tennis'
    inplay_tab = 'In Play'
    enable_bs_performance_log = True

    def verify_breadcrumbs(self):
        page = self.site.sports_page
        breadcrumbs = OrderedDict((key.strip(), page.breadcrumbs.items_as_ordered_dict[key])
                                  for key in page.breadcrumbs.items_as_ordered_dict)
        self.assertTrue(breadcrumbs, msg='No breadcrumbs found')
        self.assertEqual(list(breadcrumbs.keys()).index(self.home_breadcrumb), 0,
                         msg=f'{self.home_breadcrumb} breadcrumb is not shown first')
        self.assertTrue(breadcrumbs[self.home_breadcrumb].angle_bracket,
                        msg=f'Angle bracket is not shown after "{self.home_breadcrumb}" breadcrumb')
        self.assertEqual(list(breadcrumbs.keys()).index(self.sport_name), 1,
                         msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
        self.assertTrue(breadcrumbs[self.sport_name].angle_bracket,
                        msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')
        self.assertEqual(list(breadcrumbs.keys()).index(self.inplay_tab), 2,
                         msg=f'{self.inplay_tab} is not shown after "{self.sport_name}"')
        self.assertTrue(
            int(breadcrumbs[self.inplay_tab].link.css_property_value('font-weight')) == 700,
            msg=f'" matches " hyperlink from breadcrumbs is not highlighted according to the selected page')

    def mobile_validations(self):        
        # ****************************** Verification of In Play module ************************
        in_play_module_status = self.site.sports_page.tab_content.has_inplay_module()
        if not in_play_module_status:
            self.device.refresh_page()
            wait_for_cms_reflection(lambda: self.site.sports_page.tab_content.has_inplay_module(), refresh_count=5, timeout=10, ref=self)
            in_play_module_status = self.site.sports_page.tab_content.has_inplay_module()
        self.assertTrue(bool(in_play_module_status), msg='In-Play Module is not available')
        self._logger.info(f'=====> Verified In Play module successfully')
        # ****************************** Verification of See All link ************************
        in_play_module = self.site.sports_page.tab_content.in_play_module
        self.assertTrue(in_play_module.has_see_all_link(), 'SEE ALL link is not displayed')
        in_play_module.see_all_link.click()
        self.site.wait_content_state_changed()
        sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        active_sport = next((sport_name.upper() for sport_name, sport in sports.items() if sport.is_selected()),
                            None)
        self.assertEqual(active_sport, "TABLE TENNIS",
                         f'Navigated to {active_sport} After clicking on "SEE ALL" link from TABLE TENNIS IN-PLAY Module')
        self._logger.info(f'=====> Verified See All link successfully')
        # ****************************** Verification of Live Now header with event count ************************
        tabs = self.site.inplay.tab_content.items_as_ordered_dict
        live_now = next((tab for tab_name, tab in tabs.items() if tab_name.upper() == "LIVE NOW"), None)
        live_events = get_inplay_sports_by_section(type='LIVE_EVENT')
        live_events_count_from_ws = f"({live_events.get('eventCount')})"
        live_events_count_from_fe = live_now.events_count_label
        if self.device_type != "mobile":
            self.assertEqual(live_events_count_from_ws, live_events_count_from_fe,
                             f'Actual Live Events Count {live_events_count_from_fe} is not same as '
                             f'Expected Live Events Count {live_events_count_from_ws}')
        self._logger.info(f'=====> Verified Live Now header with events count successfully')
        # ****************************** Verify accordions are expandable and Collapsable ************************
        event_scores_before = {}
        accordions = live_now.n_items_as_ordered_dict()
        scores_changed = False
        for accordion_name, accordion in accordions.items():
            accordion.collapse()
            self.assertFalse(accordion.is_expanded(), f'"{accordion_name}" is not collapsed after clicking on it')
            accordion.expand()
            self.assertTrue(accordion.is_expanded(), f'"{accordion_name}" is not expanded after clicking on it')
            self._logger.info(f'=====> Verified accordions are expandable and Collapsable')
            # ****************************** Verify Score Updates ************************
            event_scores_before[accordion_name] = list(accordion.items_as_ordered_dict.items())[0][
                1].template.score_table.items_as_ordered_dict.keys()
            elapsed_time = 0
            check_interval = 5
            max_wait_time = 120
            event_scores_after = {}
            scores_changed = False
            while elapsed_time < max_wait_time:
                event_scores_after[accordion_name] = list(accordion.items_as_ordered_dict.items())[0][
                    1].template.score_table.items_as_ordered_dict.keys()
                if event_scores_before[accordion_name] != event_scores_after[accordion_name]:
                    scores_changed = True
                    break
                else:
                    wait_for_haul(check_interval)
                    elapsed_time += check_interval
            if scores_changed:
                break
        if not scores_changed:
            raise VoltronException(f"Event scores are not changed")
        # ****************************** Verify back button ************************
        self.site.back_button.click()
        self.assertEqual(self.site.sports_page.header_line.page_title.text.upper(),
                         "TABLE TENNIS",
                         f'After Clicking on Back Button from In-Play not navigated to TABLE TENNIS page')
        self._logger.info(f'=====> Verified back button')
        # ****************************** Verify More Link ************************
        in_play_module = self.site.sports_page.tab_content.in_play_module
        first_accordion_name, first_accordion = in_play_module.first_item
        events = first_accordion.n_items_as_ordered_dict()
        event_name, event = next(
            ([event_title, event_obj] for event_title, event_obj in events.items() if event_obj.template.has_markets()),
            [None, None])
        if not event:
            event_name, event = next(iter(events))
            more_link = event
        else:
            more_link = event.template.more_markets_link
        self.assertTrue(event.event_id in self.inplay_event_ids,
                        msg=f'{event.event_id} event id is not in inplay event ids list {self.inplay_event_ids}')
        more_link.click()
        self.site.wait_content_state('EVENTDETAILS')
        wait_for_haul(5)
        if self.brand == "ladbrokes":
            event_details_page_name = self.site.sport_event_details.header_line.page_title.sport_title.upper()
            self.assertEqual(event_details_page_name, first_accordion_name.upper(),
                             msg=f'Expected event is {first_accordion_name.upper()} but actual is {event_details_page_name}')
        self._logger.info(f'=====> Verified More link')

    def desktop_validations(self):        
        # ****************************** Verification of Table Tennis live events ************************
        live_events = get_inplay_sports_by_section(type='LIVE_EVENT')
        if live_events and live_events.get('eventsIds'):
            number_of_live_events = live_events.get('eventCount')
        else:
            raise SiteServeException(f'There are no live events in Table Tennis')
        self._logger.info(f'=====> Verified Table Tennis live events are available')
        # ****************************** Verification of Live Now header with event count ************************
        expected_live_now_tab_header = f'{vec.inplay.LIVE_NOW_SWITCHER} ({number_of_live_events})'.upper()
        live_now_tab = self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.get(
            vec.inplay.LIVE_NOW_SWITCHER)
        actual_live_now_tab_header = f'{live_now_tab.name} ({live_now_tab.counter})'.upper()
        self.assertEqual(expected_live_now_tab_header, actual_live_now_tab_header,
                         msg=f'Expected live now header is {expected_live_now_tab_header}'
                             f'but Actual is  {actual_live_now_tab_header}')
        self._logger.info(f'=====> Verified Live Now header with event count')
        # ****************************** Verification Breadcrumbs ************************
        self.verify_breadcrumbs()
        # ****************************** Verify accordions are expandable and Collapsable ************************
        live_sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        if not live_sections:
            raise VoltronException(f"No live events available in sports")
        event_scores_before = {}
        scores_changed = False
        for section_name, section in list(live_sections.items()):
            section.collapse()
            self.assertFalse(section.is_expanded(), f'"{section_name}" is not collapsed after clicking on it')
            section.expand()
            self.assertTrue(section.is_expanded(), f'"{section_name}" is not expanded after clicking on it')
            self._logger.info(f'=====> Verified accordions are expandable and Collapsable')
            # ****************************** Verify Score Updates ************************
            event_scores_before[section_name] = list(section.items_as_ordered_dict.items())[0][
                1].template.score_table.items_as_ordered_dict.keys()
            elapsed_time = 0
            check_interval = 5
            max_wait_time = 120
            event_scores_after = {}
            while elapsed_time < max_wait_time:
                event_scores_after[section_name] = list(section.items_as_ordered_dict.items())[0][
                    1].template.score_table.items_as_ordered_dict.keys()
                if event_scores_before[section_name] != event_scores_after[section_name]:
                    self._logger.info("Event scores are changed")
                    scores_changed = True
                    break
                else:
                    wait_for_haul(check_interval)
                    elapsed_time += check_interval
            if scores_changed:
                break
        if not scores_changed:
            raise VoltronException(f"Event scores are not changed")
        self._logger.info(f'=====> Verified event scores are changed')
        # ****************************** Verify back button ************************
        self.site.sports_page.header_line.back_button.click()
        self.site.wait_content_state_changed()
        self._logger.info(f'=====> Verified back button')
        self.navigate_to_page(name='sport/table-tennis')
        self.site.wait_content_state('Table Tennis')
        self._logger.info(f'=====> Navigated to Table Tennis sport page successfully')
        # ****************************** Navigating to Table Tennis >> In Play >> LIVE NOW tab ************************
        current_tab = self.site.sports_page.tabs_menu.current
        inplay_tab = 'IN-PLAY'
        if current_tab.upper() != inplay_tab.upper():
            self.site.sports_page.tabs_menu.click_button(inplay_tab)
        self.site.sports_page.tab_content.grouping_buttons.click_button(vec.inplay.LIVE_NOW_SWITCHER)
        self._logger.info(f'=====> Navigated to In Play Live Now tab')
        # ****************************** Verify More link  ************************
        live_sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        section = list(live_sections.values())[0]
        if not section.is_expanded():
            section.expand()
        events = section.items_as_ordered_dict
        event_name, event = next(iter(events.items()))
        self.assertTrue(event.event_id in self.inplay_event_ids, msg=f'{event.event_id} event id is not in inplay event ids list {self.inplay_event_ids}')
        self.assertTrue(event.template.more_markets_link,
                        msg=f'More Markets Link is not present for event {event_name}')
        event.template.more_markets_link.click()
        self.site.wait_content_state('EVENTDETAILS')
        wait_for_haul(15)
        if self.brand == 'ladbrokes':
            actual_section_name = self.site.competition_league.title_section.type_name.name.upper()
            self.assertEqual(event_name.upper(), actual_section_name,
                             msg=f'Expected section name is {event_name.upper()} but Actual is {actual_section_name}')
        self._logger.info(f'=====> Verified More link')

    def test_000_pre_condition(self):
        """
        PRECONDITIONS: Check Table Tennis live events
        PRECONDITIONS: Table Tennis live events should be available
        """
        inplay_events = self.get_active_events_for_category(category_id="59", in_play_event=True, all_available_events=True)
        self.__class__.inplay_event_ids = []
        for inplay_event in inplay_events:
            if inplay_event['event']['id'] not in self.inplay_event_ids:
                self.inplay_event_ids.append(inplay_event['event']['id'])

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the Lads/Coral application
        EXPECTED: Home page should be loaded successfully
        """
        # ****************************** Navigating to Home page ************************
        self.site.login()
        self.site.wait_content_state(state_name="Homepage")
        self._logger.info(f'=====> Launched application and Home page loaded successfully')

    def test_002_click_on_table_tennis_sport(self):
        """
        DESCRIPTION: Click on table tennis sport.
        EXPECTED: User should be able to navigate table tennis landing page.
        """
        # ****************************** Navigating to Table Tennis ************************
        self.navigate_to_page(name='sport/table-tennis')
        self.site.wait_content_state('Table Tennis')
        self._logger.info(f'=====> Navigated to Table Tennis sport page successfully')
        # ****************************** Navigating to Table Tennis >> In Play >> LIVE NOW tab ************************
        current_tab = self.site.sports_page.tabs_menu.current
        expected_tab_name = 'IN-PLAY' if self.device_type != 'mobile' else 'MATCHES'
        if current_tab.upper() != expected_tab_name.upper():
            self.site.sports_page.tabs_menu.click_button(expected_tab_name)
        if self.device_type != 'mobile':
            self.site.sports_page.tab_content.grouping_buttons.click_button(vec.inplay.LIVE_NOW_SWITCHER)
        self._logger.info(f'=====> Navigated to In Play Live Now tab')
        if self.device_type == 'mobile':
            self.mobile_validations()
        else:
            self.desktop_validations()

    def test_003_verify_inplay_tab(self):
        """
        DESCRIPTION: Verify inplay tab
        EXPECTED: User must be able to in play events count  with event details
        """
        # Covered in step 2

    def test_004_verify_score_updates(self):
        """
        DESCRIPTION: Verify score updates
        EXPECTED: Scores updates should happen
        """
        # Covered in step 2

    def test_005_verify_sign_postings(self):
        """
        DESCRIPTION: Verify sign postings
        EXPECTED: User should be able to see signposting.
        """
        # Covered in C65968956 test case

    def test_006_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordion's are collapsable and expandable
        EXPECTED: Accordion's should be collapsable and expandable
        """
        # Covered in step 2

    def test_007_verify_more_link_on_above_odds_selection(self):
        """
        DESCRIPTION: Verify More link on above odds selection
        EXPECTED: User should be navigated to respective EDP page
        """
        # Covered in step 2

    def test_008_verify_by_clicking_on_event_details(self):
        """
        DESCRIPTION: Verify by clicking on event details
        EXPECTED: User should be navigated to respective EDP page
        """
        # Covered in step 2

    def test_009_verify_by_clicking_on_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be navigated to home page
        EXPECTED: Mobile
        EXPECTED: User should be navigated to sport navigation  page
        """
        # Covered in step 2

    def test_010_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should navigate to the respective page on click
        EXPECTED: Mobile
        EXPECTED: User should navigate to sports ribbon in play tab by default
        """
        # Covered in step 2

    def test_011_verify_by_clicking_see_all(self):
        """
        DESCRIPTION: Verify by clicking SEE ALL
        EXPECTED: Mobile
        EXPECTED: User should navigate to sports ribbon in play tab by default
        """
        # Covered in step 2

    def test_012_verify_bet_placements_for_single_multiplecomplex(self):
        """
        DESCRIPTION: Verify bet placements for single, multiple,complex
        EXPECTED: Bet placements should be successful
        """
        # Covered in C65968766 test case
