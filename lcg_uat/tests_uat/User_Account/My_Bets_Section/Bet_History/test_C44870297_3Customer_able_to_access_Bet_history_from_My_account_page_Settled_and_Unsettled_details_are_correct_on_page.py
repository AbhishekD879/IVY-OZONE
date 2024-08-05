import pytest
import tests
from datetime import timedelta, date
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from random import choice, choices


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.slow
@pytest.mark.prod
@pytest.mark.p1
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870297_3Customer_able_to_access_Bet_history_from_My_account_page_Settled_and_Unsettled_details_are_correct_on_page(BaseBetSlipTest):
    """
    TR_ID: C44870297
    NAME: "3.Customer able to access Bet history from My account page Settled and Unsettled details are correct on page"
    """
    keep_browser_open = True
    selection_ids = []
    coral_my_bets_tabs = [vec.bet_history.CASH_OUT_TAB_NAME, vec.bet_history.OPEN_BETS_TAB_NAME,
                          vec.bet_history.SETTLED_BETS_TAB_NAME, vec.bet_history.IN_SHOP_BETS_TAB_NAME]
    ladbrokes_my_bets_tabs = [vec.bet_history.CASH_OUT_TAB_NAME, vec.bet_history.OPEN_BETS_TAB_NAME, vec.bet_history.SETTLED_BETS_TAB_NAME,
                              vec.bet_history.IN_SHOP_BETS_TAB_NAME]
    top_four_bets = 0

    def test_000_preconditions(self, expected_betslip_counter_value=0):
        """
        PRECONDITIONS: User should be logged in.
        PRECONDITIONS: Uses must have placed bets (single, double, each way and accumulator)
        """
        self.site.login(username=tests.settings.betplacement_user)
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         all_available_events=True, in_play_event=False)
            event = choice(events)
            market = next((market for market in event['event']['children']), None)
            outcomes_resp = market['market']['children']
            self.all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                                      for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
            selection = list(self.all_selection_ids.values())[0]
        else:
            event = self.ob_config.add_UK_racing_event()
            self._logger.info(f'*** Created Horse racing event "{event}"')
            selection = list(event.selection_ids.values())[0]

        self.open_betslip_with_selections(selection_ids=selection)
        self.place_and_validate_single_bet()
        self.site.bet_receipt.close_button.click()
        self.site.wait_content_state(state_name='HomePage')

        self.__class__.expected_betslip_counter_value = expected_betslip_counter_value
        self.open_betslip_with_selections(selection_ids=list(self.all_selection_ids.values())[1] if tests.settings.backend_env == 'prod' else list(event.selection_ids.values())[1])
        self.place_single_bet(each_way=True)
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state(state_name='HomePage')

        if tests.settings.backend_env == 'prod':
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
                self.selection_ids.append(selection_id)
        else:
            for i in range(4):
                event = self.ob_config.add_UK_racing_event()
                self._logger.info(f'*** Created Horse racing event "{event}"')
                selection_id = list(event.selection_ids.values())[0]
                self.selection_ids.append(selection_id)

        self.__class__.expected_betslip_counter_value = expected_betslip_counter_value
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=2)
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_001_user_shall_launch_test_appsite(self):
        """
        DESCRIPTION: User shall Launch test App/Site
        EXPECTED: User successfully Launches test App/Site
        """
        # Covered in Preconditions

    def test_002_user_shall_login_with__valid_credentials(self):
        """
        DESCRIPTION: User shall Login with  valid credentials
        EXPECTED: User successfully logs in with valid credentials
        """
        # Covered in Preconditions

    def test_003_verify_bet_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: Verify Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: Cashout/Open bets/Settled bets/Shop bets
        EXPECTED: All bet tabs must be displayed with the right details
        """
        self.navigate_to_page(name='bet-history')
        expected_my_bets_tabs = self.ladbrokes_my_bets_tabs if self.brand == 'ladbrokes' else self.coral_my_bets_tabs
        self.__class__.bet_tabs = self.site.bet_history.tabs_menu.items_as_ordered_dict
        actual_my_bet_tabs = list(self.bet_tabs)
        for tab in actual_my_bet_tabs:
            self.assertIn(tab, expected_my_bets_tabs,
                          msg=f'Actual tab: "{tab}" is not present in the list of tabs: "{expected_my_bets_tabs}"')

    def test_004_verify_bet_history_via_my_account_overlay___for_all_types_of_bets___single_multiple_ew_cashed_out_bets_hr_etc(self):
        """
        DESCRIPTION: Verify Bet History via My Account overlay - for all types of bets - single, multiple, E/W, cashed out bets, HR etc
        EXPECTED: User must be able to open Bet History via My Account
        EXPECTED: All bets must be displayed with the right details
        EXPECTED: for all types of bets
        EXPECTED: - single, multiple, E/W, cashed out bets, HR etc
        """
        bet = None
        bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        if (len(bets)) == 0:
            current_tab_name = self.site.bet_history.tab_content.grouping_buttons.current
            self._logger.info(f'There are no bets displayed on "{current_tab_name}" of "{vec.bet_history.SETTLED_BETS_TAB_NAME}"')
        else:
            bet_headers = self.site.bet_history.bet_types
            for bet_type in bet_headers:
                if any(subheader in bet_type for subheader in vec.betslip.BETSLIP_BETTYPES):
                    _, bet = self.site.bet_history.tab_content.accordions_list.get_bet(bet_type=bet_type)
                self.assertEqual(bet.bet_type, bet_type,
                                 msg=f'Bet type: "{bet.bet_type}" is not as expected: "{bet_type}"')
                if self.top_four_bets < 4:
                    self.assertTrue(bet.date, msg=f'Bet date is not shown for bet type "{bet_type}"')
                    odds_sign = bet.odds_sign.strip('"')
                    bet_odds = f'{odds_sign}{bet.odds_value}'
                    self.assertTrue(bet_odds, msg=f'odds are not present for bet type "{bet_type}" ')
                    self.assertTrue(bet.stake.value, msg=f'stake is not present for bet type "{bet_type}"')
                    self.assertTrue(bet.bet_receipt_info.bet_id, msg=f'bet id is not present for bet type "{bet_type}"')
                    status = bet.bet_status
                    self.assertTrue(status in vec.betslip.BETSLIP_BETSTATUS, msg=f'bets not available for bet type "{bet_type}"')

    def test_005_verify_bet_history_via_my_account_overlay___for_all_types_of_bets___unsettled(self):
        """
        DESCRIPTION: Verify Bet History via My Account overlay - for all types of bets - unsettled
        EXPECTED: All bets must be displayed with the right details
        """
        bet = None
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        if (len(bets)) == 0:
            current_tab_name = self.site.open_bets.tab_content.grouping_buttons.current
            self._logger.info(f'There are no bets displayed on "{current_tab_name}" of "{vec.bet_history.SETTLED_BETS_TAB_NAME}"')
        else:
            bet_headers = self.site.open_bets.bet_types
            for bet_type in bet_headers:
                if any(subheader in bet_type for subheader in vec.betslip.BETSLIP_BETTYPES):
                    _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=bet_type)
                self.assertEqual(bet.bet_type, bet_type,
                                 msg=f'Bet type: "{bet.bet_type}" is not as expected: "{bet_type}"')
                odds_sign = bet.odds_sign.strip('"')
                bet_odds = f'{odds_sign}{bet.odds_value}'
                self.assertTrue(bet_odds, msg=f'odds are not present for bet type "{bet_type}" ')
                self.assertTrue(bet.stake.value, msg=f'stake is not present for bet type "{bet_type}"')

    def test_006_verify_functionality_of_date_picker_today_last_7_days_and_last_30_days_from_bet_history_via_my_account_overlay(self):
        """
        DESCRIPTION: Verify functionality of Date Picker Today, Last 7 days and Last 30 days from Bet History via My Account overlay
        EXPECTED: Date Picker Today, Last 7 days and Last 30 days must be functional and working as per design implementation
        """
        self.site.open_my_bets_settled_bets()
        for i in [0, 7, 30]:
            new_date = date.today() - timedelta(days=i)
            past_date = new_date.__format__('%d/%m/%Y')
            self.site.bet_history.tab_content.accordions_list.date_picker.date_from.date_picker_value = past_date
            self.assertEqual(self.site.bet_history.tab_content.accordions_list.date_picker.date_from.text, past_date,
                             msg='Date range is not selected')
            self.test_004_verify_bet_history_via_my_account_overlay___for_all_types_of_bets___single_multiple_ew_cashed_out_bets_hr_etc()
