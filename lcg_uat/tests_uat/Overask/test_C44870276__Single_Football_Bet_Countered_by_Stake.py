import pytest
import tests
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.uat
@pytest.mark.open_bets
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C44870276__Single_Football_Bet_Countered_by_Stake(BaseBetSlipTest):
    """
    TR_ID: C44870276
    NAME: - Single Football Bet Countered by Stake
    """
    keep_browser_open = True
    max_bet = 1.2
    max_mult_bet = 1.3
    suggested_max_bet = 0.94
    prices = {0: '1/12', 1: '1/13', 2: '1/14'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, default_market_name='|Draw No Bet|', max_bet=self.max_bet)
        self.__class__.eventID, self.__class__.selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_name, self.__class__.selection_id = list(self.selection_ids.items())[0]
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_place_a_single_overask_bet_on_a_football_game(self):
        """
        DESCRIPTION: Place a single overask bet on a football game
        EXPECTED: You should have placed an overask bet
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_mult_bet + 0.42
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_traders_ti_give_a_counter_offer_by_stake(self):
        """
        DESCRIPTION: In trader's TI, give a counter offer by stake
        EXPECTED: You should see a counter offer on the front end
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

    def test_003_check_that_the_stake_is_highlighted_in_yellow_and_that_the_potential_returns_are_correct(self):
        """
        DESCRIPTION: Check that the stake is highlighted in yellow and that the potential returns are correct
        EXPECTED: The stake should be highlighted and the potential returns should be correct
        """
        sections = self.get_betslip_sections()
        multiples_section = sections.Singles
        amount = multiples_section.overask_trader_offer.stake_content.stake_value.value
        self.__class__.amount = float(amount.strip('£'))
        self.assertEqual(self.amount, self.suggested_max_bet,
                         msg=f'The value of suggested stake "{self.suggested_max_bet}" is not present in '
                             f'the "Stake" field, the value is: "{self.amount}"')
        self.assertEqual(multiples_section.overask_trader_offer.stake_content.stake_value.value_color,
                         vec.colors.OVERASK_MODIFIED_PRICE_COLOR, msg=f'Modified price for stake is not highlighted in yellow')
        self.__class__.expected_return = self.get_betslip_content().total_estimate_returns
        self.verify_estimated_returns(est_returns=self.expected_return, bet_amount=self.amount, odds=self.prices[0])

    def test_004_click_on_place_bet_and_check_the_bet_receipt_for_the_correct_stake_and_potential_returns(self):
        """
        DESCRIPTION: Click on Place Bet and check the Bet Receipt for the correct stake and potential returns
        EXPECTED: Your bet should have been placed and the correct stake and potential returns should be seen
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

    def test_005_check_the_bet_in_my_bets_open_bets_for_the_correct_stake_and_potential_returns(self):
        """
        DESCRIPTION: Check the bet in My Bets->Open Bets for the correct stake and potential returns.
        EXPECTED: You should see the bet with the correct stake and potential returns.
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
