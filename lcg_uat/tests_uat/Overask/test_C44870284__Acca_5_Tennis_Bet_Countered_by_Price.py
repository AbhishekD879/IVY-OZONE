import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.open_bets
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.uat
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870284__Acca_5_Tennis_Bet_Countered_by_Price(BaseBetSlipTest):
    """
    TR_ID: C44870284
    NAME: - Acca 5 Tennis Bet Countered by Price
    """
    keep_browser_open = True
    max_mult_bet = 0.35
    max_bet = 0.25
    prices = [{'odds_home': '1/5', 'odds_away': '1/6'},
              {'odds_home': '1/10', 'odds_away': '1/6'},
              {'odds_home': '1/15', 'odds_away': '1/6'},
              {'odds_home': '1/20', 'odds_away': '1/6'},
              {'odds_home': '1/25', 'odds_away': '1/6'}]
    new_price_1 = '1/7'
    new_price_2 = '3/5'
    new_price_3 = '5/10'
    selection_names = []
    selection_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION:Create an event
        EXPECTED: Event is created
        """
        for i in range(0, 5):
            event_params = self.ob_config.\
                add_tennis_event_to_autotest_trophy(lp=self.prices[i], max_mult_bet=self.max_mult_bet, max_bet=self.max_bet)
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_names.append(list(selection_ids.keys())[0])
            self.selection_ids.append(list(selection_ids.values())[0])
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_place_an_oa_5_fold_tennis_acca(self):
        """
        DESCRIPTION: Place an OA 5-fold tennis ACCA
        EXPECTED: The bet should have gone through to TI
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_bet + 5
        self.place_multiple_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_ti_change_the_price_of_all_the_selections_or_just_some_of_them_and_click_submit(self):
        """
        DESCRIPTION: In TI, change the price of all the selections or just some of them and click Submit
        EXPECTED: On the Front End, you should see a counter offer with the prices which have been changed crossed out and the new prices highlighted in yellow.
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.\
            offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                  betslip_id=betslip_id, max_bet=self.max_bet,
                                  price_1=self.new_price_1, price_2=self.new_price_2,
                                  price_3=self.new_price_3)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask panel is not closed')
        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')

    def test_003_check_that_the_potential_returns_are_correct_on_the_counter_offer(self):
        """
        DESCRIPTION: Check that the Potential Returns are correct on the counter offer
        EXPECTED: The Potential Returns should be correct
        """
        expected_return = self.get_betslip_content().total_estimate_returns
        self.prices[0]['odds_home'], self.prices[1]['odds_home'], self.prices[2]['odds_home'] \
            = self.new_price_1, self.new_price_2, self.new_price_3

        self.__class__.combined_odd = self.calculate_combined_odd(prices_list=self.prices)
        self.verify_estimated_returns(est_returns=expected_return, odds=self.combined_odd, bet_amount=self.max_bet)

    def test_004_place_the_bet(self):
        """
        DESCRIPTION: Place the bet
        EXPECTED: You should see the bet receipt and it should have the correct Potential Returns
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        actual_est_returns = self.site.bet_receipt.footer.total_estimate_returns
        self.verify_estimated_returns(est_returns=actual_est_returns, odds=self.combined_odd, bet_amount=self.max_bet)
        self.site.bet_receipt.close_button.click()

    def test_005_check_that_the_bets_are_correctly_seen_in_________my_bets_open_bets(self):
        """
        DESCRIPTION: Check that the bets are correctly seen in         My Bets->Open Bets
        EXPECTED: The bets should correctly be seen in My Bets->Open Bets
        """
        self.site.open_my_bets_open_bets()
        open_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(open_bets,
                        msg='No bets found in open bet')
        bet = list(open_bets.values())[0]
        actual_est_returns = bet.est_returns.stake_value
        betlegs = bet.items_as_ordered_dict
        for betleg_name, bet_leg in list(betlegs.items()):
            outcome = bet_leg.outcome_name
            self.assertIn(outcome, self.selection_names,
                          msg=f'outcome:{outcome} is not in'
                              f'Expected outcome: {self.selection_names}')
        actual_stake = bet.stake.stake_value
        self.assertIn(str(self.max_bet), actual_stake,
                      msg=f'Actual stake: "{actual_stake}" is not same as '
                          f'Expected stake:"{str(self.bet_amount)}"')
        self.verify_estimated_returns(est_returns=actual_est_returns, odds=self.combined_odd, bet_amount=self.max_bet)
