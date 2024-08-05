import pytest
import tests
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.base_test import vtest


@pytest.mark.open_bets
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C44870274__Single_Horse_Racing_Bet_Countered_by_Price_to_SP(BaseBetSlipTest):
    """
    TR_ID: C44870274
    NAME: - Single Horse Racing Bet Countered by Price to SP
    """
    keep_browser_open = True
    max_bet = 0.2
    max_mult_bet = 0.3
    prices = {0: '1/20'}
    new_price = 'SP'

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

    def test_002_in_traders_ti_give_a_counter_offer_by_price_to_sp(self):
        """
        DESCRIPTION: In trader's TI, give a counter offer by price to SP
        EXPECTED: You should see a counter offer on the front end
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.change_price_type(account_id=account_id, bet_id=bet_id,
                                             betslip_id=betslip_id, bet_amount=self.bet_amount,
                                             price_type='S')
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

    def test_003_check_that_the_price_is_sp_and_it_is_highlighted_in_yellow_and_that_the_potential_returns_are_showing_as_na(self):
        """
        DESCRIPTION: Check that the price is SP and it is highlighted in yellow and that the potential returns are showing as N/A
        EXPECTED: The price should be SP and should be highlighted and the potential returns should be N/A
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

    def test_004_click_on_place_bet_and_check_the_bet_receipt_shows_the_price_as_sp_and_potential_returns_as_na(self):
        """
        DESCRIPTION: Click on Place Bet and check the Bet Receipt shows the price as SP and Potential returns as N/A
        EXPECTED: Your bet should have been placed and the price on the receipt should be SP and Potential returns should be N/A
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        singles = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict['Single']
        odd = list(singles.items_as_ordered_dict.values())[0]
        actual_odd = odd.odds
        self.assertEqual(actual_odd, self.new_price,
                         msg=f'Actual stake: "{actual_odd}" is not same as '
                             f'Expected stake:"{self.new_price}"')
        actual_est_returns = self.site.bet_receipt.footer.total_estimate_returns
        self.assertEqual(actual_est_returns, self.expected_return,
                         msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                             f'Expected Returns:"{self.expected_return}"')
        self.site.bet_receipt.close_button.click()

    def test_005_check_the_bet_in_my_bets_open_bets_for_the_correct_price_sp_and_potential_returns_as_na(self):
        """
        DESCRIPTION: Check the bet in My Bets->Open Bets for the correct price (SP) and potential returns as N/A
        EXPECTED: You should see the bet with a price of SP and potential returns of N/A.
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
