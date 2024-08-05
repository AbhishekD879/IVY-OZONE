import re
import tests
import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from collections import OrderedDict
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't grant freebet on prod/hl
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_placement
@pytest.mark.betslip
@pytest.mark.freebets
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_C874312_Place_Tennis_bet_using_Freebet_Token(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C874312
    NAME: Place Tennis bet using Freebet Token
    DESCRIPTION: Bet Placement - Verify that the customer can place a bet on Tennis using a Freebet Token (with a customer that has 0 funds)
    DESCRIPTION: Instructions how to add freebet tokens for TEST2/STAGE users or existing PROD users with already granted tokens can be found here:
    DESCRIPTION: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: A customer with zero balance (£ 0) but has freebets  available.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/select tennis event
        """
        event_params = self.ob_config.add_tennis_event_to_autotest_trophy()
        self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2
        date_time = self.convert_time_to_local(date_time_str=event_params.event_date_time)
        self.__class__.event_name = f'{self.team1} v {self.team2} {date_time}'
        self.__class__.selection_name = self.team1
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.market_name = self.expected_market_sections.match_betting.title()
        self._logger.info(f'*** Tennis event with name "{self.event_name}" and selection ids "{self.selection_ids}"')
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        # We Can not place a free bet with zero account balance
        self.add_card_and_deposit(username=self.username, amount=tests.settings.min_deposit_amount,
                                  card_number=tests.settings.visa_card)
        self.ob_config.grant_freebet(username=self.username,
                                     level='event', id=event_params.event_id)

    def test_001_login_to_oxygen_app_with_a_customer_with_zero_balance_and_at_least_one_freebet(self):
        """
        DESCRIPTION: Login to Oxygen app with a customer with Zero balance and at least one freebet.
        EXPECTED: The customer is logged in
        """
        self.site.login(username=self.username, async_close_dialogs=False)
        self.assertTrue(self.site.header.has_freebets(), msg='User does not have Free bets')

    def test_002_add_a_tennis_selection_selections_to_bet_slip(self):
        """
        DESCRIPTION: Add a Tennis selection/selections to bet slip
        EXPECTED: The selection/selections is added to bet slip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_003_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        EXPECTED: The betslip is loaded
        """
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip is not opened')

    def test_004_select_a_freebet_from_the_freebets_drop_down_customer_needs_to_have_a_zero_balance(self):
        """
        DESCRIPTION: Select a freebet from the freebets drop-down
        DESCRIPTION: (Customer needs to have a zero balance)
        EXPECTED: The freebet is selected
        """
        self.__class__.bet_info = OrderedDict()
        section = self.get_betslip_sections().Singles
        stake = list(self.zip_available_stakes(section=section, number_of_stakes=1).items())[0]
        # magic is happening here on the lad qa2, left unchanged currently, may fail after click on freebet on dialog
        # user is redirected to page to set nickname, but in case with manual click (not via code) it works ok
        selected_free_bet = self.select_freebet_for_stake(stake=stake)
        freebet_stake = float(re.search(r'\d+.\d+', selected_free_bet).group())
        self.__class__.expected_stake = f"{freebet_stake:.2f}"
        params = self.collect_stake_info(stake=stake)
        self.bet_info[stake[0]] = params
        betslip = self.get_betslip_content()
        total_stake_betslip = float(betslip.total_stake)
        self.bet_info['total_stake'] = total_stake_betslip
        total_est_returns = betslip.total_estimate_returns
        self.bet_info['total_estimate_returns'] = float(total_est_returns)

    def test_005_click_on_place_bet_button(self):
        """
        DESCRIPTION: Click on 'Place Bet' button
        EXPECTED: The bet is successfully placed and bet receipt is displayed.
        """
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(timeout=1.5), msg='Place Bet button is not enabled')
        bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_006_verify_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Bet receipt
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type is displayed: (e.g: double);
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: Correct Event is displayed;
        EXPECTED: * 'Cashout' label between the bet and Bet ID (if cashout is available for this event)
        EXPECTED: **Unique Bet ID is displayed;
        EXPECTED: The balance is correctly updated;
        EXPECTED: **Odds are exactly the same as when bet has been placed;
        EXPECTED: **Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed;
        EXPECTED: **Estimated Returns is exactly the same as when bet has been placed;
        EXPECTED: "Reuse Selection" and "Done" buttons are displayed.
        """
        self.check_bet_receipt(betslip_info=self.bet_info, freebet=True)
        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Can not find "Reuse selection" button')
        self.assertTrue(self.site.bet_receipt.footer.has_done_button(), msg='Can not find "Done" button')
        self.site.close_betreceipt()

    def test_007_click_on_my_bets(self):
        """
        DESCRIPTION: Click on My Bets
        EXPECTED: My Bets page is opened
        """
        self.site.open_my_bets_open_bets()

    def test_008_go_to_the_bet_that_was_just_placed_and_verify_bet_details(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify bet details.
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type , Selection Name and odds are displayed
        EXPECTED: Event Name is displayed
        EXPECTED: Selection Details:
        EXPECTED: Selection Name where the bet has been placed
        EXPECTED: Event name
        EXPECTED: **Time and Date
        EXPECTED: **Market where the bet has been placed
        EXPECTED: **E/W Terms: (None for bets where E/W is not valid)
        EXPECTED: **Correct Stake is correctly displayed;
        """
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)

        self.assertEqual(bet.bet_type, vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                         msg=f'Bet type "{bet.bet_type}" is not the same as expected "{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}"')

        bet_legs = bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: "{bet_name}"')

        name, selection = list(bet_legs.items())[0]
        self.assertEqual(selection.outcome_name, self.selection_name,
                         msg=f'Selection name "{selection.outcome_name}" is not the same as '
                             f'expected "{self.selection_name}"')
        self.assertEqual(selection.market_name, self.market_name,
                         msg=f'Market name "{selection.market_name}" is not the same as '
                             f'expected "{ self.market_name}"')
        expected_odds = self.bet_info[self.selection_name]['odds']
        self.assertEqual(selection.odds_value, expected_odds,
                         msg=f'Odds "{selection.odds_value}" is not the same as expected "{expected_odds}"')
        self.assertEqual(bet.stake.stake_value, self.expected_stake,
                         msg=f'Bet stake "{bet.stake.stake_value}" is not as entered on Betslip "{self.expected_stake}"')
        currency = '£'
        self.assertEqual(bet.stake.currency, currency,
                         msg=f'Stake currency "{bet.stake.currency}" is not the same as expected "{currency}"')
        expected_est_returns = self.bet_info[self.selection_name]['estimate_returns']
        self.assertAlmostEqual(float(bet.est_returns.stake_value), expected_est_returns, delta=0.02,
                               msg=f'Estimate returns "{float(bet.est_returns.stake_value)}" is not the same as '
                                   f'calculated on Betslip "{expected_est_returns}" within 0.02 delta')
        self.assertEqual(bet.est_returns.currency, currency,
                         msg=f'Estimate returns currency "{bet.est_returns.currency}" is not the same as '
                             f'expected "{currency}"')

    def test_009_click_on_user_menu___logout(self):
        """
        DESCRIPTION: Click on User Menu -> logout
        EXPECTED: Customer is logged out
        """
        self.site.logout()
