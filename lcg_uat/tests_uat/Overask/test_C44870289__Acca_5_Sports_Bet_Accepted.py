import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.open_bets
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.uat
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870289__Acca_5_Sports_Bet_Accepted(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C44870289
    NAME: - Acca 5 Sports Bet Accepted
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 0.25
    max_mult_bet = 0.35
    prices = [{'odds_home': '1/5', 'odds_draw': '1/4', 'odds_away': '1/6'},
              {'odds_home': '1/10', 'odds_draw': '1/4', 'odds_away': '1/6'},
              {'odds_home': '1/15', 'odds_draw': '1/4', 'odds_away': '1/6'},
              {'odds_home': '1/20', 'odds_draw': '1/4', 'odds_away': '1/6'},
              {'odds_home': '1/25', 'odds_draw': '1/4', 'odds_away': '1/6'}]
    selection_ids = []
    selection_names = []

    def verifying_placed_bet_in_open_bets(self):
        open_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(open_bets, msg='No bets found in open bet')
        bet = list(open_bets.values())[0]
        betlegs = bet.items_as_ordered_dict
        for bet_leg in list(betlegs.values()):
            outcome = bet_leg.outcome_name
            self.assertIn(outcome, self.selection_names,
                          msg=f'Actual outcome:"{outcome}" is not same as'
                              f'Expected outcome: "{self.selection_names}"')
        actual_stake = bet.stake.stake_value
        actual_est_returns = bet.est_returns.stake_value
        self.assertIn(str(self.bet_amount), actual_stake,
                      msg=f'Actual stake: "{actual_stake}" is not same as '
                          f'Expected stake:"{str(self.bet_amount)}"')
        combined_odd = self.calculate_combined_odd(prices_list=self.prices)
        self.verify_estimated_returns(est_returns=actual_est_returns, bet_amount=self.bet_amount, odds=combined_odd)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        if self.brand == 'ladbrokes':
            self.gvc_wallet_user_client.add_payment_card_and_deposit(amount=20, card_number=tests.settings.visa_card,
                                                                     card_type='visa',
                                                                     expiry_month='09',
                                                                     expiry_year='2029',
                                                                     cvv=tests.settings.visa_card_cvv)
        else:
            self.gvc_wallet_user_client.add_payment_card_and_deposit(amount=20, card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month='09',
                                                                     expiry_year='2029',
                                                                     cvv=tests.settings.master_card_cvv)
        for i in range(5):
            event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices[i], max_bet=self.max_bet, max_mult_bet=self.max_mult_bet)
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.selection_names.append(list(selection_ids.keys())[0])
        self.site.login(self.username)

    def test_001_add_five_selections_from_any_sport_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add five selections from any sport to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_bet + 5
        self.place_multiple_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_accept_the_bet_in_ob_ti_tool(self):
        """
        DESCRIPTION: Accept the bet in OB TI Tool
        EXPECTED: Bet is placed and the customer is taken to the bet receipt
        EXPECTED: My Bets and Account History should show the bet.
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.accept_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        self.verifying_placed_bet_in_open_bets()
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        if self.brand == 'ladbrokes':
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[6])
        else:
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[2])
        self.device.driver.implicitly_wait(3)
        self.site.right_menu.click_item(vec.bma.HISTORY_MENU_ITEMS[0])
        self.site.close_all_dialogs()
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.site.wait_content_state('OpenBets')
        self.verifying_placed_bet_in_open_bets()
