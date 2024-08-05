import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod #Cant create event and trigger overask on prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.overask
@pytest.mark.other
@pytest.mark.betslip
@vtest
class Test_C44870280__Treble_Horse_Racing_Bet_Countered_by_Price(BaseBetSlipTest):
    """
    TR_ID: C44870280
    NAME: - Treble Horse Racing Bet Countered by Price
    """
    keep_browser_open = True
    max_bet = 1
    max_mult_bet = 0.3
    suggested_max_bet = 0.24
    prices = [{0: '1/12'}, {0: '1/13'}, {0: '1/14'}]
    selection_ids = []
    selection_names = []
    new_price_1 = '1/7'
    new_price_2 = '3/17'
    new_price_3 = '13/100'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events for HR
        """
        for i in range(0, 3):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices[i], max_bet=self.max_bet,
                                                              max_mult_bet=self.max_mult_bet)
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_names.append(list(selection_ids.keys())[0])
            self.selection_ids.append(list(selection_ids.values())[0])
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_place_a_hr_treble_with_a_stake_that_will_take_it_to_overask(self):
        """
        DESCRIPTION: Place a HR treble with a stake that will take it to Overask
        EXPECTED: You should have placed the bet and it should have gone to Overask
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_mult_bet + 0.1
        self.place_multiple_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_traders_ti_counter_by_price_ie_reduce_the_price_you_can_reduce_the_prices_of_all_or_some_of_the_selections_in_the_bet(self):
        """
        DESCRIPTION: In Trader's TI, counter by price i.e. reduce the price. You can reduce the prices of all or some of the selections in the bet.
        EXPECTED: You should have given a counter offer by reducing the prices of all or some of the selections
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.\
            offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                  betslip_id=betslip_id, max_bet=self.bet_amount,
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

    def test_003_in_the_counter_offer_verify_that_only_the_prices_that_you_changed_in_ti_the_are_highlighted_in_yellow_and_verify_that_the_new_potential_returns_are_correct(self):
        """
        DESCRIPTION: In the counter offer, verify that only the prices that you changed in TI the are highlighted in yellow and verify that the new potential returns are correct.
        EXPECTED: You should see changed prices in yellow and you should see the correct potential returns.
        """
        self.sections = self.get_betslip_sections(multiples=True).Multiples
        stakes = self.sections.overask_trader_offer.items_as_ordered_dict
        for stake_name, stake in stakes.items():
                self.assertEqual(stake.stake_odds.value_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                                 msg=f'Modified price for "{stake_name}" is '
                                     f'not highlighted in "{vec.colors.OVERASK_MODIFIED_PRICE_COLOR}"')
        expected_return = self.get_betslip_content().total_estimate_returns
        self.prices[0][0], self.prices[1][0], self.prices[2][0] = self.new_price_1, self.new_price_2, self.new_price_3
        self.__class__.combined_odd = self.calculate_combined_odd(prices_list=self.prices)
        self.verify_estimated_returns(est_returns=expected_return, odds=self.combined_odd, bet_amount=self.bet_amount)

    def test_004_place_the_bet_and_in_the_bet_receipt_verify_that_you_see_the_correct_stake_and_returns(self):
        """
        DESCRIPTION: Place the bet and in the bet receipt, verify that you see the correct stake and returns
        EXPECTED: You should have placed the bet and in the bet receipt, you should see the correct stake and returns.
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        actual_est_returns = self.site.bet_receipt.footer.total_estimate_returns
        self.verify_estimated_returns(est_returns=actual_est_returns, odds=self.combined_odd, bet_amount=self.bet_amount)
        self.site.bet_receipt.close_button.click()

    def test_005_verify_that_the_bet_is_showing_in_my_bets_open_bets_and_that_it_shows_the_correct_stake_and_potential_returns(self):
        """
        DESCRIPTION: Verify that the bet is showing in My Bets->Open Bets and that it shows the correct stake and potential returns.
        EXPECTED: The bet should show in My Bets->Open Bets and that it shows the correct stake and returns.
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
                          msg=f'outcome:"{outcome}" is not in'
                              f'Expected outcome:"{self.selection_names}"')
        actual_stake = bet.stake.stake_value
        self.assertIn(str(self.bet_amount), actual_stake,
                      msg=f'Actual stake: "{actual_stake}" is not same as '
                          f'Expected stake:"{str(self.bet_amount)}"')
        self.verify_estimated_returns(est_returns=actual_est_returns, odds=self.combined_odd, bet_amount=self.bet_amount)
