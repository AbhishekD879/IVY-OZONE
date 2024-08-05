import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.uat
# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.medium
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.open_bets
@pytest.mark.other
@vtest
class Test_C44870279__Acca_4_Horse_Racing_Bet_Countered_by_Stake(BaseBetSlipTest):
    """
    TR_ID: C44870279
    NAME: - Acca 4 Horse Racing Bet Countered by Stake
    """
    keep_browser_open = True
    max_bet = 1
    max_mult_bet = 1
    suggested_max_bet = 0.15
    prices = [{0: '1/12'}, {0: '1/13'}, {0: '1/14'}, {0: '1/15'}]
    selection_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create HR event's with required conditions
        EXPECTED: HR events are created
        """
        self.__class__.cms_overask_trader_message = self.get_overask_trader_offer()
        self.__class__.cms_overask_expires_message = self.get_overask_expires_message()
        for i in range(0, 4):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices[i], max_bet=self.max_bet,
                                                              max_mult_bet=self.max_mult_bet)
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_place_a_4_fold_hr_acca_with_a_stake_that_will_take_it_to_overask(self):
        """
        DESCRIPTION: Place a 4 fold HR ACCA with a stake that will take it to Overask
        EXPECTED: You should have placed the bet and it should have gone to Overask
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_mult_bet + 0.1
        self.place_multiple_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_traders_ti_counter_by_stake_ie_reduce_the_stake(self):
        """
        DESCRIPTION: In Trader's TI, counter by stake i.e. reduce the stake
        EXPECTED: You should have given a counter offer by reducing the stake
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet)

    def test_003_verify_that_you_see_the_counter_offer_at_the_front_end_that_the_new_stake_is_highlighted_in_yellow_and_that_the_new_potential_returns_are_correct(self):
        """
        DESCRIPTION: Verify that you see the counter offer at the front end, that the new stake is highlighted in yellow and that the new potential returns are correct.
        EXPECTED: In the counter offer, only the new stake should be highlighted in yellow and the new potential returns should be correct.
        """
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask panel is not closed')
        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        self.assertEqual(overask_trader_message, self.cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{self.cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        self.assertIn(self.cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{self.cms_overask_expires_message}" from CMS')

        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertEqual(sections.overask_trader_offer.stake_content.stake_value.value_color,
                         vec.colors.OVERASK_MODIFIED_PRICE_COLOR, msg=f'Modified price for stake is not '
                                                                      f'highlighted in {vec.colors.OVERASK_MODIFIED_PRICE_COLOR}')
        self.__class__.expected_return = self.get_betslip_content().total_estimate_returns
        combined_odd = self.calculate_combined_odd(self.prices)
        self.verify_estimated_returns(est_returns=self.expected_return, bet_amount=self.suggested_max_bet, odds=combined_odd)

    def test_004_place_the_bet_and_in_the_bet_receipt_verify_that_you_see_the_correct_stake_and_returns(self):
        """
        DESCRIPTION: Place the bet and in the bet receipt, verify that you see the correct stake and returns
        EXPECTED: You should have placed the bet and in the bet receipt, you should see the correct stake and returns.
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        actual_stake = self.site.bet_receipt.footer.total_stake
        actual_est_returns = self.site.bet_receipt.footer.total_estimate_returns
        self.assertEqual(actual_stake, str(self.suggested_max_bet),
                         msg=f'Actual stake: "{actual_stake}" is not same as '
                             f'Expected stake:"{str(self.suggested_max_bet)}"')
        self.assertEqual(actual_est_returns, self.expected_return,
                         msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                             f'Expected Returns:"{self.expected_return}"')
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
        actual_stake = bet.stake.stake_value
        actual_est_returns = bet.est_returns.stake_value
        self.assertEqual(actual_stake, str(self.suggested_max_bet),
                         msg=f'Actual stake: "{actual_stake}" is not same as '
                             f'Expected stake:"{str(self.suggested_max_bet)}"')
        self.assertEqual(actual_est_returns, self.expected_return,
                         msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                             f'Expected Returns:"{self.expected_return}"')
