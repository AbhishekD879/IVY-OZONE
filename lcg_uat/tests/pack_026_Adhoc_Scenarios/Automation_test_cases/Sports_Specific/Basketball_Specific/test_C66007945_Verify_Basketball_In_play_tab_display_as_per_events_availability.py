from collections import OrderedDict
import pytest
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_inplay_sport_by_category
from voltron.utils.waiters import wait_for_result, wait_for_haul
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports_specific
@pytest.mark.basketball_specific
@pytest.mark.adhoc_suite
@pytest.mark.reg165_fix
@pytest.mark.usefsccache_fix
@pytest.mark.desktop
@vtest
class Test_C66007945_Verify_Basketball_In_play_tab_display_as_per_events_availability(BaseBetSlipTest):
    """
    TR_ID: C66007945
    NAME: Verify Basketball In-play tab display as per events availability.
    DESCRIPTION: This test case needs to verify Basketball In-play tab display as per events availability
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    home_breadcrumb = 'Home'
    sport_name = 'Basketball'
    in_play = 'In Play'

    def get_accordion_list(self):
        if self.device_type == "mobile":
            accordion_list = self.site.inplay.tab_content.items_as_ordered_dict.get(vec.inplay.LIVE_NOW_EVENTS_SECTION)
        else:
            accordion_list = self.site.basketball.tab_content.accordions_list
        return accordion_list

    def get_odd_values_for_events(self, events, sleep=True):
        if sleep:
            wait_for_haul(5)
        res = {}
        for event_name, event in events.items():
            res[event_name] = [button.name for button in event.template.get_available_prices().values()]
        return res

    def get_dict_as_name_and_more_link_status(self, event_ids):
        res = {}
        for id in event_ids:
            details = self.ss_req.ss_event_to_outcome_for_event(event_id=id, raise_exceptions=False)[0].get('event')
            res[details['name'].upper()] = True if len(details.get('children')) > 1 else False
        return res

    def check_accordion_flexibility(self, accordion_name, accordion):
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
        wait_for_haul(5)
        response = get_inplay_sport_by_category(category_id=self.ob_config.basketball_config.category_id)
        types = [type for item in response for type in item.get('eventsByTypeName')] if isinstance(response, list) else response.get('eventsByTypeName')
        res = {'typesDetails': {}, 'eventsIds': [], 'eventsCount': 0, 'typeNames': [], 'typesCount': 0}
        type_key = 'typeSectionTitleAllSports' if self.device_type != 'mobile' else 'typeSectionTitleConnectApp'
        res['typesDetails'] = {type[type_key].upper(): type for type in types}
        res['typeNames'] = res['typesDetails'].keys()
        res['eventsIds'] = set([id for type in types for id in type['eventsIds']])
        res['eventsCount'] = len(res['eventsIds'])
        res['typesCount'] = len(types)
        return res

    def select_non_aggregated_market(self):
        market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.main_markets
        dropdown = self.site.basketball.tab_content.dropdown_market_selector

        if self.brand == 'bma' and self.device_type == 'mobile' :
            if not self.site.basketball.tab_content.dropdown_market_selector.is_expanded():
                self.site.basketball.tab_content.dropdown_market_selector.expand()
        if self.brand == 'bma':
            available_markets = [option.strip() for option in self.site.basketball.tab_content.dropdown_market_selector.available_options]
        else:
            available_markets = [option.strip() for option in self.site.inplay.tab_content.dropdown_market_selector.available_options]

        if self.device_type != 'mobile' and self.brand == 'bma':
            dropdown.click()
            list(self.site.basketball.tab_content.dropdown_market_selector.options)[
                available_markets.index(market_name)].click()
        elif self.device_type != 'mobile' and self.brand != 'bma':
            if not dropdown.is_expanded():
                dropdown.expand()
            list(self.site.inplay.tab_content.dropdown_market_selector.items_as_ordered_dict.values())[
                available_markets.index(market_name)].click()
        else:
            if not self.site.basketball.tab_content.dropdown_market_selector.is_expanded():
                self.site.basketball.tab_content.dropdown_market_selector.expand()
            self.site.basketball.tab_content.dropdown_market_selector.items_as_ordered_dict[market_name].click()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User must be logged in /logout
        PRECONDITIONS: Note: In mobile when no events are available Basketball sport is not displayed in A-Z sports menu and on clicking Basketball from Sports ribbon user is navigated back to the sports homepage
        """
        # checking live events availability
        is_basketball_live_events_available = bool(self.get_active_events_for_category(
            category_id=self.ob_config.basketball_config.category_id,
            in_play_event=True, raise_exceptions=False)
        )

        if not is_basketball_live_events_available:
            # checking basketball sport availability in menu carousel
            if self.device_type == "mobile":
                is_basketball_events_available = bool(self.get_active_events_for_category(
                    category_id=self.ob_config.basketball_config.category_id,
                    raise_exceptions=False)
                )
                if not is_basketball_events_available:
                    sports = self.home.menu_carousel.items_as_ordered_dict
                    basketball_availability = next(
                        (True for sport_name in sports if sport_name.upper() == "BASKETBALL"), False)
                    if basketball_availability:
                        raise VoltronException(
                            'BasketBall sport is available in menu carousel evenn though events not available for Basketball')

            raise SiteServeException("There is no live events for Basketball")

        # checking IN-PLAY tab availability in CMS
        self.__class__.in_play_tab = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                    self.ob_config.basketball_config.category_id,
                                    raise_exceptions=False)

        is_in_play_tab_available_in_cms = bool(self.in_play_tab)

        if not is_in_play_tab_available_in_cms:
            raise CmsClientException(
                f'{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play} is not available in basketball CMS configuration')

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the Lads/Coral application
        EXPECTED: Home page should be loaded successfully
        """
        self.site.login()

    def test_002_click_on_basketball_sport(self):
        """
        DESCRIPTION: Click on Basketball sport.
        EXPECTED: User should be able to navigate Basketball landing page.
        """
        self.site.open_sport("Basketball")

    def test_003_verify_inplay_tab(self):
        """
        DESCRIPTION: Verify inplay tab
        EXPECTED: User must be able to in play events count  with event details
        """
        tabs = self.site.basketball.tabs_menu.items_as_ordered_dict
        in_play_tab_name, in_play_tab = next(
            ((tab_name, tab) for tab_name, tab in tabs.items() if tab_name.upper() == self.in_play_tab.upper()),
            (None, None))
        in_play_tab.click()

        events_details = self.get_events_details()
        if self.device_type == "mobile":
            pass
            # live now and the counter is not applicable after 167 release  OZONE-12249
            # live_now = self.site.inplay.tab_content.items_as_ordered_dict.get(vec.inplay.LIVE_NOW_EVENTS_SECTION)
            # self.assertEqual(live_now.events_count_label, f"({events_details.get('eventsCount')})",
            #                  f'events count is not same as expected')
        else:
            default_tab = 'UPCOMING' if events_details.get('eventsCount') == 0 else 'LIVE NOW'
            self.assertEqual(self.site.basketball.tab_content.grouping_buttons.current.upper(),
                             default_tab, f'default tab : {default_tab} is not selected')
            if default_tab != 'LIVE NOW':
                is_basketball_live_events_available = bool(self.get_active_events_for_category(
                    category_id=self.ob_config.basketball_config.category_id,
                    in_play_event=True, raise_exceptions=False)
                )
                sub_tabs = self.site.basketball.tab_content.grouping_buttons.items_as_ordered_dict

                live_now = next(tab for tab_name, tab in sub_tabs.items() if tab_name.upper() == 'LIVE NOW')
                self.assertTrue((live_now.counter == 0 and not is_basketball_live_events_available), 'Live Events are available but not shown in front end')

                # verifying error msg
                live_now.click()
                error_msg = self.site.basketball.tab_content.has_no_events_label()
                self.assertTrue(error_msg, 'Error Message is Not Displayed even though events unavailable')

            sub_tabs = self.site.basketball.tab_content.grouping_buttons.items_as_ordered_dict

            live_now = next(tab for tab_name, tab in sub_tabs.items() if tab_name.upper() == 'LIVE NOW')

            self.assertEqual(live_now.counter, events_details.get('eventsCount'),
                             f"Counter value :{live_now.counter} is not expected value {events_details.get('eventsCount')}")

    def test_004_verify_score_updates(self):
        """
        DESCRIPTION: Verify score updates
        EXPECTED: Scores updates should happen
        """
        # selecting non aggregated markets
        self.select_non_aggregated_market()

        # reading 3 events
        accordion_list = self.get_accordion_list()
        events = {}
        events = {event_name: event for accordion_name, accordion in accordion_list.items_as_ordered_dict.items() for event_name, event in accordion.items_as_ordered_dict.items() if len(events) < 3}

        # checking odds changed status
        events_with_odds = self.get_odd_values_for_events(events=events, sleep=False)
        is_odds_changed = next((True for _ in range(24) if events_with_odds != self.get_odd_values_for_events(events=events)), False)
        self.assertTrue(is_odds_changed, f'scores are not changed')

    def test_005_verify_sign_postings(self):
        """
        DESCRIPTION: Verify sign postings
        EXPECTED: User should be able to see signposting.
        """
        events_details = self.get_events_details()
        more_link_status = self.get_dict_as_name_and_more_link_status(events_details.get('eventsIds'))

        accordion_list = self.get_accordion_list()
        accordions = accordion_list.n_items_as_ordered_dict(4)

        for accordion_name, accordion in accordions.items():
            self.check_accordion_flexibility(accordion_name, accordion)
            events = accordion.n_items_as_ordered_dict(2)
            for event_name, event in events.items():
                self.assertTrue(event.template.is_live_now_event, f'"LIVE NOW" label is not available for {event_name}')
                if more_link_status.get(event_name.upper()) != None:
                    self.assertEqual(event.template.more_markets_link, more_link_status[event_name.upper()],
                                     f'Actual More Link Market Status is : {event.template.more_markets_link}'
                                     f'is not same as Expected Status : {more_link_status[event_name.upper()]}')

        first_accordion_name, first_accordion = accordion_list.first_item
        first_event_name, first_event = first_accordion.first_item
        first_event.click()
        self.site.wait_content_state('EVENTDETAILS')

        if self.device_type == "desktop":
            event_name = wait_for_result(lambda: self.site.sport_event_details.header_line.page_title.text.upper(), bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException))
            self.assertEqual(event_name.replace(' V ', ' VS '), first_event_name.upper().replace(' V ', ' VS '),
                             f'not navigated to {first_event_name}')

    def test_006_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordion's are collapsable and expandable
        EXPECTED: Accordion's should be collapsable and expandable
        """
        # covered in above step

    def test_007_verify_more_link_on_above_odds_selection(self):
        """
        DESCRIPTION: Verify More link on above odds selection
        EXPECTED: User should be navigated to respective EDP page
        """
        # covered in above step

    def test_008_verify_by_clicking_on_event_details(self):
        """
        DESCRIPTION: Verify by clicking on event details
        EXPECTED: User should be navigated to respective EDP page
        """
        # covered in above step

    def test_009_verify_by_clicking_on_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be navigated to home page
        EXPECTED: Mobile
        EXPECTED: User should be navigated to sport navigation  page
        """
        self.site.back_button.click()
        self.site.wait_content_state_changed()

    def test_010_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should navigate to the respective page on click
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

    def test_011_verify_by_clicking_see_all(self):
        """
        DESCRIPTION: Verify by clicking SEE ALL
        EXPECTED: Mobile
        EXPECTED: User should navigate to sports ribbon in play tab by default
        """
        if self.device_type == 'desktop':
            return 'This test is not applicable for Desktop'

        accordion_list = self.get_accordion_list()
        first_accordion_name, first_accordion = accordion_list.first_item
        first_accordion_name = first_accordion_name.upper().replace('\nSEE ALL', '')

        first_accordion.expand()
        self.assertTrue(first_accordion.group_header.has_see_all_link(),
                        f'SEE ALL link is not available for {first_accordion_name}')

        first_accordion.group_header.see_all_link.click()
        self.site.wait_content_state_changed()

        page_title = self.site.competition_league.title_section.type_name.text.upper()
        self.assertEqual(first_accordion_name.upper(), page_title, f'Actual Page title is : {page_title}'
                                                                   f'is not same as Expected : {first_accordion_name.upper()}')

        self.site.back_button.click()

    def test_012_verify_bet_placements_for_single_multiple_complex(self):
        """
        DESCRIPTION: Verify bet placements for single, multiple, complex
        EXPECTED: Bet placements should be successful
        """
        # covered in C60089514
