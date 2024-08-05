import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.open_bets
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870273__Single_Horse_Racing_Bet_Countered_by_Price(BaseBetSlipTest):
    """
    TR_ID: C44870273
    NAME: - Single Horse Racing Bet Countered by Price
    """
    keep_browser_open = True
    max_bet = 0.2
    max_mult_bet = 0.3
    prices = {0: '1/20'}
    new_price = '1/10'

    def test_000_preconditions(self):
        """
        DESCRIPTION:Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices, max_bet=self.max_bet,
                                                          max_mult_bet=self.max_mult_bet)
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_place_a_single_overask_bet_on_a_horse(self):
        """
        DESCRIPTION: Place a single overask bet on a horse
        EXPECTED: You should have placed an overask bet
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_mult_bet + 0.1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_traders_ti_give_a_counter_offer_by_price(self):
        """
        DESCRIPTION: In trader's TI, give a counter offer by price
        EXPECTED: You should see a counter offer on the front end
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                                 betslip_id=betslip_id,
                                                 price_1=self.new_price, max_bet=self.bet_amount)
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

    def test_003_check_that_the_price_is_highlighted_in_yellow_and_that_the_potential_returns_are_correct(self):
        """
        DESCRIPTION: Check that the price is highlighted in yellow and that the potential returns are correct
        EXPECTED: The price should be highlighted and the potential returns should be correct
        """
        sections = self.get_betslip_sections().Singles
        odd_value = sections.overask_trader_offer.stake_content.odd_value.value
        self.__class__.odd_value = odd_value.strip(' x')
        self.assertEqual(self.odd_value, self.new_price,
                         msg=f'Actual price :{self.odd_value} is not same as'
                             f'Expected price :{self.new_price}')
        self.assertEqual(sections.overask_trader_offer.stake_content.odd_value.value_color,
                         vec.colors.OVERASK_MODIFIED_PRICE_COLOR, msg=f'Modified price for stake is not highlighted in yellow')
        self.__class__.expected_return = self.get_betslip_content().total_estimate_returns
        self.verify_estimated_returns(est_returns=self.expected_return, bet_amount=self.bet_amount, odds=self.new_price)

    def test_004_click_on_place_bet_and_check_the_bet_receipt_for_the_correct_price_and_potential_returns(self):
        """
        DESCRIPTION: Click on Place Bet and check the Bet Receipt for the correct price and potential returns
        EXPECTED: Your bet should have been placed and the correct price and potential returns should be seen
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        singles = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict['Single']
        odd = singles.items_as_ordered_dict
        values = list(odd.values())[0]
        actual_odd = values.odds
        self.assertEqual(actual_odd, self.new_price,
                         msg=f'Actual stake: "{actual_odd}" is not same as '
                             f'Expected stake:"{self.new_price}"')
        actual_est_returns = self.site.bet_receipt.footer.total_estimate_returns
        self.assertEqual(actual_est_returns, self.expected_return,
                         msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                             f'Expected Returns:"{self.expected_return}"')
        self.site.bet_receipt.close_button.click()

    def test_005_check_the_bet_in_my_bets_open_bets_for_the_correct_price_and_potential_returns(self):
        """
        DESCRIPTION: Check the bet in My Bets->Open Bets for the correct price and potential returns.
        EXPECTED: You should see the bet with the correct price and potential returns.
        """
        self.site.open_my_bets_open_bets()
        open_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(open_bets,
                        msg='No bets found in open bet')
        bet = list(open_bets.values())[0]
        actual_odd = bet.odds_value
        actual_est_returns = bet.est_returns.stake_value
        self.assertEqual(actual_odd, self.new_price,
                         msg=f'Actual stake: "{actual_odd}" is not same as '
                             f'Expected stake:"{self.new_price}"')
        self.assertEqual(actual_est_returns, self.expected_return,
                         msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                             f'Expected Returns:"{self.expected_return}"')
