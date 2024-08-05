import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import get_inplay_sports_by_section
from voltron.utils.waiters import wait_for_haul, wait_for_cms_reflection


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.table_tennis_specific
@pytest.mark.sports_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65968766_Verify_loading_of_upcoming_events_in_upcoming_tab_of_in_play_module_for_Table_Tennis(BaseBetSlipTest):
    """
    TR_ID: C65968766
    NAME: Verify loading of upcoming events in upcoming tab of in-play module for Table Tennis
    DESCRIPTION: This test case needs to  verify loading of upcoming events in upcoming tab of in-play module for Table tennis
    PRECONDITIONS: User must be logged in /logout
    PRECONDITIONS: Note: In mobile when no events are available table tennis sport is not displayed in A-Z sports menu and on clicking table tennis  from Sports ribbon user is navigated back to the sports homepage.
    """
    keep_browser_open = True
    is_in_play_events_available = False
    enable_bs_performance_log = True

    def select_active_odds(self, sections):
        odds = []
        for section_name, section in sections.items():
            events = section.items_as_ordered_dict
            for event_name, event in events.items():
                odd = next((odd for odd in list(event.template.get_available_prices().values()) if
                            odd.name.upper() not in ['N/A', 'SUSP']), None)
                if odd:
                    odds.append(odd)
                if len(odds) == 2:
                    break
            if len(odds) == 2:
                break
        return odds

    def mobile_validations(self):
        self.navigate_to_page(name='sport/table-tennis')
        wait_for_haul(10)

        current_tab = self.site.sports_page.tabs_menu.current
        expected_tab_name = 'MATCHES'
        if current_tab.upper() != expected_tab_name.upper():
            self.site.sports_page.tabs_menu.click_button(expected_tab_name)

        # verifying in play module presence status
        in_play_module_status = self.site.sports_page.tab_content.has_inplay_module()
        if not in_play_module_status:
            self.device.refresh_page()
            wait_for_cms_reflection(lambda: self.site.sports_page.tab_content.has_inplay_module(), refresh_count=5, timeout=10, ref=self)
            in_play_module_status = self.site.sports_page.tab_content.has_inplay_module()
        self.assertEqual(self.is_in_play_events_available, bool(in_play_module_status), 'In-Play Module is not available')

        if not self.is_in_play_events_available:
            return "In-Play Events Are Unavailable"

        # verifying SEE ALL link status and working
        in_play_module = self.site.sports_page.tab_content.in_play_module
        self.assertTrue(in_play_module.has_see_all_link(), 'SEE ALL link is not displayed')

        in_play_module.see_all_link.click()
        self.site.wait_content_state_changed()

        sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        active_sport = next((sport_name.upper() for sport_name, sport in sports.items() if sport.is_selected()), None)
        self.assertEqual(active_sport, "TABLE TENNIS",
                         f'Navigated to {active_sport} After clicking on "SEE ALL" link from TABLE TENNIS IN-PLAY Module')

        # verifying Live Now and Upcoming Sections Locations
        tabs = self.site.inplay.tab_content.items_as_ordered_dict
        live_now = next((tab for tab_name, tab in tabs.items() if tab_name.upper() == "LIVE NOW"), None)
        upcoming = next((tab for tab_name, tab in tabs.items() if tab_name.upper() == "UPCOMING EVENTS"), None)

        live_now_location = live_now.location.get('y')
        upcoming_location = upcoming.location.get('y')
        self.assertLess(live_now_location, upcoming_location, 'LIVE NOW section is not at top of the UPCOMING section')

        # live now and upcoming events counter
        if self.device_type != "mobile":
            live_events_count_from_ws = f"({self.get_events_details().get('eventsCount')})"
            live_events_count_from_fe = live_now.events_count_label
            self.assertEqual(live_events_count_from_ws, live_events_count_from_fe,
                             f'Actual Live Events Count {live_events_count_from_fe} is not same as '
                             f'Expected Live Events Count {live_events_count_from_ws}')

        upcoming_events_count_from_ws = f"({self.get_events_details('UPCOMING').get('eventsCount')})"
        upcoming_events_count_from_fe = upcoming.events_count_label
        self.assertEqual(upcoming_events_count_from_fe, upcoming_events_count_from_ws,
                         f'Actual Upcoming Events Count {upcoming_events_count_from_fe} is not same as '
                         f'Expected Upcoming Events Count {upcoming_events_count_from_ws}')

        # upcoming accordions collapsed mode and checking able to expand and collapse
        accordions = upcoming.n_items_as_ordered_dict()
        for accordion_name, accordion in accordions.items():
            self.assertFalse(accordion.is_expanded(), f'"{accordion_name}" is not in collapsed mode')
            accordion.expand()
            self.assertTrue(accordion.is_expanded(), f'"{accordion_name}" is not expanded after clicking on it')
            accordion.collapse()
            self.assertFalse(accordion.is_expanded(), f'"{accordion_name}" is not collapsed after clicking on it')

        # Verifying live now accordions are collapsable and expandable
        accordions = live_now.n_items_as_ordered_dict()
        for accordion_name, accordion in accordions.items():
            accordion.expand()
            self.assertTrue(accordion.is_expanded(), f'"{accordion_name}" is not expanded after clicking on it')
            accordion.collapse()
            self.assertFalse(accordion.is_expanded(), f'"{accordion_name}" is not collapsed after clicking on it')

        # verifying back button
        self.site.back_button.click()
        self.assertEqual(self.site.sports_page.header_line.page_title.text.upper(),
                         "TABLE TENNIS",
                         f'After Clicking on Back Button from In-Play not navigated to TABLE TENNIS page')

        # verifying More Link working
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

        more_link.click()
        self.site.wait_content_state('EVENTDETAILS')
        wait_for_haul(5)
        if self.brand == "ladbrokes":
            event_details_page_name = self.site.sport_event_details.header_line.page_title.sport_title.upper()
            self.assertEqual(event_details_page_name, first_accordion_name.upper(),
                             'After Clicking on event from In-Play module not navigated proper event')
        self.site.back_button.click()
        self.site.wait_content_state_changed()

    def desktop_validations(self):
        self.navigate_to_page(name='sport/table-tennis')
        wait_for_haul(10)

        # verifying Breadcrumbs
        breadcrumbs_for_tab = {'IN-PLAY': 'IN PLAY', 'MATCHES': 'MATCHES'}
        for tab_name, tab in self.site.sports_page.tabs_menu.items_as_ordered_dict.items():
            if tab_name not in breadcrumbs_for_tab:
                continue
            tab.click()
            wait_for_haul(2)
            expected_breadcrumb = f'HOME > TABLE TENNIS > {breadcrumbs_for_tab.get(tab_name).upper()}'
            breadcrumbs = self.site.sports_page.breadcrumbs.items_as_ordered_dict
            actual_breadcrumb = ' > '.join(breadcrumbs.keys()).upper()
            self.assertEqual(expected_breadcrumb, actual_breadcrumb,
                             msg=f'Actual Bread Crumb is "{actual_breadcrumb}" is not same as Expected Breadcrumb'
                                 f': "{expected_breadcrumb}"')

        in_play_tab = "IN-PLAY"
        self.site.sports_page.tabs_menu.click_button(in_play_tab)

        events_details = self.get_events_details()

        default_tab = 'UPCOMING' if events_details.get('eventsCount') == 0 else 'LIVE NOW'

        self.assertEqual(self.site.sports_page.tab_content.grouping_buttons.current.upper(),
                         default_tab, f'default tab : {default_tab} is not selected')

        sub_tabs = self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.keys()
        for tab_name in sub_tabs:
            self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.get(tab_name).click()
            wait_for_haul(5)
            events_details = self.get_events_details(type_of_events=tab_name)

            # verifying events count and error msg
            error_msg = False
            if events_details.get('eventCount') == 0:
                # verifying error msg
                error_msg = self.site.sports_page.tab_content.has_no_events_label()
                self.assertTrue(error_msg, 'Error Message is Not Displayed even though events unavailable')

            if error_msg:
                continue

            count_of_events_on_fe = self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.get(
                tab_name).counter
            self.assertEqual(events_details.get('eventsCount'), count_of_events_on_fe,
                             msg=f'Actual Events Count : "{count_of_events_on_fe}" is not same'
                                 f'as Expected Events Count : "{events_details.get("eventsCount")}" in "{tab_name}" tab')

            # verifying accordions expandable and collapsable
            accordions = self.site.sports_page.tab_content.accordions_list.n_items_as_ordered_dict()
            for accordion_name, accordion in accordions.items():
                if accordion.is_expanded():
                    accordion.collapse()
                    self.assertFalse(accordion.is_expanded(),
                                     f'Accordion: "{accordion_name}" is not collapsed after clicking on it')
                    accordion.expand()
                    self.assertTrue(accordion.is_expanded(),
                                    f'Accordion: "{accordion_name}"  is not expanded after clicking on it')
                else:
                    accordion.expand()
                    self.assertTrue(accordion.is_expanded(),
                                    f'Accordion: "{accordion_name}"  is not expanded after clicking on it')
                    accordion.collapse()
                    self.assertFalse(accordion.is_expanded(),
                                     f'Accordion: "{accordion_name}"  is not collapsed after clicking on it')

            # verifying more link
            accordion_name, accordion = next(iter(accordions.items()))
            accordion.expand()
            events = accordion.items_as_ordered_dict
            for event_name, event in events.items():
                if not event.template.has_markets():
                    continue
                more_link_location = event.template.more_markets_link.location.get('y')
                odds_location = event.template.first_item[1].location.get('y')
                if self.brand == "ladbrokes":
                    self.assertLess(more_link_location, odds_location, f'More link is not displayed above the odds')
                    break

            if event.template.has_markets():
                event.template.more_markets_link.click()
                self.site.wait_content_state('EVENTDETAILS')
                self.assertEqual(event_name.upper(),
                                 self.site.sport_event_details.header_line.page_title.sport_title.upper(),
                                 msg=f"After Clicking on {event_name} event's More Link not navigated properly")
                self.site.sport_event_details.header_line.press_back()
                self.site.wait_content_state_changed()

    def get_events_details(self, type_of_events='LIVE NOW'):
        """
        @param
        'type_of_events' : accepts value in ('LIVE_EVENT', 'UPCOMING_EVENT')
        @return:
            {
                'typesDetails': {
                                    'type_name1': details1,
                                    'types_name2': details2, .. typenameN: detailsN
                                }
                'eventsIds' : list of event ids (list : []),
                'eventsCount' : total no of events (int),
                'typeNames' : list of type names (list : []),
                'typesCount' : number of types (int)
            }
        """
        types_of_events = {'LIVE NOW': 'LIVE_EVENT', 'UPCOMING': 'UPCOMING_EVENT'}
        types = get_inplay_sports_by_section(type=types_of_events.get(type_of_events)).get('eventsByTypeName')
        res = {'typesDetails': {}, 'eventsIds': [], 'eventsCount': 0, 'typeNames': [], 'typesCount': 0}
        if not types:
            raise SiteServeException(f'Neither events found for {type_of_events}')
        res['typesDetails'] = {f"{type['className']} - {type['typeName']}".upper(): type for type in types}
        res['typeNames'] = res['typesDetails'].keys()
        res['eventsCount'] = sum([type['eventCount'] for type in types])
        res['eventsIds'] = [id for type in types for id in type['eventsIds']]
        res['typesCount'] = len(types)
        return res

    def test_000_pre_condition(self):
        """
        PRECONDITIONS: User must be logged in /logout
        PRECONDITIONS: Note: In mobile when no events are available table tennis sport is not displayed in A-Z sports menu and on clicking table tennis  from Sports ribbon user is navigated back to the sports homepage.
        """
        in_play_events = self.get_active_events_for_category(category_id="59", in_play_event=True, raise_exceptions=False)
        self.__class__.is_in_play_events_available = True if in_play_events else False

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should loaded successfully
        """
        self.site.login()
        if self.device_type == "mobile":
            msg = self.mobile_validations()
            if msg:
                raise SiteServeException(msg)
        else:
            self.desktop_validations()

    def test_002_click_on_table_tennis_sport(self):
        """
        DESCRIPTION: Click on table tennis sport.
        EXPECTED: User should be able to navigate table tennis landing page.
        """
        pass

    def test_003_verify_by_clicking_in_play(self):
        """
        DESCRIPTION: Verify by clicking IN PLAY
        EXPECTED: DESKTOP
        EXPECTED: User should navigate to live now tab with count display  by default if live events present.
        EXPECTED: User should navigate to upcoming tab with count display  by default if no  live events present.
        """
        # covered in above steps

    def test_004_verify_error_message_for_live_events_and_upcoming_events_if_no_data_available(self):
        """
        DESCRIPTION: Verify error message for live events and upcoming events if no data available
        EXPECTED: Live now
        EXPECTED: There are currently no Live events available
        EXPECTED: Upcoming
        EXPECTED: There are no upcoming events
        """
        # covered in above steps

    def test_005_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should be navigated on the respective page on click
        """
        # covered in above steps

    def test_006_verify_by_clicking_on_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be navigated to homepage
        EXPECTED: Mobile
        EXPECTED: User should be naviagted to sport navigation page
        """
        # covered in above steps

    def test_007_verify_upcoming_events_for_mobile_by_clicking_on_see_all_link_in__inplay(self):
        """
        DESCRIPTION: Verify upcoming events for mobile by clicking on see all link in  inplay
        EXPECTED: Upcoming events should be displayed in collapsed mode below in play module .
        """
        # covered in above steps

    def test_008_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordion's are collapsable and expandable
        EXPECTED: Accordion's should be collapsable and expandable
        """
        # covered in above steps

    def test_009_verify_more_link_on_above_odds_selection(self):
        """
        DESCRIPTION: Verify More link on above odds selection
        EXPECTED: User should be navigated to respective EDP page.
        """
        # covered in above steps

    def test_010_verify_bet_placement_for_single_multiplecomplex(self):
        """
        DESCRIPTION: Verify bet placement for single, multiple,complex
        EXPECTED: Bet placement need to successful
        """
        if self.device_type == "mobile":
            sections = self.site.sports_page.tab_content.in_play_module.items_as_ordered_dict
        else:
            self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.get("LIVE NOW").click()
            sections = self.site.sports_page.tab_content.accordions_list.n_items_as_ordered_dict()
            self.assertTrue(sections, 'There is no active events to place bet')

        odds = self.select_active_odds(sections)

        self.assertTrue(odds, 'There is no active events to place bet')

        # placing single bet
        odds[0].click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.site.open_betslip()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

        # placing multiple bet
        odds = self.select_active_odds(sections)
        if len(odds) < 2:
            self._logger.info(f'there is no events to place double bet"')
        else:
            odds[0].click()
            if self.device_type == 'mobile':
                self.site.add_first_selection_from_quick_bet_to_betslip()
            odds[1].click()
            self.site.open_betslip()
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
