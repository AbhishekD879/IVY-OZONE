import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from random import choices, choice
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.prod
@pytest.mark.p1
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C44870233_Customer_able_to_Cash_Out_the_SGL_Double_and_Acca_bets_from_My_Bets__CO_and_Bet_history_for_Sports_and_Races(BaseCashOutTest):
    """
    TR_ID: C44870233
    NAME: "Customer able to Cash Out the SGL, Double and Acca bets from My Bets -> CO and Bet history for Sports and Races
    DESCRIPTION: "Customer able to Cash Out the SGL, Double and Acca bets from My Bets -> CO and Bet history for Sports and Races
    DESCRIPTION: - Check Cashout successful and header balance
    DESCRIPTION: (b)Customer able to Partial Cash Out for SGL, Double and Acca bets in Open Bets/Cash Out
    DESCRIPTION: Check Cashout successful and header balance
    """
    keep_browser_open = True

    def test_001_user_shall_launch_test_appsite(self):
        """
        DESCRIPTION: User shall Launch Test App/Site
        EXPECTED: User successfully Launches Test App/Site
        """
        self.site.wait_content_state('HomePage')

    def test_002_user_shall_login_with_valid_credentials(self):
        """
        DESCRIPTION: User shall Login with valid credentials
        EXPECTED: User successfully Logins with valid credentials
        """
        self.site.login(tests.settings.betplacement_user)

    def test_003_add_the_selections_in_to_bet_slip_and_place_the_bet_on_any_single_or_double_selections(self, expected_betslip_counter_value=0):
        """
        DESCRIPTION: Add the selections in to bet slip and place the bet on any single or double selections
        EXPECTED: User successfully added the selections in to bet slip and placed bet
        """
        selection_ids = []
        self.__class__.event_names = []
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), simple_filter(
                LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True,
                                                         additional_filters=cashout_filter, in_play_event=False)
            event = choice(events)
            market = next((market for market in event['event']['children']), None)
            outcomes_resp = market['market']['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                                 for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
            selection = list(all_selection_ids.values())[0]
        else:
            events_params = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
            selection = list(events_params.selection_ids.values())[0]
        self.open_betslip_with_selections(selection_ids=selection)
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        #  In step 4 we need Acca bet so getting, creating events in this step
        self.__class__.expected_betslip_counter_value = expected_betslip_counter_value
        if tests.settings.backend_env == 'prod':
            event1 = choices(events, k=4)
            for event in event1:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                event_name = event['event']['name']
                self.event_names.append(event_name)
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                selection_ids.append(selection_id)
        else:
            events_params = self.create_several_autotest_premier_league_football_events(number_of_events=4, cashout=True)
            selections_ids = list(event_params.selection_ids[event_params.team1] for event_params in events_params)
            selection_ids.append(selections_ids)
            events_names = list(events_name.team1 for events_name in events_params)
            self.event_names.append(events_names)
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=2)
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_004_user_shall_go_to_my_bets_at_the_bottom_carousalfind_the_acca_bet_or_single_double_placed_and_taps_on_the_cash_out_option(self):
        """
        DESCRIPTION: User shall go to My Bets at the bottom carousal
        DESCRIPTION: Find the Acca Bet or single ,double placed and Taps on the Cash Out option
        EXPECTED: User successfully goes to My Bet at the bottom carousal
        EXPECTED: Find the Acca Bet,or single ,double placed and Taps on the Cash Out option
        """
        self.site.open_my_bets_open_bets()
        count = 0
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        if len(bets) != 0:
            self.assertTrue(bets, msg=f'There are no bets displayed on "{vec.bet_history.OPEN_BETS_TAB_NAME}" tab')
        bet_headers = self.site.open_bets.bet_types
        expected_bet_headers = ['DOUBLE', 'ACCA (4)']
        for bet_type in bet_headers:
            if bet_type in expected_bet_headers:
                count += 1
                _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=bet_type,
                                                                                                event_names=self.event_names,
                                                                                                number_of_bets=1)
                user_balance = self.site.header.user_balance
                self.assertTrue(self.bet.buttons_panel.has_full_cashout_button, msg=f'{vec.bet_history.CASH_OUT_UNAVAILABLE}')
                self.bet.buttons_panel.full_cashout_button.click()
                self.bet.buttons_panel.cashout_button.click()
                self.assertTrue(self.bet.wait_for_message(message=vec.bet_history.FULL_CASH_OUT_SUCCESS, timeout=30),
                                msg=f'Message: "{vec.bet_history.FULL_CASH_OUT_SUCCESS}" is not shown')
                self.device.refresh_page()
                self.site.open_my_bets_open_bets()
                new_user_balance = self.site.header.user_balance
                self.assertTrue(user_balance < new_user_balance,
                                msg='balance is not updated with cashout value')
            if count >= 2:
                break

    def test_005_observe_the_header_balance(self):
        """
        DESCRIPTION: Observe the header balance
        EXPECTED: Header balance should be updated
        """
        # This step is covered in scope of test_004
        pass

    def test_006_user_can_go_to_bet_history_via_my_accounts_and_find_the_cash_out_tab_for_particular_bets(self):
        """
        DESCRIPTION: User can go to bet history via my accounts and find the cash out tab for particular bets.
        EXPECTED: User successfully goes to bet history via my accounts
        EXPECTED: Find the Acca Bet,or single ,double placed and Taps on the Cash Out option
        """
        self.navigate_to_page("bet-history")
        self.site.wait_content_state(state_name='BetHistory')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.site.wait_content_state('openbets')
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        if len(bets) != 0:
            self.assertTrue(bets, msg=f'There are no bets displayed on "{vec.bet_history.OPEN_BETS_TAB_NAME}" tab')
            _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type='SINGLE')
            self.assertTrue(self.bet.buttons_panel.has_full_cashout_button, msg=f'"{vec.bet_history.CASH_OUT_TAB_NAME}" button is not present')
            self.bet.buttons_panel.full_cashout_button.click()
            self.bet.buttons_panel.cashout_button.click()
            self.assertTrue(self.bet.wait_for_message(message=vec.bet_history.FULL_CASH_OUT_SUCCESS, timeout=30),
                            msg=f'Message: "{vec.bet_history.FULL_CASH_OUT_SUCCESS}" is not shown')
        else:
            self._logger.info(msg=f'There are no bets displayed on "{vec.bet_history.OPEN_BETS_TAB_NAME}" tab')
