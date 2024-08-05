import pytest
import tests
from time import sleep
from selenium.common.exceptions import WebDriverException
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C1992664_Verify_sticky_Market_Collections_section(Common):
    """
    TR_ID: C1992664
    NAME: Verify sticky Market Collections section
    DESCRIPTION: This test case verifies sticky Market Collections section on Sport EDP
    PRECONDITIONS: * Test case is applicable to **Mobile** and **Tablet** only
    PRECONDITIONS: * User is logged out
    """
    keep_browser_open = True

    def is_element_displayed(self, element):
        """
        Method to click on the element if visible on the page
        :param element: Element to be clicked on
        :return: True or False
        """
        try:
            element.check_click()  # if element is displayed, the element is clicked
        except WebDriverException:
            return False
        return True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load the app
        PRECONDITIONS: Go to the basketball Landing Page -> 'Click on Competition Tab'
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event.event_id

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_go_to_sport_event_details_page(self):
        """
        DESCRIPTION: Go to <Sport> Event Details page
        EXPECTED: * <Sport> Event Details page is opened
        EXPECTED: * List of market collections are displayed below event name and date
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.__class__.markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No markets are shown')

    def test_003_scroll_down_the_page(self):
        """
        DESCRIPTION: Scroll down the page
        EXPECTED: * Market collections are sticky and displayed below <Sport> header
        EXPECTED: * Event name and date are NOT shown
        """
        self.site.contents.scroll_to_bottom()
        self.assertTrue(self.site.footer.is_displayed(), msg='Footer is not displayed')
        self.assertFalse(self.is_element_displayed(self.site.sport_event_details.event_title_bar.event_name_we),
                         msg='"Event Name" is displayed')
        self.assertFalse(self.is_element_displayed(self.site.sport_event_details.event_title_bar.event_time_we),
                         msg='"Event Time" is displayed')

    def test_004_expandcollapse_any_market_panel(self):
        """
        DESCRIPTION: Expand/collapse any market panel
        EXPECTED: * Chosen market panel is expanded/collapsed
        EXPECTED: * Market collections remain sticky
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='markets are not listed')

        for market_name, market in list(markets.items()):
            if not market.is_expanded():
                market.click()
                self.assertTrue(market.is_expanded(), msg=f'market "{market_name}" is not expanded by tapping')
                break

        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='market collections are not sticky')

    def test_005_tap_any_collection_on_sticky_market_collections_section(self):
        """
        DESCRIPTION: Tap any collection on sticky Market collections section
        EXPECTED: * Particular market collection is opened with corresponding markets
        EXPECTED: * Page is auto-scrolled to the top of the market collection
        """
        markets_tabs_list = self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict
        self.assertTrue(markets_tabs_list,
                        msg='No one market tab found on event details page')
        for tab_name, tab in markets_tabs_list.items():
            if not tab.is_selected():
                tab.click()
                sleep(3)
                self.assertEqual(self.site.sport_event_details.markets_tabs_list.current, tab_name,
                                 msg=f'navigation to the expected tab link "{tab_name}" is not successful')
                markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(markets, msg='markets are not listed')
                break
        # self.assertTrue(self.is_element_displayed(self.site.sport_event_details.event_title_bar.event_name_we),
        #                 msg='Page is auto scrolled to the top')
        self.assertTrue(list(markets_tabs_list.values())[0].is_displayed(),
                        msg='Page is auto scrolled to the top')

    def test_006_scroll_down_the_page_until_the_end_of_its_content(self):
        """
        DESCRIPTION: Scroll down the page until the end of its content
        EXPECTED: * Market collections is NOT displayed when no content is present
        EXPECTED: * Global Footer is displayed only
        """
        markets_tabs_list = self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict
        self.site.footer.scroll_to_bottom()
        wait_for_haul(1)
        self.assertFalse(self.is_element_displayed(list(markets_tabs_list.values())[0]),
                         msg='"Market Collections" is displayed')
        self.assertTrue(self.site.footer.is_displayed(), msg='Footer is not displayed')

    def test_007_log_in_and_repeat_steps_2_6(self):
        """
        DESCRIPTION: Log in and repeat steps #2-6
        EXPECTED: As per steps
        """
        self.navigate_to_page('Home')
        self.site.wait_content_state('Homepage')
        self.site.login(username=tests.settings.betplacement_user)
        self.test_002_go_to_sport_event_details_page()
        self.test_003_scroll_down_the_page()
        self.test_004_expandcollapse_any_market_panel()
        self.test_005_tap_any_collection_on_sticky_market_collections_section()
        self.test_006_scroll_down_the_page_until_the_end_of_its_content()
