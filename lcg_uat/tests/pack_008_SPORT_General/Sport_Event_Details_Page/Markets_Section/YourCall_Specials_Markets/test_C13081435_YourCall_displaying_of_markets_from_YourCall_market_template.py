import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C13081435_YourCall_displaying_of_markets_from_YourCall_market_template(BaseSportTest):
    """
    TR_ID: C13081435
    NAME: #YourCall: displaying of markets from 'YourCall' market template
    DESCRIPTION: This test case verifies that YourCall markets are grouped within #YourCall markets accordion
    DESCRIPTION: Note: #YourCall - Coral
    DESCRIPTION: #GetAPrice - Ladbrokes
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have a Football event with couple markets added from market templates with "YourCall" word within the name
    PRECONDITIONS: - You should be on the event details page
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

        event_params = self.ob_config.add_autotest_premier_league_football_event(markets=[('your_call', )])
        self.__class__.yourcall_markets = list(event_params.selection_ids.values())[0].keys()
        self.__class__.eventID = event_params.event_id
        self.site.wait_content_state('homepage')
        self.navigate_to_edp(self.eventID, timeout=40)

    def test_001_verify_yourcall_markets_presence(self):
        """
        DESCRIPTION: Verify #YourCall markets presence
        EXPECTED: #YourCall markets are displayed according to Display Order setting in TI;
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

    def test_002_expand_yourcall_market_accordion_and_verify_displaying_of_selections(self):
        """
        DESCRIPTION: Expand #YourCall market accordion and verify displaying of selections
        EXPECTED: - All active YourCall markets added from market templates with "YourCall" word within the name are displayed with "#YourCall" prefix
        EXPECTED: - All active YourCall markets are displayed under separate accordions
        EXPECTED: - All active selections added to the markets above are displayed under respective markets
        """
        if self.brand == 'bma' and self.device_type == 'mobile':
            market = self.markets_sections.get(list(self.yourcall_markets)[0].upper())
        else:
            market = self.markets_sections.get(list(self.yourcall_markets)[0])
        if not market.is_expanded():
            market.expand()
            self.assertTrue(market.is_expanded(), msg=f'"{self.markets_sections[self.yourcall_markets[0]]}'
                                                      f' accordion is not expanded"')
        actual_selection_name = market.outcome_name
        self.assertTrue(actual_selection_name, msg='Market: "%s" not contains any selections' % market)

    def test_003_go_to_yourcall_tab_and_verify_displaying_of_markets_and_selections(self):
        """
        DESCRIPTION: Go to YourCall tab and verify displaying of markets and selections
        EXPECTED: - All active YourCall markets added from market templates with "YourCall" word within the name are displayed with "#YourCall" prefix
        EXPECTED: - All active YourCall markets are displayed under separate accordions
        EXPECTED: - All active selections added to the markets above are displayed under respective markets
        """
        if self.brand == 'bma':
            self.markets_tabs_list.open_tab(vec.siteserve.EXPECTED_MARKET_TABS.yourcall)
        else:
            self.markets_tabs_list.open_tab(vec.siteserve.EXPECTED_MARKET_TABS.get_a_price)

        expected_market_tab = vec.siteserve.EXPECTED_MARKET_TABS.yourcall \
            if self.brand == 'bma' else vec.siteserve.EXPECTED_MARKET_TABS.get_a_price

        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, expected_market_tab,
                         msg=f'"{expected_market_tab}" is not active tab, active tab is "{current_tab}"')
        markets_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        for market in self.yourcall_markets:
            if self.brand == 'bma' and self.device_type == 'mobile':
                market = market.upper()
            self.assertIn(market, list(markets_sections.keys()),
                          msg=f'"{market}" not found in the UI list "{markets_sections.keys()}"')
        self.assertTrue(markets_sections, msg='YourCall markets are not present')
