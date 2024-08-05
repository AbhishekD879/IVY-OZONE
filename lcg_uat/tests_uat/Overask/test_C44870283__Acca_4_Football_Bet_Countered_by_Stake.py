import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.open_bets
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C44870283__Acca_4_Football_Bet_Countered_by_Stake(BaseBetSlipTest):
    """
    TR_ID: C44870283
    NAME: - Acca 4 Football Bet Countered by Stake
    """
    keep_browser_open = True
    max_bet = 1.21
    max_mult_bet = 1.21
    suggested_max_bet = 0.94
    prices = [{'odds_home': '1/5', 'odds_draw': '1/4', 'odds_away': '1/6'},
              {'odds_home': '1/10', 'odds_draw': '1/4', 'odds_away': '1/6'},
              {'odds_home': '1/15', 'odds_draw': '1/4', 'odds_away': '1/6'},
              {'odds_home': '1/20', 'odds_draw': '1/4', 'odds_away': '1/6'}]
    selection_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        for i in range(4):
            event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices[i], max_bet=self.max_bet, max_mult_bet=self.max_mult_bet)
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_place_a_4_fold_oa_acca_bet(self):
        """
        DESCRIPTION: Place a 4-fold OA ACCA bet
        EXPECTED: The bet should have gone to the OA flow
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_mult_bet + 8
        self.place_multiple_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_traders_interface_change_the_stake_of_the_bet_and_click_on_submit(self):
        """
        DESCRIPTION: In Trader's Interface, change the stake of the bet and click on Submit
        EXPECTED: The counter offer should show the bet with the new stake and it should be highlighted in yellow
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask is not closed')
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

    def test_003_check_that_the_potential_returns_are_correct(self):
        """
        DESCRIPTION: Check that the Potential Returns are correct
        EXPECTED: The Potential Returns should be correct
        """
        sections = self.get_betslip_sections(multiples=True)
        multiples_section = sections.Multiples
        amount = multiples_section.overask_trader_offer.stake_content.stake_value.value
        self.__class__.amount = float(amount.strip('£'))
        self.assertEqual(self.amount, self.suggested_max_bet,
                         msg=f'The value of suggested stake "{self.suggested_max_bet}" is not present in '
                             f'the "Stake" field, the value is: "{self.amount}"')
        self.__class__.expected_return = self.get_betslip_content().total_estimate_returns
        combined_odd = self.calculate_combined_odd(self.prices)
        self.verify_estimated_returns(est_returns=self.expected_return, bet_amount=self.amount, odds=combined_odd)

    def test_004_place_the_bet(self):
        """
        DESCRIPTION: Place the bet
        EXPECTED: You should see the bet receipt and it should show the new stake and the correct potential returns
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        actual_stake = self.site.bet_receipt.footer.total_stake
        actual_est_returns = self.site.bet_receipt.footer.total_estimate_returns
        self.assertEqual(actual_stake, str(self.amount),
                         msg=f'Actual stake: "{actual_stake}" is not same as '
                             f'Expected stake:"{str(self.amount)}"')
        self.assertEqual(actual_est_returns, self.expected_return,
                         msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                             f'Expected Returns:"{self.expected_return}"')
        self.site.bet_receipt.close_button.click()

    def test_005_check_my_bets_open_bets_to_see_that_the_bet_has_the_correct_stake_and_potential_returns(self):
        """
        DESCRIPTION: Check My Bets->Open Bets to see that the bet has the correct stake and Potential Returns
        EXPECTED: The bet should show the correct new stake and Potential Returns
        """
        self.site.open_my_bets_open_bets()
        open_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(open_bets,
                        msg='No bets found in open bet')
        bet = list(open_bets.values())[0]
        actual_stake = bet.stake.stake_value
        actual_est_returns = bet.est_returns.stake_value
        self.assertEqual(actual_stake, str(self.amount),
                         msg=f'Actual stake: "{actual_stake}" is not same as '
                             f'Expected stake:"{str(self.amount)}"')
        self.assertEqual(actual_est_returns, self.expected_return,
                         msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                             f'Expected Returns:"{self.expected_return}"')
