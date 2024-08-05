import re
from copy import copy
from random import choice

import pytest

import tests
from tests.base_test import vtest
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests

from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod  # This test changes CMS data (sports ordering), better do not run it on PROD
@pytest.mark.high
@pytest.mark.virtual_sports
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_C869700_Verify_Virtual_Sport_Page_and_List_of_Virtual_Sports_types(BaseVirtualsTest):
    """
    TR_ID: C869700
    NAME: Verify Virtual Sport Page and List of Virtual Sports types
    DESCRIPTION: This test case verifies the Virtual Sport page, list and order of Virtual Sports types
    PRECONDITIONS: Get SiteServer response to verify data:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/16231,289,288,285,286,287,290,291?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&simpleFilter=event.typeId:notEquals:3048&simpleFilter=event.typeId:notEquals:3049&simpleFilter=event.typeId:notEquals:3123&simpleFilter=event.startTime:lessThanOrEqual:2016-04-18T16:28:45Z&simpleFilter=event.startTime:greaterThan:2016-04-18T09:28:45Z&translationLang=en
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True
    parent_back_up_order = None
    parent_operapable_sport_id = None
    child_back_up_order = None
    child_operapable_sport_id = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()

        # revert parent virtual sports ordering
        if cls.parent_back_up_order:
            cms_config.set_parent_virtual_sports_ordering(new_order=cls.parent_back_up_order,
                                                          moving_item=cls.parent_operapable_sport_id)

        # revert child virtual sports ordering
        if cls.child_back_up_order:
            cms_config.set_child_virtual_sports_ordering(new_order=cls.child_back_up_order,
                                                         moving_item=cls.child_operapable_sport_id)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get list of active virtual sport categories
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

        self.__class__.parent_sport_list = []
        self.__class__.child_sport_list = []

        event = None
        ss_class_id = None
        self.__class__.active_categories = []
        for sport_class in sports_list:
            class_id = sport_class['class']['id']
            if not event:
                additional_filter = exists_filter(LEVELS.EVENT,
                                                  simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES,
                                                                OPERATORS.INTERSECTS, 'CF,TC')), exists_filter(
                    LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE,
                                                OPERATORS.IS_TRUE))
                events = self.get_active_event_for_class(class_id=class_id,
                                                         additional_filters=additional_filter,
                                                         raise_exceptions=False)
                if events:
                    temp_event = choice(events)
                    temp_ss_class_id = temp_event['event']['classId']
                    if temp_ss_class_id in virtuals_cms_class_ids:
                        event = temp_event
                        ss_class_id = temp_ss_class_id

            events = self.get_active_event_for_class(class_id=class_id,
                                                     raise_exceptions=False)
            if events:
                temp_event = choice(events)
                temp_ss_class_id = temp_event['event']['classId']
                if temp_ss_class_id in virtuals_cms_class_ids:
                    self.active_categories.append(temp_ss_class_id)
        if not event or not ss_class_id:
            raise SiteServeException('There are no available race virtual events')

        tab_name = self.cms_virtual_sport_tab_name_by_class_ids(class_ids=[ss_class_id])
        self.__class__.expected_tab = tab_name[0]

        self.__class__.parent_sport_list = self.get_cms_unique_virtual_sport_tab_name_by_class_ids_by_cms_order(class_ids=self.active_categories)

    def test_001_open_virtual_sports(self):
        """
        DESCRIPTION: Open Virtual Sports page.
        EXPECTED: 1. The first track from CMS is displayed as default. The display order of the tracks should be as per the CMS.
        EXPECTED: 2. The 'Virtual Sports' page displayed with header contains all icons for the virtual, sorted as configured on CMS.
        """
        self.site.open_sport(self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports')
        self.__class__.virtual_sports_list = self.site.virtual_sports
        self.virtual_sports_list.sport_carousel.open_tab(self.expected_tab)

    def test_002_verify_the_virtuals_page(self):
        """
        DESCRIPTION: Verify the page
        EXPECTED: The page contains the following elements:
        EXPECTED: Sport carousel
        EXPECTED: Header with a back button and "Virtual" label
        EXPECTED: Virtual sports icon
        EXPECTED: Video stream window
        EXPECTED: Live and Timer bages icons under Video stream section
        EXPECTED: Child sports navigation
        EXPECTED: Event selector ribbon
        EXPECTED: Markets with price odds buttons
        """
        sport_carousel_displayed = self.virtual_sports_list.sport_carousel.is_displayed()
        self.assertTrue(sport_carousel_displayed, msg='Sport Carousel is not displayed')

        back_button_displayed = self.site.back_button.is_displayed()
        self.assertTrue(back_button_displayed, msg='Back Button is not displayed')

        sports_tabs = self.virtual_sports_list.sport_carousel.items_as_ordered_dict
        self.assertTrue(sports_tabs, msg="Virtual Carousel is empty")
        sport_tab = sports_tabs.get(self.expected_tab, None)
        self.assertTrue(sport_tab, msg=f'Sport tab "{self.expected_tab}" does not exist')
        self.assertTrue(sport_tab.has_icon(),
                        msg=f'"{self.expected_tab}" icon is not displayed in the Sports carousel')

        sport_header_date_text = self.virtual_sports_list.tab_content.sport_event_time.is_displayed()
        self.assertTrue(sport_header_date_text,
                        msg='Sport Date is not displayed')

        sport_time = self.virtual_sports_list.tab_content.sport_event_timer
        time_format_match = re.match('\d+:\d+|^LIVE$', sport_time) is not None
        self.assertTrue(time_format_match,
                        msg=f'Displayed "{sport_time}" instead of Sport time or Live label')

        stream_window_displayed = self.virtual_sports_list.tab_content.stream_window.is_displayed()
        self.assertTrue(stream_window_displayed, msg='Stream Window is not displayed')

        event_selector_ribbon_displayed = self.virtual_sports_list.tab_content.event_markets_list.is_displayed()
        self.assertTrue(event_selector_ribbon_displayed,
                        msg='Event selector ribbon is not displayed')

        markets_items_displayed = self.virtual_sports_list.tab_content.event_markets_list.market_tabs_list.is_displayed()
        self.assertTrue(markets_items_displayed,
                        msg='Market is not displayed')

        selections = self.virtual_sports_list.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(selections, msg='No outcome was found in section')
        for name, button in selections.items():
            self.assertTrue(button.bet_button.is_displayed(), msg=f'No bet buttons for outcome "{name}"')

    def test_003_verify_the_list_of_virtual_sports_in_the_sport_carousel(self):
        """
        DESCRIPTION: Verify the list of Virtual Sports in the Sport carousel
        EXPECTED: The list corresponds to the list in SiteServer response
        """
        sport_category_names_from_page = self.site.virtual_sports.sport_carousel.items_names
        self.assertSetEqual(set(sport_category_names_from_page), set(self.parent_sport_list),
                            msg=f'"{set(sport_category_names_from_page)}" is not equal to expected'
                                f'"{set(self.parent_sport_list)}" from SiteServer response')

    def test_004_change_order_of_parent_sports_on_cms_and_verify(self):
        """
        DESCRIPTION: Change order of Parent Sports on CMS and verify on FE
        EXPECTED: The Parent Sports are displayed according to new CMS configuration
        """
        self.softAssert(self.assertTrue, len(self.parent_sport_list) >= 2,
                        msg='Only one parent virtual sport is present, cannot verify FE ordering')

        operapable_sport_name = self.parent_sport_list[-1]
        virtual_sports_data = self.cms_config.get_parent_virtual_sports()
        self.__class__.parent_operapable_sport_id = next((sport['id'] for sport in virtual_sports_data if sport['title'] == operapable_sport_name), '')
        if not self.parent_operapable_sport_id:
            raise VoltronException(f'Cannot find sport id for {operapable_sport_name}')

        self.__class__.parent_back_up_order = [sport['id'] for sport in virtual_sports_data]

        # moving element from any position to the first position
        new_order = copy(self.parent_back_up_order)
        new_order.remove(self.parent_operapable_sport_id)
        new_order.insert(0, self.parent_operapable_sport_id)

        expected_sport_order = copy(self.parent_sport_list)
        expected_sport_order.remove(operapable_sport_name)
        expected_sport_order.insert(0, operapable_sport_name)

        self.cms_config.set_parent_virtual_sports_ordering(new_order=new_order, moving_item=self.parent_operapable_sport_id)

        wait_for_result(lambda: self.get_virtual_sport_ids() == new_order,
                        name='Waiting to parent virtual sports new order to apply',
                        poll_interval=5,
                        timeout=180)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        sport_category_names_from_page = self.site.virtual_sports.sport_carousel.items_names
        self.assertListEqual(sport_category_names_from_page, expected_sport_order,
                             msg=f'"{sport_category_names_from_page}" is not equal to expected'
                                 f'"{expected_sport_order}" from CMS order')

    def test_005_change_order_of_event_sports_on_cms_and_verify_on_fe_ox1021(self):
        """
        DESCRIPTION: Change order of Event Sports on CMS and verify on FE
        EXPECTED: The Child Sports are displayed according to new CMS configuration
        """
        parent_dict = self.get_parent_virtual_sport_with_more_than_one_child(self.active_categories)
        self.softAssert(self.assertTrue, parent_dict,
                        msg='There is no parent virtual sports with 2 or more child so cannot verify child ordering')

        operapable_parent, parent_id = parent_dict.popitem()

        self.site.virtual_sports.sport_carousel.open_tab(operapable_parent)

        children_data = self.cms_config.get_child_virtual_sports(parent_id)
        children_ordered_names = [child.get('title') for child in children_data]
        children_ordered_ids = [child.get('id') for child in children_data]

        self.__class__.child_back_up_order = copy(children_ordered_ids)

        child_operapable_sport_name = children_ordered_names[-1]
        self.__class__.child_operapable_sport_id = children_ordered_ids[-1]

        # moving element from any position to the first position
        children_ordered_names.remove(child_operapable_sport_name)
        children_ordered_names.insert(0, child_operapable_sport_name)

        children_ordered_ids.remove(self.child_operapable_sport_id)
        children_ordered_ids.insert(0, self.child_operapable_sport_id)

        self.cms_config.set_child_virtual_sports_ordering(new_order=children_ordered_ids, moving_item=self.child_operapable_sport_id)

        wait_for_result(lambda: self.get_child_virtual_sport_ids_for_parent(operapable_parent) == children_ordered_ids,
                        name=f'Waiting to child of "{operapable_parent}" virtual sports new order to apply',
                        poll_interval=5,
                        timeout=180)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        children_ordered_names = [name.upper() for name in children_ordered_names]  # both brands and devices upper
        children_virtual_sports_names = self.site.virtual_sports.tab_content.child_sport_carousel.items_names
        self.assertListEqual(children_virtual_sports_names, children_ordered_names,
                             msg=f'"{children_virtual_sports_names}" is not equal to expected'
                                 f'"{children_ordered_names}" from CMS order')

    def test_006_navigate_to_a_different_event_of_the_same_virtual_sport_using_event_selector_ribbon(self):
        """
        DESCRIPTION: Navigate to a different event of the same virtual sport using event selector ribbon
        EXPECTED: User is able to navigate to a different event of the same virtual sport
        """
        virtual_sports_tabs = self.site.virtual_sports.tab_content.event_off_times_list
        items_list = virtual_sports_tabs.items_names
        items_list.remove(virtual_sports_tabs.selected_item)
        new_event = choice(items_list)
        virtual_sports_tabs.click_item(new_event)
        wait_for_result(lambda: virtual_sports_tabs.selected_item == new_event,
                        timeout=2,
                        name='Current tab to be changed')
        current_event = virtual_sports_tabs.selected_item
        self.assertEqual(current_event, new_event,
                         msg=f'The user is not navigated to the event of the selected virtual sport event'
                             f'Actual: "{current_event}". Expected: "{new_event}"')

    def test_007_navigate_to_a_different_virtual_sport_using_sport_carousel(self):
        """
        DESCRIPTION: Navigate to a different virtual sport using Sport carousel
        EXPECTED: User is navigated to the event of the selected virtual sport
        """
        virtual_sport_page = self.site.virtual_sports
        current_tab = virtual_sport_page.sport_carousel.current

        all_sports = virtual_sport_page.sport_carousel.items_names
        all_sports.remove(current_tab)
        new_sport = choice(all_sports)

        virtual_sport_page.sport_carousel.open_tab(new_sport)

        self.assertEqual(virtual_sport_page.sport_carousel.current, new_sport,
                         msg=f'The user is not navigated to the selected sport'
                             f'\nActual sport: "{virtual_sport_page.sport_carousel.current}".\nExpected sport: "{new_sport}"')
