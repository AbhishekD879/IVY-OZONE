import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.open_bets
@vtest
class Test_C44870281__Double_Horse_Racing_Bet_Countered_by_Price_to_SP(BaseBetSlipTest):
    """
    TR_ID: C44870281
    NAME: - Double Horse Racing Bet Countered by Price to SP
    """
    keep_browser_open = True
    max_bet = 0.2
    max_mult_bet = 0.3
    prices = [{0: '1/12'}, {0: '1/11'}]
    new_price = 'SP'
    selection_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION:Create an event
        EXPECTED: Event is created
        """
        for i in range(2):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices[i],
                                                              max_bet=self.max_bet, max_mult_bet=self.max_mult_bet)
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)
        self.site.wait_content_state('HomePage')

    def test_001_place_an_oa_hr_double_bet_using_lp_prices(self):
        """
        DESCRIPTION: Place an OA HR double bet using LP prices
        EXPECTED: The bet should have gone to the Over Ask flow
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_mult_bet + 0.1
        self.place_multiple_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=20)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_the_traders_interface_give_a_counter_offer_by_changing_the_prices_to_sp_and_click_submit(self):
        """
        DESCRIPTION: In the Trader's Interface, give a counter offer by changing the prices to SP and click Submit
        EXPECTED: On the Front End, you should see a counter offer with the LP prices crossed out and next to them should be the text SP and it should be highlighted in yellow
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.change_price_type(account_id=account_id, bet_id=bet_id,
                                             betslip_id=betslip_id, bet_amount=self.bet_amount,
                                             price_type='S', num_of_prices_to_change=2)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=25)
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
        sections = self.get_betslip_sections(multiples=True).Singles
        stakes = sections.overask_trader_offer.items_as_ordered_dict
        for stake_name, stake in stakes.items():
            odd_value = stake.stake_content.odd_value.value
            odd_value = odd_value.strip(' x')
            self.assertEqual(odd_value, self.new_price, msg=f'Actual price :"{odd_value}" is not same as'
                                                            f'Expected price :"{self.new_price}" for stake "{stake_name}"')
            self.assertEqual(stake.stake_content.odd_value.value_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                             msg=f'Modified price for stake "{stake_name}" is not highlighted in yellow')

    def test_003_check_that_the_potential_returns_are_showing_as_na(self):
        """
        DESCRIPTION: Check that the Potential Returns are showing as N/A
        EXPECTED: The Potential Returns should be shown as N/A
        """
        self.__class__.expected_return = self.get_betslip_content().total_estimate_returns
        self.verify_estimated_returns(est_returns=self.expected_return, bet_amount=self.bet_amount, odds=self.new_price)

    def test_004_place_the_bet(self):
        """
        DESCRIPTION: Place the bet
        EXPECTED: You should see the bet receipt and the prices should be SP and the Potential Returns should be N/A
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        multiples = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict['Double']
        values = list(multiples.items_as_ordered_dict.values())
        for singles in values:
            actual_odd = singles.item_odds
            self.assertIn(self.new_price, actual_odd, msg=f'Actual stake: "{actual_odd}" is not same as '
                                                          f'Expected stake:"{self.new_price}"')
        actual_est_returns = self.site.bet_receipt.footer.total_estimate_returns
        self.assertEqual(actual_est_returns, self.expected_return,
                         msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                             f'Expected Returns:"{self.expected_return}"')
