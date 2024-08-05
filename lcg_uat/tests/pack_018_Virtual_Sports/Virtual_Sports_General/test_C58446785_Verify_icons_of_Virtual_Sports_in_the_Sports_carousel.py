from random import choice
import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.virtual_sports
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.reg157_fix
@vtest
class Test_C58446785_Verify_Parent_Sports_icons_of_Virtual_Sports(BaseVirtualsTest):
    """
    TR_ID: C58446785
    NAME: Verify Parent Sports icons of Virtual Sports
    DESCRIPTION: This test case verifies the icons for all Virtual sport types
    PRECONDITIONS: Get SiteServer response to verify data:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForClass/2
    85?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: x.xx - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: List of relevant class id's:
    PRECONDITIONS: Horse Racing class id 285
    PRECONDITIONS: Greyhounds class id 286
    PRECONDITIONS: Football class id 287
    PRECONDITIONS: Motorsports class id 288
    PRECONDITIONS: Speedway class id 289
    PRECONDITIONS: Cycling class id 290
    PRECONDITIONS: Tennis class id 291
    PRECONDITIONS: Darts class id 26615
    PRECONDITIONS: Boxing class id 26614
    PRECONDITIONS: Grand National class id 26604
    """
    keep_browser_open = True
    mapping = None
    next_events = vec.virtuals.VIRTUAL_HUB_NEXT_EVENTS

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
        event = None
        sports_list_with_active_events = []
        for sport_class in sports_list:
            class_id = sport_class['class']['id']
            events = self.get_active_event_for_class(class_id=class_id, raise_exceptions=False)
            if not events:
                continue
            event = choice(events)
            ss_class_id = event['event']['classId']
            if ss_class_id in virtuals_cms_class_ids:
                sports_list_with_active_events.append(ss_class_id)
            else:
                continue
        if not event:
            raise SiteServeException('There are no available virtual event with Forecast tab')
        sports_name_ids = {}
        for ss_all_class_id in sports_list_with_active_events:
            for item in self.virtual_carousel_menu_items:
                for tracks in item.get('tracks', None):
                    if tracks.get('classId', None) == ss_all_class_id:
                        sports_name_ids.update({item['title']: ss_all_class_id})

        # Take all sports class IDs related to Virtual category
        self.__class__.expected_sports = list(sports_name_ids.keys())

    def test_001_go_to_virtual_sports(self):
        """
        DESCRIPTION: Go to 'Virtual Sports'
        EXPECTED: 'Virtual Sports' page displayed with header contains all icons for the virtual, sorted as configured on CMS
        EXPECTED: First configured on CMS sport displayed on the page load
        EXPECTED: When Parent Sport has on Child Sports configured on CMS, icon should not appear in header
        EXPECTED: Virtuals Sports/Parent Sports header displayed according to designs:
        EXPECTED: https://app.zeplin.io/project/5d64f0e582415f9b2a7045aa
        """
        self.site.open_sport(self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports', timeout=20)

        # Added new Virtual hub home page in FE,click on any one of top sport and navigate to main virtual sport page
        virtual_hub_home_page = self.cms_config.get_system_configuration_structure().get('VirtualHubHomePage')
        if virtual_hub_home_page.get('enabled'):
            hubs_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.upper() != self.next_events.upper()), None)
            section_sports = list(hubs_section.items_as_ordered_dict.values())[0]
            section_sports.click()

    def test_002_check_header_scrolling(self):
        """
        DESCRIPTION: Check header scrolling
        EXPECTED: Header should be scrollable to fit all the sports
        """
        # We can not verify scrolling
        pass

    def test_003_verify_sport_icon_in_the_sports_carousel(self, sport_name=vec.virtuals.VIRTUAL_HORSE_RACING):
        """
        DESCRIPTION: Verify 'Horse Racing' icon in the Sports carousel
        EXPECTED: Horse racing icon is displayed in the Sports carousel
        """
        carousel_items = self.site.virtual_sports.sport_carousel.items_names
        legends = next((item for item in carousel_items if item.upper() == 'LEGENDS'), None)
        if legends:
            carousel_items.remove(legends)
        self.assertEqual(set(carousel_items), set(self.expected_sports),
                         msg=f'Menu items on UI "{set(carousel_items)}" are not '
                             f'the same as from get from CMS "{set(self.expected_sports)}"')
        if sport_name in self.expected_sports:
            virtual_sports_carousel = self.site.virtual_sports.sport_carousel
            virtual_sports_carousel.open_tab(sport_name)
            sports_tabs = virtual_sports_carousel.items_as_ordered_dict
            self.assertTrue(sports_tabs, msg="Virtual Carousel is empty")
            sport_tab = sports_tabs.get(sport_name)
            self.assertTrue(sport_tab, msg=f'Sport tab "{sport_name}" does not exist')
            self.assertTrue(sport_tab.has_icon(),
                            msg=f'"{sport_name}" icon not is displayed in the Sports carousel')
        else:
            self._logger.warning(f'*** Skipping step since no "{sport_name}" is present on the virtual carousel')

    def test_004_choose_another_sport_from_virtuals_sports_parent_sports_header(self, sport_name=vec.virtuals.VIRTUAL_HORSE_RACING):
        """
        DESCRIPTION: Choose another sport from Virtuals Sports/Parent Sports header
        EXPECTED: - Icon is hyperlinked
        EXPECTED: - User is redirected to sport page
        EXPECTED: User is redirected to other Parent sports page
        EXPECTED: First Child Sport opened
        EXPECTED: Events/Markets related to that sport displayed
        """
        if sport_name in self.expected_sports:
            sports_tabs = self.site.virtual_sports.sport_carousel.items_as_ordered_dict
            self.assertTrue(sports_tabs, msg="Virtual Carousel is empty")
            sport_tab = sports_tabs.get(sport_name)
            self.assertTrue(sport_tab, msg=f'Sport tab {sport_name} does not exist')
            sport_tab.scroll_to()
            self.assertTrue(sport_tab.icon.has_link,
                            msg=f'{sport_name} icon is not hyperlinked')
            sport_tab.click_sport_icon()
            current_event = self.site.virtual_sports.sport_carousel.current
            self.assertEqual(current_event, sport_name,
                             msg=f'The user is not redirected to sport page.'
                             f'\nActual: "{current_event}". Expected: "{sport_name}"')
        else:
            self._logger.warning(f'*** Skipping step since no "{sport_name}" is present on the virtual carousel')

    def test_005_repeat_this_test_case_for_greyhounds(self, sport_name=vec.virtuals.VIRTUAL_GREYHOUNDS):
        """
        DESCRIPTION: Repeat this test case for Greyhounds
        """
        if sport_name in self.expected_sports:
            self.test_003_verify_sport_icon_in_the_sports_carousel(sport_name)
            self.test_004_choose_another_sport_from_virtuals_sports_parent_sports_header(sport_name)
            virtual_sports_list = self.site.virtual_sports
            markets_items_displayed = virtual_sports_list.tab_content.event_markets_list.market_tabs_list.is_displayed()
            self.assertTrue(markets_items_displayed,
                            msg='Market is not displayed')
            event_selector_ribbon_displayed = virtual_sports_list.tab_content.event_markets_list.is_displayed()
            self.assertTrue(event_selector_ribbon_displayed,
                            msg='Event selector ribbon is not displayed')
        else:
            self._logger.info(f'*** Skipping step since no "{sport_name}" is present on the virtual carousel')

    def test_006_repeat_this_test_case_for_football(self, sport_name=vec.virtuals.VIRTUAL_FOOTBALL):
        """
        DESCRIPTION: Repeat this test case for Football
        """
        if sport_name in self.expected_sports:
            self.test_003_verify_sport_icon_in_the_sports_carousel(sport_name)
            self.test_004_choose_another_sport_from_virtuals_sports_parent_sports_header(sport_name)
        else:
            self._logger.info(f'*** Skipping step since no "{sport_name}" is present on the virtual carousel')

    def test_007_repeat_this_test_case_for_motorsports(self, sport_name=vec.virtuals.VIRTUAL_MOTORSPORTS):
        """
        DESCRIPTION: Repeat this test case for Motorsports
        """
        if sport_name in self.expected_sports:
            self.test_003_verify_sport_icon_in_the_sports_carousel(sport_name)
            self.test_004_choose_another_sport_from_virtuals_sports_parent_sports_header(sport_name)
            virtual_sports_list = self.site.virtual_sports
            markets_items_displayed = virtual_sports_list.tab_content.event_markets_list.market_tabs_list.is_displayed()
            self.assertTrue(markets_items_displayed,
                            msg='Market is not displayed')
            event_selector_ribbon_displayed = virtual_sports_list.tab_content.event_markets_list.is_displayed()
            self.assertTrue(event_selector_ribbon_displayed,
                            msg='Event selector ribbon is not displayed')
        else:
            self._logger.info(f'*** Skipping step since no "{sport_name}" is present on the virtual carousel')

    def test_008_repeat_this_test_case_for_cycling(self, sport_name=vec.virtuals.VIRTUAL_CYCLING):
        """
        DESCRIPTION: Repeat this test case for Cycling
        """
        if sport_name in self.expected_sports:
            self.test_003_verify_sport_icon_in_the_sports_carousel(sport_name)
            self.test_004_choose_another_sport_from_virtuals_sports_parent_sports_header(sport_name)
            virtual_sports_list = self.site.virtual_sports
            markets_items_displayed = virtual_sports_list.tab_content.event_markets_list.market_tabs_list.is_displayed()
            self.assertTrue(markets_items_displayed,
                            msg='Market is not displayed')
            event_selector_ribbon_displayed = virtual_sports_list.virtual_sports_list.tab_content.event_markets_list.is_displayed()
            self.assertTrue(event_selector_ribbon_displayed,
                            msg='Event selector ribbon is not displayed')
        else:
            self._logger.info(f'*** Skipping step since no "{sport_name}" is present on the virtual carousel')

    def test_009_repeat_this_test_case_for_speedway(self, sport_name=vec.virtuals.VIRTUAL_SPEEDWAY):
        """
        DESCRIPTION: Repeat this test case for Speedway
        """
        if sport_name in self.expected_sports:
            self.test_003_verify_sport_icon_in_the_sports_carousel(sport_name)
            self.test_004_choose_another_sport_from_virtuals_sports_parent_sports_header(sport_name)
            virtual_sports_list = self.site.virtual_sports
            markets_items_displayed = virtual_sports_list.virtual_sports_list.tab_content.event_markets_list.market_tabs_list.is_displayed()
            self.assertTrue(markets_items_displayed,
                            msg='Market is not displayed')
            event_selector_ribbon_displayed = virtual_sports_list.virtual_sports_list.tab_content.event_markets_list.is_displayed()
            self.assertTrue(event_selector_ribbon_displayed,
                            msg='Event selector ribbon is not displayed')
        else:
            self._logger.info(f'*** Skipping step since no "{sport_name}" is present on the virtual carousel')

    def test_010_repeat_this_test_case_for_grand_national(self, sport_name=vec.virtuals.VIRTUAL_GRAND_NATIONAL):
        """
        DESCRIPTION: Repeat this test case for Grand National
        """
        if sport_name in self.expected_sports:
            self.test_003_verify_sport_icon_in_the_sports_carousel(sport_name)
            self.test_004_choose_another_sport_from_virtuals_sports_parent_sports_header(sport_name)
        else:
            self._logger.info(f'*** Skipping step since no "{sport_name}" is present on the virtual carousel')

    def test_011_repeat_this_test_case_for_tennis(self, sport_name=vec.virtuals.VIRTUAL_TENNIS):
        """
        DESCRIPTION: Repeat this test case for Tennis
        """
        if sport_name in self.expected_sports:
            self.test_003_verify_sport_icon_in_the_sports_carousel(sport_name)
            self.test_004_choose_another_sport_from_virtuals_sports_parent_sports_header(sport_name)
        else:
            self._logger.info(f'*** Skipping step since no "{sport_name}" is present on the virtual carousel')
