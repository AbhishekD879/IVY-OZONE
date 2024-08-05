from collections import OrderedDict
import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_inplay_sports_by_section
from voltron.utils.waiters import wait_for_haul
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.sports_specific
@pytest.mark.snooker_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.reg165_fix
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.usefsccache_fix
@vtest
class Test_C66007998_Verify_loading_of_upcoming_events_in_Upcoming_tab_of_in_play_module_for_Snooker(BaseBetSlipTest):
    """
    TR_ID: C66007998
    NAME: Verify loading of upcoming events in Upcoming tab of in-play module for Snooker
    DESCRIPTION: This test case needs to  verify loading of upcoming events in Upcoming tab of in-play module for Snooker
    PRECONDITIONS: 1.User must be logged in /logout
    PRECONDITIONS: Note: In mobile when no events are available Snooker sport is not displayed in A-Z sports menu and on clicking Snooker  from Sports ribbon user is navigated back to the sports homepage.
    """
    keep_browser_open = True
    home_breadcrumb = vec.sb.HOME_FOOTER_ITEM.title()
    sport_name = vec.sb.SNOOKER
    inplay_tab = 'In Play'
    enable_bs_performance_log = True

    def click_active_price_button(self, sections, no_of_bet_buttons_to_be_select=1):
        no_of_odds_selected = 0
        for section_name, section in sections.items():
            section.expand()
            events = section.items_as_ordered_dict
            for event_name, event in events.items():
                odd = next((odd for odd in list(event.template.get_available_prices().values()) if
                            odd.name.upper() not in ['N/A', 'SUSP']), None)
                if odd:
                    odd.click()
                    if self.device_type == 'mobile' and no_of_odds_selected == 0:
                        wait_for_haul(3)
                        self.site.quick_bet_panel.close()
                        wait_for_haul(2)
                    self.assertTrue(odd.is_selected(), f'{event_name + ">>" + odd.name.upper()} is not selected')
                    no_of_odds_selected += 1
                if no_of_odds_selected == no_of_bet_buttons_to_be_select:
                    break
            if no_of_odds_selected == no_of_bet_buttons_to_be_select:
                break
        return no_of_odds_selected == no_of_bet_buttons_to_be_select

    def place_bet_and_validate(self, accordions):
        status = self.click_active_price_button(accordions)
        if not status:
            return "There is no active events to place betting"
        self.site.open_betslip()
        self.place_single_bet()
        self.assertTrue(self.site.is_bet_receipt_displayed(), f'Bet Receipt is not displayed')
        self.site.close_betreceipt()

        status = self.click_active_price_button(accordions, no_of_bet_buttons_to_be_select=2)
        if not status:
            return "There is no enough events to place double betting"
        self.site.open_betslip()
        self.place_multiple_bet(number_of_stakes=1)
        self.assertTrue(self.site.is_bet_receipt_displayed(), f'Bet Receipt is not displayed')
        self.site.close_betreceipt()
        return "Bet Placement is successfully done"

    def check_accordions_flexibility(self, accordions):
        for accordion_name, accordion in accordions.items():
            if accordion.is_expanded():
                accordion.collapse()
                self.assertFalse(accordion.is_expanded(),
                                 msg=f'Accordion: "{accordion_name}" is not collapsed after clicking on it')
                accordion.expand()
                self.assertTrue(accordion.is_expanded(),
                                msg=f'Accordion: "{accordion_name}"  is not expanded after clicking on it')
            else:
                accordion.expand()
                self.assertTrue(accordion.is_expanded(),
                                msg=f'Accordion: "{accordion_name}"  is not expanded after clicking on it')
                accordion.collapse()
                self.assertFalse(accordion.is_expanded(),
                                 msg=f'Accordion: "{accordion_name}"  is not collapsed after clicking on it')

    def check_more_link_status(self, accordions):
        for accordion_name, accordion in accordions.items():
            events = accordion.items_as_ordered_dict
            for event_name, event in events.items():
                event_id = event.template.event_id
                event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
                if len(event_resp[0]['event'].get('children')) > 1:
                    self.assertTrue(event.has_markets(), msg=f"Event doesn't have more link'{event_name}'")
                    event.more_markets_link.click()
                    if self.device_type == "mobile":
                        self.site.wait_content_state(state_name='EventDetails')
                    else:
                        self.site.wait_content_state(state_name='EventDetails')
                        actual_event_name = self.site.sport_event_details.content_title_text.upper().replace(' VS ',
                                                                                                             ' V ')
                        expected_event_name = event_name.upper().replace(' VS ', ' V ')
                        self.assertEqual(actual_event_name, expected_event_name,
                                         msg=f'Actual event title {actual_event_name} is not same as expected event title {expected_event_name}')
                    self.site.back_button.click()
                    self.site.wait_content_state_changed()
                    return

    def get_events_details(self, type_of_events='LIVE NOW'):
        response, res = None, {'typesDetails': {}, 'eventsIds': [], 'eventsCount': 0, 'typeNames': [], 'typesCount': 0}
        types_of_events = {'LIVE NOW': 'LIVE_EVENT', 'UPCOMING': 'UPCOMING_EVENT'}
        type = types_of_events.get(type_of_events)
        for _ in range(5):
            if response:
                break
            wait_for_haul(5)
            response = get_inplay_sports_by_section(type=type)
        if not response:
            return res
        types = response.get('eventsByTypeName')
        type_key = 'typeSectionTitleAllSports' if self.device_type != 'mobile' else 'typeSectionTitleConnectApp'
        res['typesDetails'] = {type[type_key].upper(): type for type in types}
        res['typeNames'] = res['typesDetails'].keys()
        res['eventsIds'] = set([id for type in types for id in type['eventsIds']])
        res['eventsCount'] = len(res['eventsIds'])
        res['typesCount'] = len(types)
        return res

    def test_000_preconditions(self):
        # checking live events availability
        is_snooker_live_events_available = bool(self.get_active_events_for_category(
            category_id=self.ob_config.snooker_config.category_id,
            in_play_event=True, raise_exceptions=False)
        )
        if not is_snooker_live_events_available and self.device_type == "mobile":
            # checking snooker sport availability in menu carousel
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

    def test_001_launch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes/Coral application
        EXPECTED: Home page should loaded successfully
        """
        self.site.go_to_home_page()
        self.site.login()

    def test_002_click_on_snooker_sport(self):
        """
        DESCRIPTION: Click on Snooker sport.
        EXPECTED: User should be able to navigate Snooker landing page.
        """
        self.site.open_sport(vec.sb.SNOOKER)

    def test_003_verify_snooker_landing_page(self):
        """
        DESCRIPTION: Verify Snooker landing page.
        EXPECTED: Desktop
        EXPECTED: Tabs should be displayed with Matches tab selected by default with today events  .
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

    def test_004_verify_by_clicking_in_play(self):
        """
        DESCRIPTION: Verify by clicking IN PLAY
        EXPECTED: DESKTOP
        EXPECTED: User should be navigate to live now tab with count display  by default if live events present .
        EXPECTED: User should be navigate to upcoming  tab with count display  by default if no  live events are present.
        """
        if self.device_type == 'mobile':
            return "This Step is Not Applicable for Mobile"

        in_play_tab_name = "IN-PLAY"
        self.site.snooker.tabs_menu.click_button(in_play_tab_name)

        events_data = self.get_events_details()
        default_tab = vec.Inplay.UPCOMING_SWITCHER if events_data.get('eventsCount') == 0 else vec.Inplay.LIVE_NOW_SWITCHER
        self.assertEqual(self.site.snooker.tab_content.grouping_buttons.current.upper(),
                         default_tab, f'default tab : {default_tab} is not selected')

        if default_tab == vec.Inplay.UPCOMING_SWITCHER:
            sub_tabs = self.site.snooker.tab_content.grouping_buttons.items_as_ordered_dict
            upcoming_events_data = self.get_events_details(type_of_events=vec.Inplay.UPCOMING_SWITCHER)
            upcoming_tab = sub_tabs.get(vec.Inplay.UPCOMING_SWITCHER)
            self.assertEqual(upcoming_tab.counter, upcoming_events_data.get('eventsCount'),
                             f"Counter value :{upcoming_tab.counter} is not expected value {events_data.get('eventsCount')}")
            if upcoming_events_data.get('eventsCount') == 0:
                error_msg = self.site.snooker.tab_content.has_no_events_label()
                self.assertTrue(error_msg, 'Error Message is Not Displayed even though events unavailable')

            live_now = sub_tabs.get(vec.Inplay.LIVE_NOW_SWITCHER)
            self.assertTrue(live_now.counter == 0,
                            'Live Events are available but not shown in front end')
            # verifying error msg
            live_now.click()
            error_msg = self.site.snooker.tab_content.has_no_events_label()
            self.assertTrue(error_msg, 'Error Message is Not Displayed even though events unavailable')

            sub_tabs = self.site.snooker.tab_content.grouping_buttons.items_as_ordered_dict
            upcoming_tab = sub_tabs.get(vec.Inplay.UPCOMING_SWITCHER)
            upcoming_tab.click()
        else:
            sub_tabs = self.site.snooker.tab_content.grouping_buttons.items_as_ordered_dict
            live_now = sub_tabs.get(vec.Inplay.LIVE_NOW_SWITCHER)
            self.assertEqual(live_now.counter, events_data.get('eventsCount'),
                             f"Counter value :{live_now.counter} is not expected value {events_data.get('eventsCount')}")

            upcoming_tab = sub_tabs.get(vec.Inplay.UPCOMING_SWITCHER)
            actual_event_count = upcoming_tab.counter
            upcoming_tab.click()
            upcoming_events_data = self.get_events_details(type_of_events=vec.Inplay.UPCOMING_SWITCHER)
            self.assertEqual(actual_event_count, upcoming_events_data.get('eventsCount'),
                             f"Counter value :{actual_event_count} is not expected value {upcoming_events_data.get('eventsCount')}")

            if upcoming_events_data.get('eventsCount') == 0:
                error_msg = self.site.snooker.tab_content.has_no_events_label()
                self.assertTrue(error_msg, 'Error Message is Not Displayed even though events unavailable')

    def test_005_verify_error_message_for_live_events_and_upcoming_events_if_no_data_avaible(self):
        """
        DESCRIPTION: Verify error message for live events and upcoming events if no data avaible
        EXPECTED: Live now
        EXPECTED: There are currently no Live events available
        EXPECTED: Upcoming
        EXPECTED: There are no upcoming events
        """
        # covered in above step

    def test_006_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should be navigated on the respective page on click
        """
        if self.device_type == 'mobile':
            return "Not Applicable for Mobile"

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

    def test_007_verify_by_clicking_on_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be navigated to homepage
        """
        if self.device_type == 'mobile':
            return "Not Applicable for Mobile"

        accordions = self.site.sports_page.tab_content.accordions_list.n_items_as_ordered_dict()
        self.check_accordions_flexibility(accordions=accordions)

        self.check_more_link_status(accordions)
        self.site.back_button.click()
        self.site.wait_content_state('Home')

    def test_008_verify_by_clicking_on_backward_chevron_on_above__sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron on above  sport header
        EXPECTED: Mobile
        EXPECTED: User should be navigated to sport navigation page
        """
        pass

    def test_009_verify_upcoming_events_for_mobile_by_clicking_on_see_all_link_in__inplay(self):
        """
        DESCRIPTION: Verify upcoming events for mobile by clicking on see all link in  inplay
        EXPECTED: Upcoming events should be displayed in collospsed mode below in play module .
        """
        if self.device_type == 'desktop':
            return "Not Applicable for desktop"

        in_module_availablity_status = self.site.sports_page.tab_content.has_inplay_module()
        self.assertTrue(in_module_availablity_status, f'In-Play Module is not displayed')

        in_play_module = self.site.sports_page.tab_content.in_play_module
        self.assertTrue(in_play_module.has_see_all_link(), 'SEE ALL link is not displayed')
        in_play_module.see_all_link.click()
        self.site.wait_content_state_changed()
        sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        active_sport = next((sport_name.upper() for sport_name, sport in sports.items() if sport.is_selected()),
                            None)
        self.assertEqual(active_sport.upper(), self.sport_name.upper(),
                         f'Navigated to {active_sport} After clicking on "SEE ALL" link from Snooker IN-PLAY Module')

        sections = self.site.inplay.tab_content.items_as_ordered_dict
        upcoming_section = sections.get(vec.inplay.UPCOMING_EVENTS_SECTION)

        upcoming_events_data = self.get_events_details(type_of_events=vec.Inplay.UPCOMING_SWITCHER)
        upcoming_events_count_from_ws = f"({upcoming_events_data.get('eventsCount')})"
        upcoming_events_count_from_fe = upcoming_section.events_count_label
        self.assertEqual(upcoming_events_count_from_fe, upcoming_events_count_from_ws,
                         f'Actual Upcoming Events Count : "{upcoming_events_count_from_fe}" is not same as '
                         f'Expected Upcoming Events Count : "{upcoming_events_count_from_ws}"')

        accordions = upcoming_section.items_as_ordered_dict
        expanded_accordions = [accordion_name for accordion_name, accordion in accordions.items() if accordion.is_expanded()]
        self.assertFalse(bool(expanded_accordions), f'Some of the accordions are in expanded mode : "{expanded_accordions}"')
        self.check_accordions_flexibility(accordions=accordions)

        self.site.back_button.click()
        self.site.wait_content_state('Snooker')

    def test_010_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordions are collapsable and expandable
        EXPECTED: Accordions should be collapsable and expandable
        """
        # Covered above steps

    def test_011_verify_more_link_on_above_odds_selection(self):
        """
        DESCRIPTION: Verify More link on above odds selection
        EXPECTED: User should be navigated to respective EDP page
        """
        # Covered in above steps

    def test_012_verify_bet_placements_for_single_multiple_complex(self):
        """
        DESCRIPTION: Verify bet placements for single, multiple, complex
        EXPECTED: Bet placements should be successful
        """
        if self.device_type == 'desktop':
            self.navigate_to_page('sport/snooker/live')
            sub_tabs = self.site.snooker.tab_content.grouping_buttons.items_as_ordered_dict
            sub_tabs.get(vec.Inplay.UPCOMING_SWITCHER).click()
            accordions = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        else:
            self.navigate_to_page('in-play/snooker')
            sections = self.site.inplay.tab_content.items_as_ordered_dict
            upcoming_section = sections.get(vec.inplay.UPCOMING_EVENTS_SECTION)
            accordions = upcoming_section.items_as_ordered_dict
        message = self.place_bet_and_validate(accordions)
        self._logger.info(message)