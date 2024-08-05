import pytest
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from random import choice, sample
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from collections import OrderedDict


@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@pytest.mark.uat
@vtest
class Test_C44870363_Verify_Bets_Details_in_Open_Bet(BaseBetSlipTest):
    """
    TR_ID: C44870363
    NAME: Verify Bets Details in Open Bet.
    DESCRIPTION: This TC verifies bet details in Open Bet tab.
    DESCRIPTION: Verify user can see the OPEN BETS TAB by Default in My Bets tab
    PRECONDITIONS: User should be logged in.
    PRECONDITIONS: Uses must have placed bets (single, double, each way and accumulator)
    """
    keep_browser_open = True

    def test_000_preconditions(self, expected_betslip_counter_value=0):
        """
       PRECONDITIONS: User should be logged in.
       PRECONDITIONS: Uses must have placed bets (single, double, each way and accumulator)
       DESCRIPTION: Placing AAC(4), double, single, each way bet
       """
        selection_ids = OrderedDict()
        event_names = []
        self.__class__.all_bet_selection_details = {}
        self.__class__.all_bet_event_details = {}

        self.site.login()
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'),\
            simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                     additional_filters=cashout_filter, all_available_events=True,
                                                     in_play_event=False)
        multiple_events = sample(events, k=4)
        self.assertTrue(len(multiple_events) == 4, msg=f'Expected number of events: 4 '
                                                       f'actual number of events: {len(multiple_events)}')
        for event in multiple_events:
            self.__class__.market = next((market['market'] for market in event['event']['children'] if
                                          market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = self.market['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(all_selection_ids.items())[0]
            if selection_id[0] == 'Draw':
                selection_id = list(all_selection_ids.items())[1]
            selection_ids.update({selection_id})
            event_names.append(event['event']['name'])

        self.open_betslip_with_selections(selection_ids=selection_ids.values())
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.all_bet_selection_details['ACCA (4)'] = list(selection_ids.keys())
        self.all_bet_event_details['ACCA (4)'] = event_names

        self.__class__.expected_betslip_counter_value = expected_betslip_counter_value
        self.open_betslip_with_selections(selection_ids=list(selection_ids.values())[0:2])
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.all_bet_selection_details['DOUBLE'] = list(selection_ids.keys())[0:2]
        self.all_bet_event_details['DOUBLE'] = event_names[0:2]
        self.__class__.expected_betslip_counter_value = expected_betslip_counter_value
        self.open_betslip_with_selections(selection_ids=list(selection_ids.values())[0:1])
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        self.all_bet_selection_details['SINGLE'] = list(selection_ids.keys())[0:1]
        self.all_bet_event_details['SINGLE'] = event_names[0:1]
        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                     all_available_events=True, in_play_event=False)
        single_event = choice(events)
        self.__class__.HRmarket = next((market['market'] for market in single_event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Win or Each Way'), None)
        outcomes1 = self.HRmarket['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                             for i in outcomes1 if 'Unnamed' not in i['outcome']['name']}
        self.__class__.expected_betslip_counter_value = expected_betslip_counter_value
        self.open_betslip_with_selections(selection_ids=list(all_selection_ids.values())[0])
        self.place_single_bet(each_way=True)
        self.check_bet_receipt_is_displayed()
        self.all_bet_selection_details['SINGLE (EACH WAY)'] = list(all_selection_ids.keys())[0]
        self.all_bet_event_details['SINGLE (EACH WAY)'] = single_event['event']['name']
        self.site.close_betreceipt()

    def test_001_load_application__log_in(self):
        """
        DESCRIPTION: Load Application & Log in
        EXPECTED: Application page is loaded and user is landed on Home page with Highlights tab expanded by default.
        """
        if self.device_type == "mobile":
            self.site.wait_content_state("Homepage")
            tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            if self.brand == 'ladbrokes':
                featured_section = tabs.get(vec.racing.RACING_HIGHLIGHTS_TAB_NAME)
            else:
                featured_section = tabs.get(vec.racing.RACING_DEFAULT_TAB_NAME)
            self.assertTrue(featured_section.is_selected, msg=f'"{featured_section}" section not found')
        else:
            home_page_modules = self.site.home.desktop_modules.items_as_ordered_dict
            self.assertTrue(home_page_modules, msg='No module found on Home Page')
            featured_section = home_page_modules.get(vec.Inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME)
            self.assertTrue(featured_section, msg='"Featured" section not found')

    def test_002_click_on_my_betsorclick_on_cashout_icon_on_footer_menuorclick_on_my_bets_in_bet_slip_for_desktoporclick_bet_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: Click on My Bets
        DESCRIPTION: or
        DESCRIPTION: Click on Cashout icon on Footer Menu.
        DESCRIPTION: or
        DESCRIPTION: Click on My Bets in Bet Slip (for Desktop)
        DESCRIPTION: or
        DESCRIPTION: Click Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: My Bets page should open.
        """
        # This step is covered in test_003

    def test_003__verify_user_can_see_the_open_bets_tab_by_default_verify_open_bets_page_shows_all_placed_open_betsnote_user_see_cashout__tab_by_default_when_navigated_from_cashout_via_footer_menu_on_mobile_user_sees_settled_bets_tab_by_default_when_navigated_from_bet_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: -Verify user can see the OPEN BETS TAB by Default
        DESCRIPTION: -Verify 'Open bets' page shows all placed open bets
        DESCRIPTION: Note: User see Cashout  tab by default when navigated from Cashout via Footer menu on Mobile &
        DESCRIPTION: User sees Settled bets tab by default when navigated from Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: OPEN BETS is selected by default.
        EXPECTED: User should be able to to all Open Bets (Bets which are not settled or cashed out)
        """
        self.site.open_my_bets_open_bets()
        if self.device_type == 'mobile':
            active_tab = self.site.open_bets.tabs_menu.current
            self.assertEqual(active_tab, vec.bet_history.OPEN_BETS_TAB_NAME,
                             msg=f'Current tab is: "{active_tab}", not the same as expected: "{vec.bet_history.OPEN_BETS_TAB_NAME}"')
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg=f'There are no bets displayed on "{vec.bet_history.OPEN_BETS_TAB_NAME}" tab')
        self.navigate_to_page(name='bet-history')
        self.site.wait_content_state(state_name='BetHistory')

    def test_004_verify_open_bet_pending_bet_detailsverify_below_details_of_the_bet__date_and_time_of_the_event__selection_name__event_name__market_name__stake_and_estimated_returns__watch_live_icon_if_its_live__silks_for_horse_racing__signposting_if_available(self):
        """
        DESCRIPTION: Verify open bet pending bet details
        DESCRIPTION: Verify below details of the bet
        DESCRIPTION: - date and time of the event.
        DESCRIPTION: - Selection name
        DESCRIPTION: - Event name
        DESCRIPTION: - Market name
        DESCRIPTION: - Stake and Estimated returns
        DESCRIPTION: - Silks for horse racing
        DESCRIPTION: - Signposting if available
        EXPECTED: User is able to see these details
        EXPECTED: - date and time of the event
        EXPECTED: - Selection name
        EXPECTED: - Event name
        EXPECTED: - Market Name
        EXPECTED: - Stake and Estimated returns
        EXPECTED: - Silks for horse racing
        EXPECTED: - Signposting if available
        """
        self.site.open_my_bets_open_bets()
        bet_types = [vec.bet_history.SINGLE_EACH_WAY_BET_TYPE, vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
                     vec.bet_history._bet_types_ACC4.upper(), vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE]
        for bet_type in bet_types:
            bet_name, bet = self.site.open_bets.tab_content.accordions_list.\
                get_bet(bet_type=bet_type, event_names=self.all_bet_event_details[bet_type])
            self.assertEqual(bet.bet_type, bet_type, msg=f'Bet type: "{bet.bet_type}"'
                                                         f'is not as expected: "{bet_type}"')
            self.assertTrue(bet.date, msg=f'Date is not displayed expected for "{bet_name}"')

            for selection in bet.selection_elements:
                self.assertIn(selection.text, self.all_bet_selection_details[bet_type],
                              msg=f'Actual selection: {selection.text} expected selection: {self.all_bet_selection_details[bet_type]}')
            for event in bet.event_elements:
                self.assertIn(event.text, self.all_bet_event_details[bet_type],
                              msg=f'Actual event: {event.text} expected event: {self.all_bet_event_details[bet_type]}')
            for market in bet.market_elements:
                if bet.bet_type == vec.bet_history.SINGLE_EACH_WAY_BET_TYPE:
                    self.assertEquals(market.text.split(',')[0], self.HRmarket['templateMarketName'],
                                      msg=f'Actual market: {market.text} expected market: {self.HRmarket["templateMarketName"]}')
                else:
                    self.assertIn(market.text, ['Match Result', self.market['templateMarketName']],
                                  msg=f'Actual market: {market.text} expected market: "Match Result" or {self.market["templateMarketName"]}')
            self.assertTrue(bet.stake.is_displayed(), msg='"Stake" is not displayed')
            self.assertTrue(bet.est_returns.is_displayed(), msg='"Est.return" is not displayed')
            if bet_type == vec.bet_history.SINGLE_EACH_WAY_BET_TYPE:
                if bet.has_silk(expected_result=True, timeout=2):
                    self._logger.info(f'Silk is displayed for "{bet_name}" bet')
                else:
                    self._logger.info(f'Silk is not displayed for "{bet_name}" bet')
                if bet.has_promo_icon(expected_result=True, timeout=2):
                    self._logger.info(f'Signposting is available for "{bet_name}" bet')
                else:
                    self._logger.info(f'Signposting is not available for "{bet_name}" bet')

    def test_005_verify_header_it_should_display_bet_type_for_each_bet_single__double__acca_etc_(self):
        """
        DESCRIPTION: Verify Header it should display bet type for each bet (Single / Double / ACCA etc )
        EXPECTED: -User should be able to see all these headers for bets, such as SINGLE, SINGLE (EACH WAY), DOUBLE, TREBLE, ACCA(no. of selections) etc
        """
        # This step is covered in test_004

    def test_006_verify_sports_lotto_and_pools_tab_in_open_bets(self):
        """
        DESCRIPTION: Verify 'Sports', 'Lotto' and 'Pools' tab in 'Open Bets'
        EXPECTED: Customer should see all these three tabs Sports Lotto Pools
        """
        open_bet_tabs = self.site.open_bets.tab_content.grouping_buttons.items_as_ordered_dict
        self.assertTrue(open_bet_tabs, msg='Open Bet tabs are not displayed')
        for tab_name in open_bet_tabs:
            self.assertIn(tab_name, vec.bet_history.SORTING_BUTTON_TYPES_SETTLED_BETS,
                          msg=f'Tab "{tab_name}" is not found in "{vec.bet_history.SORTING_BUTTON_TYPES_SETTLED_BETS}"')

    def test_007_verify_settled_bets_are_moved_to_settled_tab(self):
        """
        DESCRIPTION: Verify Settled Bets are moved to Settled Tab
        EXPECTED: User is able to see bets in Settled Tab once bet is settled or Cashed out.
        """
        _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.__class__.event_name = bet.event_name
        self.assertTrue(bet.buttons_panel.has_full_cashout_button, msg='"FULL CASHOUT" button is not present')
        bet.buttons_panel.full_cashout_button.click()
        self.assertTrue(bet.buttons_panel.has_cashout_button(), msg='"Confirm cash out button" is not displayed')
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.wait_for_message(message=vec.bet_history.FULL_CASH_OUT_SUCCESS, timeout=30),
                        msg=f'Message: "{vec.bet_history.FULL_CASH_OUT_SUCCESS}" is not shown')
        self.site.open_my_bets_settled_bets()
        settled_bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        if len(settled_bets) is 0:
            actual_message = self.site.bet_history.tab_content.accordions_list.no_bets_message
            self.assertEqual(actual_message, vec.bet_history.NO_HISTORY_INFO,
                             msg=f'Actual "{actual_message}"is not the same as expected"{vec.bet_history.NO_HISTORY_INFO}"')
        else:
            _, bet = self.site.bet_history.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                                               event_names=self.event_name)
            self.assertTrue(bet.event_name == self.event_name,
                            msg=f'Cannot find event {self.event_name} in Settled Bets tab')

    def test_008_verify_bets_shown_in_open_betscash_out_tab_should_have_this_informationstakepotential_returnsestimate_returns(self):
        """
        DESCRIPTION: Verify bets shown in Open Bets/Cash Out Tab should have this information
        DESCRIPTION: Stake
        DESCRIPTION: Potential Returns/Estimate Returns.
        EXPECTED: Customer should be able to see Stake and Potential Returns for all bets placed.
        """
        self.site.open_my_bets_cashout()
        _, bet = self.site.cashout.tab_content.accordions_list.get_bet(event_names=self.event_name)
        self.assertTrue(bet.stake.is_displayed(), msg='"Stake" is not displayed')
        self.assertTrue(bet.est_returns.is_displayed(), msg='"Est.return" is not displayed')
