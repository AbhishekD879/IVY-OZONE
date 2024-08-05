import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from random import choice, choices


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.prod
@pytest.mark.p1
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870360_Verify_user_can_see_the_OPEN_BETS_TAB_by_Default_in_My_Bets_tab(BaseBetSlipTest):
    """
    TR_ID: C44870360
    NAME: "Verify  user can see the OPEN BETS TAB by Default in My Bets tab
    DESCRIPTION: "Verify  user can see the OPEN BETS TAB by Default in My Bets tab
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: User must have some single, double, each way and accumulator bets placed.
    """
    keep_browser_open = True

    def test_000_preconditions(self, expected_betslip_counter_value=0):
        """
        PRECONDITIONS: Used should be logged in
        PRECONDITIONS: User must have some single, double, each way and accumulator bets placed
        """
        self.site.login(tests.settings.betplacement_user)
        selection_ids = []
        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                     all_available_events=True, in_play_event=False)
        event = choice(events)
        market = next((market for market in event['event']['children']), None)
        outcomes_resp = market['market']['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                             for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
        selection = list(all_selection_ids.values())[0]
        self.open_betslip_with_selections(selection_ids=selection)
        self.place_and_validate_single_bet()
        self.__class__.expected_betslip_counter_value = expected_betslip_counter_value
        self.open_betslip_with_selections(selection_ids=list(all_selection_ids.values())[1])
        self.place_single_bet(each_way=True)
        self.__class__.expected_betslip_counter_value = expected_betslip_counter_value
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                     all_available_events=True,
                                                     in_play_event=False)
        event1 = choices(events, k=4)
        for event in event1:
            match_result_market = next((market['market'] for market in event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = match_result_market['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(all_selection_ids.values())[0]
            selection_ids.append(selection_id)
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=2)
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_001_load_application(self):
        """
        DESCRIPTION: Load Application
        EXPECTED: Application page is loaded and user is landed on Home page with Highlights tab expanded by default.
        """
        self.site.wait_content_state('Homepage')

    def test_002_click_bet_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: Click on My Bets
        DESCRIPTION: or
        DESCRIPTION: Click on My Bets icon on Footer Menu.
        DESCRIPTION: or
        DESCRIPTION: Click on My Bets in Bet Slip (for Desktop)
        DESCRIPTION: or
        DESCRIPTION: Click Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: My Bets page should open.
        """
        self.site.open_my_bets_open_bets()

    def test_003__verify__user_can_see_the_open_bets_tab_by_default(self):
        """
        DESCRIPTION: -Verify  user can see the OPEN BETS TAB by Default
        DESCRIPTION: -Verify 'Open bets' page shows all placed open bets
        DESCRIPTION: Note: User see Settled bets tab by default when navigated from Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: - OPEN BETS is selected by default.
        EXPECTED: - User should be able to to all Open Bets (Bets which are not settled or cashed out)
        EXPECTED: Note: User see Settled bets tab by default when navigated from Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        """
        if self.device_type == 'mobile':
            active_tab = self.site.open_bets.tabs_menu.current
            self.assertEqual(active_tab, vec.bet_history.OPEN_BETS_TAB_NAME,
                             msg=f'Current tab is: "{active_tab}", not the same as expected: "{vec.bet_history.OPEN_BETS_TAB_NAME}"')
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        if len(bets) != 0:
            self.assertTrue(bets, msg=f'There are no bets displayed on "{vec.bet_history.OPEN_BETS_TAB_NAME}" tab')
        else:
            self._logger.info(msg=f'There are no bets displayed on "{vec.bet_history.OPEN_BETS_TAB_NAME}" tab')
#        self.site.navigate_to_right_menu_item(name='My Bets')
#         self.navigate_to_page(name='bet-history')
#         self.site.wait_content_state(state_name='BetHistory')
        # self.site.right_menu.click_item(item_name='Betting History')
        # self.site.wait_content_state(state_name='BetHistory')
        # self.site.open_my_bets_open_bets()
        # active_tab = self.site.open_bets.tabs_menu.current
        # self.assertEqual(active_tab, vec.bet_history.OPEN_BETS_TAB_NAME,
        #                  msg=f'"{vec.bet_history.OPEN_BETS_TAB_NAME}" is not active tab, active tab is: "{active_tab}"')

    def test_004__verify_see_retail_bets_on_the_shop_bet_tracker(self):
        """
        DESCRIPTION: -Verify See Retail bets on the Shop bet tracker navigates to shop bets
        DESCRIPTION: -Verify Cash Out Terms & Conditions
        DESCRIPTION: -Verify Edit My Acca Terms & Conditions
        DESCRIPTION: by scrolling down your bets and see if links are navigating to relevant pages.
        EXPECTED: - User should be able to see
        EXPECTED: See Retail Bets on Shop Bet Tracker > navigated to shop bets
        EXPECTED: Cash Out Terms & Conditions
        EXPECTED: Edit My Acca Terms & Conditions
        """
        # Script is not done for test_004 as it will be removed in future because there are no shop bets.
        pass

    def test_005__verify_header_it_should_display_bet_type_for_each_bet_single__double__acca_etc_(self):
        """
        DESCRIPTION: -Verify Header it should display bet type for each bet (Single / Double / ACCA etc )
        EXPECTED: -User should be able to see all these headers for bets, such as SINGLE, SINGLE (EACH WAY), DOUBLE, TREBLE, ACCA(no. of selections) etc
        """
        if self.device_type == 'mobile':
            self.site.open_bets.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        else:
            self.site.open_bets.grouping_buttons.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.__class__.bet_headers = self.site.open_bets.bet_types
        self.__class__.expected_bet_headers = ['SINGLE', 'DOUBLE', 'ACCA (4)']
        for headers in self.bet_headers:
            if headers in self.expected_bet_headers:
                self.assertTrue(any(self.expected_bet_headers for subheader in headers),
                                msg=f'"{headers}" is not expected bet header')

    def test_006__verify_sports_lotto_and_pools_tab_in_open_bets(self):
        """
        DESCRIPTION: -Verify 'Sports', 'Lotto' and 'Pools' tab in 'Open Bets'
        EXPECTED: - Customer should see all these three tabs
        EXPECTED: Sports   Lotto  Pools
        """
        tabs = self.site.open_bets.tab_content.grouping_buttons.items_as_ordered_dict
        for actual_tab in tabs:
            self.assertIn(actual_tab, vec.bet_history.SORTING_BUTTON_TYPES_SETTLED_BETS,
                          msg=f'Tab "{actual_tab}" is not found in "{vec.bet_history.SORTING_BUTTON_TYPES_SETTLED_BETS}"')

    def test_007_verify_my_bets_tabcash_out_if_configured_in_cmsopen_betssettled_betsshop_bets(self):
        """
        DESCRIPTION: Verify My Bets tab
        DESCRIPTION: Cash Out (if configured in CMS)
        DESCRIPTION: Open Bets
        DESCRIPTION: Settled Bets
        DESCRIPTION: Shop bets
        EXPECTED: User is able to see these tabs
        EXPECTED: Cash Out    Open Bets     Settled Bets   Shop bets
        """
        if self.device_type == 'mobile':
            tabs = self.site.open_bets.tabs_menu.items_names
        else:
            tabs = self.site.betslip.tabs_menu.items_names
        self.assertTrue(tabs, msg='Tabs are not found')
        for tab in tabs:
            self.assertIn(tab, vec.bet_history.MY_BETS_TAB_NAMES,
                          msg=f'Tab "{tab}" is not found in "{vec.bet_history.MY_BETS_TAB_NAMES}"')

    def test_008__verify_bets_shown_in_open_betscash_out_tab_should_have_this_informationstakepotential_returnsestimate_returns(
            self):
        """
        DESCRIPTION: -Verify bets shown in Open Bets/Cash Out Tab should have this information
        DESCRIPTION: Stake
        DESCRIPTION: Potential Returns/Estimate Returns.
        EXPECTED: Customer should be able to see Stake and Potential Returns for all bets placed.
        """
        count = 0
        if self.brand == 'bma':
            sports = vec.bma.SPORTS.upper()
        else:
            sports = vec.bma.SPORTS
        self.site.open_bets.tab_content.grouping_buttons.click_button(sports)
        for bet_type in self.bet_headers:
            if bet_type in self.expected_bet_headers:
                _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=bet_type)
                count += 1
                self.assertTrue(bet.stake.value, msg=f'stake is not present for bet "{bet_type}"')
                self.assertTrue(bet.est_returns.value, msg=f'est returns is not present for bet "{bet_type}"')
            if count >= 3:
                break
