import re
from random import choice

import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.high
@pytest.mark.virtual_sports
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.reg157_fix
@pytest.mark.sanity
@vtest
class Test_C874393_Virtual_Sport_Page(BaseVirtualsTest):
    """
    TR_ID: C874393
    NAME: Virtual Sport Page
    DESCRIPTION: This test case verifies the Virtual Sport page, list and order of Virtual Sports types
    DESCRIPTION: NOTE:
    DESCRIPTION: On step #3 - Darts and Boxing are absent (prod)
    """
    keep_browser_open = True
    next_events = vec.virtuals.VIRTUAL_HUB_NEXT_EVENTS

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get list of active virtual sports
        DESCRIPTION: Login into the app
        EXPECTED: User successfully log into the app
        """
        virtuals_cms_class_ids = self.cms_virtual_sports_class_ids()
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.virtuals_config.category_id)
        sports_list = ss_req.ss_class(query_builder=self.ss_query_builder.
                                      add_filter(simple_filter(LEVELS.CLASS,
                                                               ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                                               str(self.ob_config.virtuals_config.category_id))))
        if not sports_list:
            raise SiteServeException('There are no active virtual sports')
        event = None
        events = None
        for sport_class in sports_list:
            class_id = sport_class['class']['id']
            events = self.get_active_event_for_class(class_id=class_id, raise_exceptions=False)
            if not events:
                continue
            event = choice(events)
            ss_class_id = event['event']['classId']
            if ss_class_id not in virtuals_cms_class_ids:
                continue
            break
        if not event or not events:
            raise SiteServeException('There are no available virtual event with Forecast tab')
        tab_name = self.cms_virtual_sport_tab_name_by_class_ids(class_ids=[ss_class_id])
        self.__class__.expected_tab = tab_name[0]

    def test_001_load_oxygen_application_and_go_to_virtual_sports(self):
        """
        DESCRIPTION: Load Oxygen application and go to Virtual Sports
        EXPECTED: 'Horse Racing' page is opened
        Added new Virtual hub home page in FE,click on any one of top sport and navigate to main virtual sport page
        """
        self.site.open_sport(self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports')
        virtual_hub_home_page = self.cms_config.get_system_configuration_structure().get('VirtualHubHomePage')
        if virtual_hub_home_page.get('enabled'):
            virtual_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.upper() != self.next_events.upper()), None)
            virtual_sport = list(virtual_section.items_as_ordered_dict.values())[0]
            if self.device_type == 'mobile' and self.use_browser_stack and 'iPhone' in self._device.device_args.get('device'):
                virtual_sport.link.click()
            else:
                virtual_sport.click()
        virtual_sports_list = self.site.virtual_sports
        open_tab = virtual_sports_list.sport_carousel.open_tab(self.expected_tab)
        self.assertTrue(open_tab, msg=f'Tab "{self.expected_tab}" is not opened')

    def test_002_verify_the_page(self):
        """
        DESCRIPTION: Verify the page
        EXPECTED: The page contains the following elements:
        EXPECTED: * Header with a back button and "Virtual" label
        EXPECTED: * Sport carousel
        EXPECTED: * First accordion, which contains virtual sport play title, date and hour and "LIVE" label (for live events)
        EXPECTED: * Video stream window
        EXPECTED: * Event selector ribbon
        EXPECTED: * Markets with price odds buttons
        EXPECTED: **For Desktop:**
        EXPECTED: * Breadcrumbs are displayed below 'Virtual' header
        EXPECTED: * Breadcrumbs are displayed in the following format : 'Home' > 'Virtuals'
        """
        virtual_sports = self.site.virtual_sports
        sport_carousel_displayed = virtual_sports.sport_carousel.is_displayed()
        self.assertTrue(sport_carousel_displayed,
                        msg='Sport Carousel is not displayed')

        back_button_displayed = self.site.back_button.is_displayed()
        self.assertTrue(back_button_displayed,
                        msg='Back Button is not displayed')

        header_title_text = virtual_sports.header_line.page_title.sport_title
        self.assertEqual(header_title_text, vec.virtuals.VIRTUAL,
                         msg=f'Labels text does not match. '
                         f'Actual: "{header_title_text}". Expected: "{vec.virtuals.VIRTUAL}"')

        sport_header_event_name = virtual_sports.tab_content.sport_event_name
        self.assertTrue(sport_header_event_name, msg='Sport Event Name is not displayed')

        sport_header_time = virtual_sports.tab_content.sport_event_time.is_displayed()
        self.assertTrue(sport_header_time, msg='Sport Event Time is not displayed')

        sport_time = virtual_sports.tab_content.sport_event_timer
        time_format_match = re.match(r'\d+:\d+|^LIVE$', sport_time) is not None
        self.assertTrue(time_format_match,
                        msg=f'Displayed "{sport_time}" instead of Sport time or Live label')

        stream_window_displayed = virtual_sports.tab_content.stream_window.is_displayed()
        self.assertTrue(stream_window_displayed,
                        msg='Stream Window is not displayed')

        if virtual_sports.has_switchers():

            event_selector_ribbon_displayed = virtual_sports.tab_content.event_markets_list.is_displayed()
            self.assertTrue(event_selector_ribbon_displayed,
                            msg='Event selector ribbon is not displayed')

            markets_items_displayed = virtual_sports.tab_content.event_markets_list.market_tabs_list.is_displayed()
            self.assertTrue(markets_items_displayed, msg='Market is not displayed')

            selections = virtual_sports.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(selections, msg='No outcome was found in section')
            for selection_name, selection in selections.items():
                self.assertTrue(selection.bet_button.is_displayed(), msg=f'No bet button shown for outcome "{selection_name}"')
                self.assertTrue(selection.output_price, msg=f'No price shown for outcome "{selection_name}"')
        else:
            sections = virtual_sports.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found')
            current_url = self.device.get_current_url()
            url = current_url.split('/')[-1]
            if url == 'darts':
                self._logger.info(f'*** Darts do not have "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_betting}" market')
            else:
                match_betting = sections.get(vec.siteserve.EXPECTED_MARKETS_NAMES.match_betting)
                self.assertTrue(match_betting,
                                msg=f'"{vec.siteserve.EXPECTED_MARKETS_NAMES.match_betting}" market not found in {list(sections.keys())}')
                match_betting.expand()
                self.assertTrue(match_betting.is_expanded(), msg=f'"{vec.siteserve.EXPECTED_MARKETS_NAMES.match_betting}" is not expanded')
                selections = match_betting.outcomes.items_as_ordered_dict
                self.assertTrue(selections, msg=f'No selections found for "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_betting}" market')
                for selection_name, selection in selections.items():
                    self.assertTrue(selection.bet_button.is_displayed(), msg=f'No bet button show for outcome "{selection_name}"')
                    self.assertTrue(selection.output_price, msg=f'No price shown for outcome "{selection_name}"')

        if self.device_type == 'desktop':
            breadcrumbs = virtual_sports.breadcrumbs.items_as_ordered_dict
            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')
            self.assertEqual(list(breadcrumbs.keys()).index(vec.virtuals.VIRTUAL_HOME_BREADCRUMB), 0,
                             msg='Home page is not shown the first by default')
            self.assertEqual(list(breadcrumbs.keys()).index(vec.virtuals.VIRTUAL_SPORTS.title()), 1,
                             msg='Home page is not shown the first by default')

    def test_003_verify_display_order_of_virtual_sports(self):
        """
        DESCRIPTION: Verify display order of Virtual Sports
        EXPECTED: Virtual Sports are displayed according to СMS
        """
        # TODO add method in CMS VOL-5854
        # sport_category_names_from_page = self.site.virtual_sports.sport_carousel.menu_item_names
        # self.assertTrue(set(sport_category_names_from_page).issubset(set(expected_order_of_virtual_sports)),
        #                 msg=f'Order of virtual sports does not match expected order. '
        #                 f'\nActual: "{sport_category_names_from_page}".\nExpected: "{expected_order_of_virtual_sports}"')

    def test_004_navigate_to_a_different_event_of_the_same_virtual_sport_using_event_selector_ribbon(self):
        """
        DESCRIPTION: Navigate to a different event of the same virtual sport using event selector ribbon
        EXPECTED: User is able to navigate to a different event of the same virtual sport
        """
        virtual_sports_tabs = self.site.virtual_sports
        event_off_times_list = virtual_sports_tabs.tab_content.event_off_times_list
        virtual_sports_tabs_list = event_off_times_list.items_as_ordered_dict.keys()
        event_off_time_tab = list(virtual_sports_tabs_list)[2]
        event_off_times_list.select_off_time(event_off_time_tab)
        current_event = event_off_times_list.selected_item
        self.assertTrue(current_event,
                        msg=f'The user is not navigated to the event of the selected virtual sport event'
                        f'Actual: "{current_event}". Expected: "{event_off_time_tab}"')

    def test_005_navigate_to_a_different_virtual_sport_using_sport_carousel(self):
        """
        DESCRIPTION: Navigate to a different virtual sport using Sport carousel
        EXPECTED: User is navigated to the event of the selected virtual sport
        """
        virtual_sports_carousel = self.site.virtual_sports.sport_carousel
        carousel_items = virtual_sports_carousel.items_as_ordered_dict
        self.assertTrue(carousel_items, msg='No items found in sport carousel')
        carousel_items.pop(self.expected_tab)
        if not carousel_items:
            self._logger.warning('Only one Virtual sport is present')
            return
        different_sport_name, different_sport = list(carousel_items.items())[-1]

        virtual_sports_carousel.open_tab(different_sport_name)
        current_opened_sport_tab = virtual_sports_carousel.current
        self.assertEqual(current_opened_sport_tab, different_sport_name,
                         msg=f'The user is not navigated to the selected sport'
                         f'\nActual sport: "{current_opened_sport_tab}".\nExpected sport: "{different_sport_name}"')
