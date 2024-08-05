import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.prod_incident
@pytest.mark.your_call
@pytest.mark.event_details
@pytest.mark.ob_smoke
@pytest.mark.medium
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.safari
@vtest
class Test_C488641_YourCall_Special_Markets_on_Sports_Event_Details_Page(BaseSportTest):
    """
    TR_ID: C488641
    NAME: #YourCall Special Markets on Sport's Event Details Page
    DESCRIPTION: This test case verifies #YourCall Special Markets on Sport's Event Details Page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    DESCRIPTION: Note: #YourCall - Coral
    DESCRIPTION: #GetAPrice - Ladbrokes
    PRECONDITIONS: 1) To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to add new market use ti tool http://backoffice-tst2.coral.co.uk/ti/
    PRECONDITIONS: 3) In order to create new market use |YourCallSpecials| Market Template in ti tool
    PRECONDITIONS: 4) For Featured selections |Featured| market must be created using |YourCallSpecials| Market Template. All selections for this Market will be considered as Featured selections.
    PRECONDITIONS: 5) Position (tab of displaying) of #YourCallMarkets is depending on TI settings for |YourCallSpecials| Market Template
    PRECONDITIONS: 6) There is no restriction for selections displaying within Markets depending on price range on front-end side, all should be configured properly in TI Tool by Traders team
    PRECONDITIONS: 7) |YourCallSpecials| market template is available in TI tool for the following Football leagues:
    PRECONDITIONS: **Test 2:**
    PRECONDITIONS: Premier League - 597276
    PRECONDITIONS: La Liga - 599078
    PRECONDITIONS: Serie A - 599077
    PRECONDITIONS: Champions League - 599079
    PRECONDITIONS: **Stage:**
    PRECONDITIONS: Premier League 832526
    PRECONDITIONS: La Liga 832527
    PRECONDITIONS: Serie A 832528
    PRECONDITIONS: Champions League 832529
    PRECONDITIONS: **Production:**
    PRECONDITIONS: Premier League - 2308603
    PRECONDITIONS: La Liga - 2308604
    PRECONDITIONS: Serie A - 2308606
    PRECONDITIONS: Champions League - 2308607
    PRECONDITIONS: 8) |YourCallSpecials| market template is available in TI tool for the following leagues:
    PRECONDITIONS: NFL (American Football)
    PRECONDITIONS: NBA (Basketball)
    PRECONDITIONS: MLB (Baseball)
    PRECONDITIONS: AFL (Aussie Rules)
    """
    keep_browser_open = True
    event_not_your_call_id = None
    actual_your_call_markets = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event with #YourCall special markets available
        EXPECTED: Test event created
        """
        self.__class__.your_call_market = self.get_initial_data_system_configuration().get('YourCallMarket', {})
        if not self.your_call_market:
            self.your_call_market = self.cms_config.get_system_configuration_item('YourCallMarket')
        if not self.your_call_market.get('football'):
            raise CmsClientException('"YourCall" market name not found for football event in CMS')

        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_not_your_call_id = event_params.event_id
        event_params = self.ob_config.add_autotest_premier_league_football_event(markets=[('your_call', )])
        self.__class__.yourcall_markets = list(event_params.selection_ids.values())[0].keys()
        self.__class__.eventID = event_params.event_id

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.site.wait_content_state('homepage')

    def test_002_navigate_to_event_details_page_of_sports_event(self):
        """
        DESCRIPTION: Navigate to Event Details page of Sport's event
        EXPECTED: * Event Details page is opened successfully representing available markets
        EXPECTED: * 'Main Markets' tab is selected by default
        """
        self.navigate_to_edp(self.eventID)
        self.__class__.markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(self.markets_tabs_list,
                        msg='No one market tab found on event details page')
        markets_tabs = self.markets_tabs_list.items_as_ordered_dict
        self.assertTrue(markets_tabs, msg='No Market tabs found')
        self.verify_edp_market_tabs_order(markets_tabs.keys())
        current_tab = self.markets_tabs_list.current
        expected_tab = self.get_default_tab_name_on_sports_edp(event_id=self.eventID)
        self.assertEqual(current_tab, expected_tab,
                         msg=f'"{expected_tab}" is not active tab, active tab is "{current_tab}"')

    def test_003_choose_all_markets_tab(self):
        """
        DESCRIPTION: Choose 'All Markets' tab
        EXPECTED: * 'All Markets' tab is selected
        EXPECTED: * List of all available markets received in response from OB is displayed
        """
        self.markets_tabs_list.open_tab(vec.siteserve.EXPECTED_MARKET_TABS.all_markets)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, vec.siteserve.EXPECTED_MARKET_TABS.all_markets,
                         msg=f'"{vec.siteserve.EXPECTED_MARKET_TABS.all_markets}" is not active tab, active tab is "{current_tab}"')
        self.__class__.markets_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(vec.yourcall.MARKETS.market_result.upper(), list(self.markets_sections.keys()), msg=f'"{vec.yourcall.MARKETS.market_result}" market is not displayed')
        for market in self.yourcall_markets:
            self.assertIn(market.upper(), list(self.markets_sections.keys()), msg=f'"{market}" not found in the UI list "{self.markets_sections.keys()}"')

    def test_004_verify_that_yourcall_markets_are_present_on_the_page(self):
        """
        DESCRIPTION: Verify that '#YourCall' markets are present on the page
        EXPECTED: * '#YourCall' markets are present on Event Details Page
        """
        # covered in step 003

    def test_005_verify_displaying_of_yourcall_markets_if_there_are_no_created_any_market(self):
        """
        DESCRIPTION: Verify displaying of '#YourCall' markets if there are no created any market
        EXPECTED: '#YourCall' markets are not displayed on front-end
        """
        self.navigate_to_edp(self.event_not_your_call_id)
        markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(markets_tabs_list,
                        msg='No one market tab found on event details page')
        markets_tabs = markets_tabs_list.items_as_ordered_dict
        self.assertNotIn(self.expected_market_sections.yourcall, markets_tabs.keys(), msg=f'"{self.expected_market_sections.yourcall}" tab is displayed even there is no yourcall markets created')
        markets_tabs_list.open_tab(vec.siteserve.EXPECTED_MARKET_TABS.all_markets)
        markets_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_sections,
                        msg='There is no one market section on event details page')
        self.assertNotIn(self.yourcall_markets, list(markets_sections.keys()), msg=f'"{self.yourcall_markets}" market is displayed even there is no yourcall markets created')
