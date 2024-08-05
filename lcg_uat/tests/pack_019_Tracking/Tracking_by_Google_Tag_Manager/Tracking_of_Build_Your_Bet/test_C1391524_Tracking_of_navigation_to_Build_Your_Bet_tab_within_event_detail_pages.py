import pytest

import tests
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseYourCallTrackingTest
import voltron.environments.constants as vec


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.google_analytics
@pytest.mark.banach
@pytest.mark.build_your_bet
@pytest.mark.mocked_data
@pytest.mark.cms
@pytest.mark.slow
@pytest.mark.other
@vtest
class Test_C1391524_Tracking_of_navigation_to_Build_Your_Bet_tab_within_event_detail_pages(BaseBanachTest, BaseYourCallTrackingTest):
    """
    TR_ID: C1391524
    TR_ID: C1391532
    TR_ID: C1391619
    TR_ID: C1391650
    VOL_ID: C9697958
    NAME: Tracking of navigation to Build Your Bet tab within event detail pages
    DESCRIPTION:  Verify <Race> events carousel Race Time & Meeting
    PRECONDITIONS: 1. Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: 2. Browser console should be opened
    """
    keep_browser_open = True
    market_names = {'match_betting', 'both_teams_to_score', 'double_chance'}

    def add_byb_selection_to_dashboard(self, market_name: str, switcher_name: str = None, **kwargs) -> list:
        """
        :param market_name: Name of market
        :param switcher_name: Name of switcher button (only for markets with switchers)
        :param kwargs: Prioritized market selection parameters:
          - add selection outcome by name  if 'selection_name' specified;
          - add selection outcome by index if 'selection_index' specified;
          - add specified selections count is 'count' specified;
          - add all market selections if **kwargs empty
        :return: selection_names: List of added selections names
        """
        market = self.get_market(market_name=market_name)
        if switcher_name:
            result = market.grouping_buttons.click_button(switcher_name)
            self.assertTrue(result, msg=f'Switcher "{switcher_name}" is not active for "{market_name}"')
        selection_names = market.set_market_selection(**kwargs)
        self.assertTrue(selection_names, msg='No selection from "%s" was added to Dashboard' % market_name)
        expected_result = kwargs.get('expected_result', True)
        self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=expected_result)
        if expected_result:
            self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)
            self.__class__.initial_counter += 1
        return selection_names

    def expand_collapse_market(self, market_name, collapse=False):
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='Can not find market list "%s"' % markets_list)
        market = markets_list.get(market_name)
        self.assertTrue(market, msg='Can not get market "%s"' % market_name)
        if collapse:
            market.collapse()
            self.assertFalse(market.is_expanded(), msg='"%s" section is not expanded' % market_name)
        else:
            market.expand()
            self.assertTrue(market.is_expanded(), msg='"%s" section is not expanded' % market_name)

    def test_000_check_ob_event_is_active_to_use_in_mock(self):
        """
        DESCRIPTION: Get OB event to use in mock service
        """
        self.__class__.eventID = self.create_ob_event_for_mock()
        self._logger.info('*** Created BYB event id "%s"' % self.eventID)

    def test_001_turn_on_required_yourcall_league_in_cms(self):
        """
        DESCRIPTION: Check if required #YourCall league enabled in CMS and turn it on if not
        """
        self.cms_config.your_call_league_switcher()

    def test_002_navigate_to_yourcall_detail_page(self):
        """
        DESCRIPTION: Click on 'Go to Event' link within the #YourCall accordions
        EXPECTED: - Event details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, timeout=45)
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet, timeout=5),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

    def test_003_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'content-view',
        EXPECTED: 'screen_name' : '<< PAGE URL >>' })
        """
        actual_response = self.get_data_layer_specific_object(object_key='event', object_value='content-view')
        url = self.device.get_current_url()
        path = url.replace('https://%s' % tests.HOSTNAME, '')
        expected_response = {'event': 'content-view',
                             'screen_name': path}
        self.compare_json_response(actual_response, expected_response)

    def test_004_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: Football Landing page is opened
        DESCRIPTION: Go to the Event details page with the #YourCall (Leagues with available YourCall are marked with YourCall icon on accordion)
        EXPECTED: Build Your Bet tab is opened
        """
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=vec.yourcall.DASHBOARD_TITLE)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, vec.yourcall.DASHBOARD_TITLE,
                         msg='"All Markets" is not active tab after click, active tab is "%s"' % current_tab)

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'content-view',
        EXPECTED: 'screen_name' : '<< PAGE URL >>' })
        """
        self.test_003_type_in_browser_console_datalayer_and_tap_enter()

    def test_006_expand_add_deselect_remove_collapse_selections(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        """
        for market_name in self.market_names:
            market = getattr(self.expected_market_sections, market_name)
            if market == self.expected_market_sections.match_betting:
                self.expand_collapse_market(market_name=market, collapse=True)

            # track expand market group
            self.expand_collapse_market(market_name=market)
            self.verify_tracking_of_expanding_collapsing_market_accordion(accordion_action='expand market accordion')

            # track adding selection
            self.add_byb_selection_to_dashboard(market_name=market, count=1)
            self.verify_tracking_of_added_selections(market_name='match bet')

            # deselect selection
            self.add_byb_selection_to_dashboard(market_name=market, count=1, expected_result=False)
            self.verify_tracking_of_deselecting_selection(place_of_action='dashboard')

            # track removing
            self.add_byb_selection_to_dashboard(market_name=market, count=1)
            self.site.sport_event_details.tab_content.wait_for_dashboard_panel()
            self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.open_close_toggle_button.scroll_to()
            self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.open_close_toggle_button.click()
            self.remove_all_selections_from_dashboard()
            self.verify_tracking_of_removing_selection(market_name=market, place_of_action='dashboard')

            # track collapsing
            self.expand_collapse_market(market_name=market, collapse=True)
            self.verify_tracking_of_expanding_collapsing_market_accordion(accordion_action='collapse market accordion')
