import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create events in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C59499271_YourCall_markets_grouping_on_All_Markets_tab(BaseSportTest):
    """
    TR_ID: C59499271
    NAME: YourCall markets grouping on All Markets tab
    DESCRIPTION: This TC verifies the appearance of YourCall markets on All Markets tab
    DESCRIPTION: Note: #YourCall - Coral
    DESCRIPTION: #GetAPrice - Ladbrokes
    PRECONDITIONS: YourCall markets are available for an event;
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event with #YourCall special markets available
        EXPECTED: Test event created
        """
        self.__class__.your_call_market = self.get_initial_data_system_configuration().get('YourCallMarket', {})
        if not self.your_call_market:
            self.your_call_market = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not self.your_call_market.get('football'):
            raise CmsClientException('"YourCall" market name not found for football event in CMS')
        event_params = self.ob_config.add_autotest_premier_league_football_event(markets=[('your_call',)])
        self.__class__.yourcall_markets = list(event_params.selection_ids.values())[0].keys()
        self.__class__.eventID = event_params.event_id

    def test_001_log_in_to_application_and_go_to_football_event_edp(self):
        """
        DESCRIPTION: Log in to application and go to Football event EDP;
        EXPECTED: User is on EDP, Main tab;
        """
        self.navigate_to_edp(self.eventID, timeout=40)

    def test_002_go_to_all_markets_tab_and_review_the_market_grouping(self):
        """
        DESCRIPTION: Go to All Markets tab and review the market grouping;
        EXPECTED: - YourCall markets are present on this tab along with other markets;
        EXPECTED: - markets are not grouped under one header;
        EXPECTED: - market order is set according to backoffice setting "Display Order";
        EXPECTED: - YourCall market layout should be equal to standard market layout comparing to other tabs;
        EXPECTED: - top two/four markets are expanded by default (on Mobile/Desktop);
        """
        self.__class__.markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(self.markets_tabs_list,
                        msg='No one market tab found on event details page')
        markets_tabs = self.markets_tabs_list.items_as_ordered_dict
        self.assertTrue(markets_tabs, msg='No Market tabs found')
        self.verify_edp_market_tabs_order(markets_tabs.keys())
        self.markets_tabs_list.open_tab(vec.siteserve.EXPECTED_MARKET_TABS.all_markets)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, vec.siteserve.EXPECTED_MARKET_TABS.all_markets,
                         msg=f'"{vec.siteserve.EXPECTED_MARKET_TABS.all_markets}" is not active tab, active tab is "{current_tab}"')
        self.__class__.markets_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        if self.brand == 'bma' and self.device_type == 'mobile':
            market_section_names = vec.yourcall.MARKETS.market_result.upper()
        else:
            market_section_names = vec.yourcall.MARKETS.market_result
        self.assertIn(market_section_names, list(self.markets_sections.keys()),
                      msg=f'"{vec.yourcall.MARKETS.market_result}" market is not displayed')
        for market in self.yourcall_markets:
            if self.brand == 'bma' and self.device_type == 'mobile':
                market = market.upper()
            self.assertIn(market, list(self.markets_sections.keys()),
                          msg=f'"{market}" not found in the UI list "{self.markets_sections.keys()}"')

        self.assertTrue(list(self.markets_sections.values())[0].is_expanded(),
                        msg='First market is not expanded by default')
        self.assertTrue(list(self.markets_sections.values())[1].is_expanded(),
                        msg='Second market is not expanded by default')

    def test_003_try_to_expandcollapse_markets(self):
        """
        DESCRIPTION: Try to expand/collapse markets;
        EXPECTED: Each market should be independently expandable / collapsable;
        """
        for market in self.markets_sections.values():
            if market.is_expanded():
                market.collapse()
                self.assertFalse(market.is_expanded(), msg='Markets are not collapsed after click')
                market.expand()
                self.assertTrue(market.is_expanded(), msg='Markets are not expanded after click')
                continue
            if not market.is_expanded():
                market.expand()
                self.assertTrue(market.is_expanded(), msg='Markets are not expanded after click')
                market.collapse()
                self.assertFalse(market.is_expanded(), msg='Markets are not collapsed after click')
                continue
