import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.open_bets
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870287__Single_Sports_Bet_Accepted(BaseBetSlipTest):
    """
    TR_ID: C44870287
    NAME: - Single Sports Bet Accepted
    """
    keep_browser_open = True
    max_bet = 0.15
    prices = {0: '1/20', 1: '1/10', 2: '1/16'}

    def test_000_preconditions(self):
        """
        DESCRIPTION:Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet,
                                                                                 default_market_name='|Draw No Bet|')
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_name, self.__class__.selection_id = list(selection_ids.items())[0]
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_place_a_single_oa_bet_on_any_sport_except_hr_and_gh(self):
        """
        DESCRIPTION: Place a single OA bet on any sport except HR and GH
        EXPECTED: The bet should go through to the OA flow
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_and_validate_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_the_traders_interface_accept_the_bet(self):
        """
        DESCRIPTION: In the Trader's Interface, accept the bet
        EXPECTED: On the Front End, you should see the bet receipt
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.accept_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)
        self.check_bet_receipt_is_displayed()

    def test_003_check_that_the_bet_shows_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Check that the bet shows in My Bets->Open Bets
        EXPECTED: The bet should show in My Bets->Open Bets
        """
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        open_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(open_bets,
                        msg='No bets found in open bet')
        bet = list(open_bets.values())[0]
        betlegs = list(bet.items_as_ordered_dict.values())[0]
        outcome = betlegs.outcome_name
        actual_stake = bet.stake.stake_value
        actual_est_returns = bet.est_returns.stake_value
        self.assertEqual(outcome, self.selection_name,
                         msg=f'Actual outcome:{outcome} is not same as'
                             f'Expected outcome: {self.selection_name}')
        self.assertIn(str(self.bet_amount), actual_stake,
                      msg=f'Actual stake: "{actual_stake}" is not same as '
                          f'Expected stake:"{str(self.bet_amount)}"')
        self.verify_estimated_returns(est_returns=actual_est_returns, bet_amount=self.bet_amount, odds=self.prices[0])
