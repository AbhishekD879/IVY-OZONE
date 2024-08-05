from collections import OrderedDict
import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_in_play_module_from_ws
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.sports_specific
@pytest.mark.snooker_specific
@pytest.mark.adhoc_suite
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.usefsccache_fix
@pytest.mark.reg165_fix
@pytest.mark.desktop
@vtest
class Test_C66007991_Validate_Snooker_In_play_tab_display_as_per_events_availability(BaseBetSlipTest):
    """
    TR_ID: C66007991
    NAME: Validate Snooker In-play tab display as per events availability
    DESCRIPTION: This test case needs to verify Snooker In-play tab display as per events availability
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    home_breadcrumb = 'Home'
    sport_name = 'Snooker'
    in_play = 'In Play'

    @classmethod
    def custom_tearDown(cls):
        cms = cls.get_cms_config()
        cms.update_system_configuration_structure(config_item='UseFSCCached', field_name="enabled", field_value='true')

    def click_active_price_button(self, sections):
        for section_name, section in sections.items():
            events = section.items_as_ordered_dict
            for event_name, event in events.items():
                odd = next((odd for odd in list(event.template.get_available_prices().values()) if
                            odd.name.upper() not in ['N/A', 'SUSP']), None)
                if odd:
                    odd.click()
                    if self.device_type == 'mobile':
                        wait_for_haul(3)
                        self.site.quick_bet_panel.close()
                    self.assertTrue(odd.is_selected(), f'{event_name + ">>" + odd.name.upper()} is not selected')
                    return odd.name.upper()
        return None

    def get_accordion_list(self):
        if self.device_type == "mobile":
            accordion_list = self.site.sports_page.tab_content.in_play_module
        else:
            accordion_list = self.site.snooker.tab_content.accordions_list
        return accordion_list

    def get_odd_values_for_events(self, events, sleep=True):
        if sleep:
            wait_for_haul(5)
        res = {}
        for event_name, event in events.items():
            res[event_name] = [button.name for button in event.template.get_available_prices().values()]
        return res

    def get_events_details(self):
        """
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
        response = None
        for _ in range(5):
            if response:
                break
            wait_for_haul(5)
            response = get_in_play_module_from_ws()
        types = response.get('data')[0].get('eventsByTypeName')
        res = {'typesDetails': {}, 'eventsIds': [], 'eventsCount': 0, 'typeNames': [], 'typesCount': 0}
        type_key = 'typeSectionTitleAllSports' if self.device_type != 'mobile' else 'typeSectionTitleConnectApp'
        res['typesDetails'] = {type[type_key].upper(): type for type in types}
        res['typeNames'] = res['typesDetails'].keys()
        res['eventsIds'] = set([id for type in types for id in type['eventsIds']])
        res['eventsCount'] = len(res['eventsIds'])
        res['typesCount'] = len(types)
        return res

    def test_000_preconditions(self):
        """
        DESCRIPTION: This test case needs to verify Snooker In-play tab display as per events availability
        PRECONDITIONS: 1.User must be logged in /logout
        PRECONDITIONS: Note: In mobile when no events are available Snooker sport is not displayed in A-Z sports menu and on clicking Snooker  from Sports ribbon user is navigated back to the sports homepage.
        """
        # checking live events availability
        is_snooker_live_events_available = bool(self.get_active_events_for_category(
            category_id=self.ob_config.snooker_config.category_id,
            in_play_event=True, raise_exceptions=False)
        )
        if not is_snooker_live_events_available:
            # checking basketball sport availability in menu carousel
            if self.device_type == "mobile":
                self.__class__.end_date = f'{get_date_time_as_string(days=182)}T22:00:00.000Z'
                is_snooker_events_available = bool(self.get_active_events_for_category(
                    category_id=self.ob_config.snooker_config.category_id,
                    all_available_events=True,
                    raise_exceptions=False)
                )
                if not is_snooker_events_available:
                    sports = self.site.home.menu_carousel.items_as_ordered_dict
                    snooker_availability = next(
                        (True for sport_name in sports if sport_name.upper() == self.sport_name.upper()), False)
                    if snooker_availability:
                        raise VoltronException(
                            'Snooker sport is available in menu carousel even though events not available for Snooker')
            raise SiteServeException("There is no live events for Snooker")

        # disabling UseFSCCached in CMS
        system_config = self.get_initial_data_system_configuration()
        fsc_call = system_config.get('UseFSCCached', {})
        if not fsc_call:
            fsc_call = self.cms_config.get_system_configuration_item('UseFSCCached')
        if fsc_call.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='UseFSCCached',
                                                                  field_name="enabled",
                                                                  field_value=False)

    def test_001_launch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes/Coral application
        EXPECTED: Home page should loaded successfully
        """
        self.site.go_to_home_page()
        self.site.login()

    def test_002_click_on_the_snooker_sport(self):
        """
        DESCRIPTION: Click on the Snooker sport.
        EXPECTED: User should be able to navigate to the Snooker landing page.
        """
        self.site.open_sport('Snooker')

    def test_003_verify_snooker_landing_page(self):
        """
        DESCRIPTION: Verify Snooker landing page.
        EXPECTED: Desktop
        EXPECTED: Tabs should be displayed with Matches tab selected by default with today events .
        EXPECTED: In play widget will display if any events are in live when it was enabled in sys config.
        EXPECTED: Mobile
        EXPECTED: Matches module loaded as default with inplay events in it
        """
        selected_default_tab = self.site.snooker.tabs_menu.current.upper()
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                    self.ob_config.snooker_config.category_id)
        self.assertEqual(selected_default_tab, expected_tab_name, f'{expected_tab_name} is not selected')

        if self.device_type == 'mobile':
            in_module_availablity_status = self.site.sports_page.tab_content.has_inplay_module()
            self.assertTrue(in_module_availablity_status, f'In-Play Module is not displayed')

    def test_004_verify_the_data_in_the_in_play_tab(self):
        """
        DESCRIPTION: Verify the data in the In play tab
        EXPECTED: User must be able to view the in play events count  with event details
        """
        events_data = self.get_events_details()
        if self.device_type == "mobile":
            expected_event_count = events_data.get('eventsCount')
            in_play_module = self.site.sports_page.tab_content.in_play_module
            actual_events_count = int(in_play_module.in_play_header.events_count_label)
            self.assertEqual(actual_events_count, expected_event_count, f'Actual Event Count : "{actual_events_count}"'
                                                                        f'is not same as '
                                                                        f'Expected Event Count : "{expected_event_count}"')
        else:
            in_play_tab_name = "IN-PLAY"
            self.site.snooker.tabs_menu.click_button(in_play_tab_name)

            default_tab = 'UPCOMING' if events_data.get('eventsCount') == 0 else 'LIVE NOW'
            self.assertEqual(self.site.snooker.tab_content.grouping_buttons.current.upper(),
                             default_tab, f'default tab : {default_tab} is not selected')
            if default_tab != 'LIVE NOW':
                is_snooker_live_events_available = bool(self.get_active_events_for_category(
                    category_id=self.ob_config.snooker_config.category_id,
                    in_play_event=True, raise_exceptions=False)
                )
                sub_tabs = self.site.snooker.tab_content.grouping_buttons.items_as_ordered_dict
                live_now = next(tab for tab_name, tab in sub_tabs.items() if tab_name.upper() == 'LIVE NOW')
                self.assertTrue((live_now.counter == 0 and not is_snooker_live_events_available),
                                'Live Events are available but not shown in front end')
                # verifying error msg
                live_now.click()
                error_msg = self.site.basketball.tab_content.has_no_events_label()
                self.assertTrue(error_msg, 'Error Message is Not Displayed even though events unavailable')
            sub_tabs = self.site.snooker.tab_content.grouping_buttons.items_as_ordered_dict
            live_now = next(tab for tab_name, tab in sub_tabs.items() if tab_name.upper() == 'LIVE NOW')
            self.assertEqual(live_now.counter, events_data.get('eventsCount'),
                             f"Counter value :{live_now.counter} is not expected value {events_data.get('eventsCount')}")


    def test_005_verify_the_score_updates(self):
        """
        DESCRIPTION: Verify the score updates
        EXPECTED: Scores updates should be seen in the front end.
        """
        accordion_list = self.get_accordion_list()
        events = {}
        events = {event_name: event for accordion_name, accordion in accordion_list.items_as_ordered_dict.items()
                  for event_name, event in accordion.items_as_ordered_dict.items() if len(events) < 3}
        # checking odds changed status
        events_with_odds = self.get_odd_values_for_events(events=events, sleep=False)
        is_odds_changed = next(
            (True for _ in range(24) if events_with_odds != self.get_odd_values_for_events(events=events)), False)
        self.assertTrue(is_odds_changed, f'scores are not changed')

        # signposting verification
        for event_name, event in events.items():
            self.assertTrue(event.template.is_live_now_event, f'"LIVE NOW" label is not available for {event_name}')

        # accordions flexibility
        if self.device_type == 'desktop':
            for accordion_name, accordion in accordion_list.items_as_ordered_dict.items():
                if accordion.is_expanded():
                    accordion.collapse()
                    self.assertFalse(accordion.is_expanded(), f'Accordion : {accordion_name} is not collapsed')
                    accordion.expand()
                    self.assertTrue(accordion.is_expanded(), f'Accordion : {accordion_name} is not expanded')
                else:
                    accordion.expand()
                    self.assertTrue(accordion.is_expanded(), f'Accordion : {accordion_name} is not expanded')
                    accordion.collapse()
                    self.assertFalse(accordion.is_expanded(), f'Accordion : {accordion_name} is not collapsed')
                    accordion.expand()

        # more link status
        for event_name, event in events.items():
            event_id = event.template.event_id
            event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0]['event']['children']

            if len(event_details) > 1:
                self.assertTrue(event.template.has_markets, msg='There is no "More" markets link')

        # navigation checking when click on event
        event_name, event = next(iter(events.items()))
        event.click()
        self.site.wait_content_state('EVENTDETAILS')

        if self.device_type == "desktop":
            event_name = wait_for_result(lambda: self.site.sport_event_details.header_line.page_title.text.upper(),
                                         bypass_exceptions=(
                                         NoSuchElementException, StaleElementReferenceException, VoltronException))
            self.assertEqual(event_name.replace(' V ', ' VS '), event_name.upper().replace(' V ', ' VS '),
                             f'not navigated to {event_name}')

    def test_006_verify_sign_postings(self):
        """
        DESCRIPTION: Verify sign postings
        EXPECTED: User should be able to see sign posting.
        """
        # covered in above step

    def test_007_verify_that_the_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify that the accordions are collapsable and expandable
        EXPECTED: Desktop
        EXPECTED: Accordions should be collapsable and expandable
        """
        # covered in above steps

    def test_008_verify_more_link_on_above_odds_selection(self):
        """
        DESCRIPTION: Verify More link on above odds selection
        EXPECTED: User should be navigated to respective EDP page
        """
        # covered in above steps

    def test_009_verify_by_clicking_on_event_details(self):
        """
        DESCRIPTION: Verify by clicking on event details
        EXPECTED: User should be navigate to the respective EDP page
        """
        # covered in above steps

    def test_010_verify_by_clicking_on_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be able to navigte to home page
        """
        self.site.back_button.click()
        self.site.wait_content_state_changed()

    def test_011_verify_by_clicking_on_backward_chevron_on_above__sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron on above  sport header
        EXPECTED: Mobile
        EXPECTED: User should be able tp navigate to sport navigation  page
        """
        # covered in above step

    def test_012_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should be able to navigate on the respective page on click
        """
        if self.device_type == 'mobile':
            return "This step is not applicable for mobile"
        page = self.site.sports_page
        breadcrumbs = OrderedDict((key.strip(), page.breadcrumbs.items_as_ordered_dict[key])
                                  for key in page.breadcrumbs.items_as_ordered_dict)
        self.assertTrue(breadcrumbs, msg='No breadcrumbs found')
        self.assertEqual(list(breadcrumbs.keys()).index(self.home_breadcrumb), 0,
                         msg='Home page is not shown the first by default')
        self.assertTrue(breadcrumbs[self.home_breadcrumb].angle_bracket,
                        msg=f'Angle bracket is not shown after "{self.home_breadcrumb}" breadcrumb')
        self.assertEqual(list(breadcrumbs.keys()).index(self.sport_name), 1,
                         msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
        self.assertTrue(breadcrumbs[self.sport_name].angle_bracket,
                        msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')
        self.assertEqual(list(breadcrumbs.keys()).index(self.in_play), 2,
                         msg=f'" In Play " item name is not shown after "{self.sport_name}"')
        self.assertTrue(
            int(breadcrumbs[self.in_play].link.css_property_value('font-weight')) == 700,
            msg=f'" In Play " hyperlink from breadcrumbs is not highlighted according to the selected page')

    def test_013_verify_by_clicking_see_all(self):
        """
        DESCRIPTION: Verify by clicking SEE ALL
        EXPECTED: Mobile
        EXPECTED: User should be navigate to sports ribbon in play tab by default  Snooker should be selected.
        """
        if self.device_type == "mobile":
            in_play_module = self.site.sports_page.tab_content.in_play_module
            self.assertTrue(in_play_module.has_see_all_link(), '"SEE ALL" link is not displayed')
            in_play_module.see_all_link.click()
            self.site.wait_content_state('InPlay', timeout=3)

            sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
            self.assertTrue(sports, msg='Sports list tab is not present')
            selected_tab_name = next((tab_name for tab_name, tab in sports.items() if tab.is_selected(timeout=5)), None)
            self.assertTrue(selected_tab_name, msg='Cannot find selected tab')
            self.assertEqual(selected_tab_name.upper(), self.sport_name.upper(),
                             msg=f'Selected tab "{selected_tab_name}" is same as Expected: "{self.sport_name.upper()}"')
            self.site.back_button.click()
            self.site.wait_content_state_changed()

    def test_014_verify_bet_placements_for_single_multiple_complex(self):
        """
        DESCRIPTION: Verify bet placements for single, multiple, complex
        EXPECTED: Bet placements should be successful
        """
        accordion_list = self.get_accordion_list()
        selected_odd = self.click_active_price_button(accordion_list.items_as_ordered_dict)
        if selected_odd:
            self.site.open_betslip()
            self.place_single_bet()
        else:
            self._logger.info(f'there is no active odds to place bet')

