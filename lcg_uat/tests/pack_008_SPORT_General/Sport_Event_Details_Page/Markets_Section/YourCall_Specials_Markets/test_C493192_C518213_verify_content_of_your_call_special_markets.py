import voltron.environments.constants as vec
import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.crl_tst2  # coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.your_call
@pytest.mark.event_details
@pytest.mark.medium
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.safari
@vtest
class Test_C493192_C518213_Verify_Content_Of_Your_Call_Special_Markets(BaseSportTest):
    """
    TR_ID: C493192
    TR_ID: C518213
    VOL_ID: C9698316
    NAME: Verify content of #YourCall Special Markets on Sport's Event Details Page
    """
    keep_browser_open = True
    selection_name = 'Long selection name long selection name long selection name long selection name long selection name'

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

        event_params = self.ob_config.add_autotest_premier_league_football_event(
            markets=[('your_call', {'selection_prefix': self.selection_name})])
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
        self.navigate_to_edp(self.eventID, timeout=40)
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
        """"
        DESCRIPTION: Choose 'ALL MARKETS' tab
        EXPECTED: 'ALL MARKETS' tab is selected
        """
        self.markets_tabs_list.open_tab(vec.siteserve.EXPECTED_MARKET_TABS.all_markets)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, vec.siteserve.EXPECTED_MARKET_TABS.all_markets,
                         msg=f'"{vec.siteserve.EXPECTED_MARKET_TABS.all_markets}" is not active tab, active tab is "{current_tab}"')

    def test_004_find_any_of_yourcall_market_accordions(self):
        """
        DESCRIPTION: Find any of '#YourCall' market accordions
        EXPECTED: * '#YourCall' market accordion is present on Event Details Page;
        """
        self.__class__.markets_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        for market in self.yourcall_markets:
            self.assertIn(market.upper(), list(self.markets_sections.keys()), msg=f'"{market}" not found in the UI list "{self.markets_sections.keys()}"')

    def test_005_expand_yourcall_market_accordion(self):
        """
        DESCRIPTION: Expand '#YourCall' market accordion
        EXPECTED: Market is expanded, List of all available selections that are received in response from OB is displayed;
        EXPECTED: * The name of selection is displayed on the left side of card
        EXPECTED: * The text displayed within the selection extends to more than one line and not truncated
        """
        market = self.markets_sections.get(self.yourcall_markets[0])
        if not market.is_expanded():
            market.expand()
            self.assertTrue(market.is_expanded(), msg=f'"{self.markets_sections[self.yourcall_markets[0]]}'
                                                      f' accordion is not expanded"')
        actual_selection_name = market.outcome_name
        self.assertTrue(actual_selection_name, msg='Market: "%s" not contains any selections' % self.markets_sections[self.yourcall_markets[0]])
        self.assertIn(self.selection_name, actual_selection_name, msg=f'Actual selection "{actual_selection_name}" is not same as Expected selection "{self.selection_name}"')
