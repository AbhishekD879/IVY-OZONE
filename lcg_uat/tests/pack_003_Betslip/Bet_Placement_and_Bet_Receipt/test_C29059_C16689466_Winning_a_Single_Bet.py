import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl  # cannot settle events on prod
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.high
@pytest.mark.safari
@pytest.mark.login
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1248')
@vtest
class Test_C29059_C16689466_Winning_a_Single_Bet(BaseBetSlipTest):
    """
    TR_ID: C29059
    TR_ID: C16689466
    NAME: Winning a Single Bet
    DESCRIPTION: This test case verifies Winning a Bet for single selection
    PRECONDITIONS: 1. User should be Log in
    PRECONDITIONS: 2. User should have sufficient funds to place a bet
    PRECONDITIONS: 3. How to trigger the situation when user wins a bet https://confluence.egalacoral.com/pages/viewpage.action?pageId=96150627
    """
    keep_browser_open = True
    bet_amount = 3
    odds = 1.5

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add one selection to the Bet Slip
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()

        self.__class__.eventID = event_params.event_id
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.marketID = self.ob_config.market_ids[event_params.event_id][market_short_name]
        self.__class__.team1 = event_params.team1
        self.__class__.selection_id = event_params.selection_ids[self.team1]
        self.__class__.event_name = '%s v %s' % (event_params.team1, event_params.team2)

        self.site.login(username=tests.settings.betplacement_user)

    def test_001_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: Added selection is displayed
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

        if self.device_type in ['mobile', 'tablet']:
            self.__class__.balance = self.get_betslip_content().header.user_balance
        else:
            self.__class__.balance = self.site.header.user_balance

        singles_section = self.get_betslip_sections().Singles
        selections_count = self.get_betslip_content().selections_count
        self.assertEqual(selections_count, '1',
                         msg='Singles selection count "%s" is not the same as expected "%s"' %
                             (selections_count, '1'))
        stake = singles_section.get(self.team1)
        self.assertTrue(stake, msg=f'"{self.team1}" stake was not found on the Betslip')

        self.verify_betslip_counter_change(expected_value=1)

    def test_002_enter_correct_stake_in_stake_field_and_tap_bet_now(self):
        """
        DESCRIPTION: Enter correct Stake in 'Stake' field and tap 'Bet Now'
        EXPECTED: *  Bet is placed successfully
        EXPECTED: *  User 'Balance' is decreased by value entered in 'Stake' field
        EXPECTED: *  Bet Slip is replaced with a Bet Receipt view
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.__class__.new_balance = self.site.bet_receipt.user_header.user_balance
        self.verify_user_balance(self.balance - self.bet_amount)

        self.assertTrue(self.site.bet_receipt.footer.has_done_button(),
                        msg='Done button is not shown, Bet was not placed')
        try:
            self.assertEqual(self.site.bet_receipt.bet_receipt_header_name, vec.betslip.BET_RECEIPT,
                             msg=f'Page title "{self.site.bet_receipt.bet_receipt_header_name}" is '
                                 f'not the same as expected "{vec.betslip.BET_RECEIPT}"')
        except NotImplementedError as e:
            self._logger.warning(e)

    def test_003_trigger_the_situation_when_user_wins_a_bet(self):
        """
        DESCRIPTION: Trigger the situation when user wins a bet
        EXPECTED: User balance is increased on bet win amount immediately
        """
        self.ob_config.result_selection(selection_id=self.selection_id, market_id=self.marketID, event_id=self.eventID,
                                        wait_for_update=True)
        self.ob_config.confirm_result(selection_id=self.selection_id, market_id=self.marketID, event_id=self.eventID,
                                      wait_for_update=True)
        self.ob_config.settle_result(selection_id=self.selection_id, market_id=self.marketID, event_id=self.eventID,
                                     wait_for_update=True)

        self.verify_user_balance(expected_user_balance=self.new_balance + self.bet_amount * self.odds)

    def test_004_go_to_bet_history(self):
        """
        DESCRIPTION: Go to Settled Bets
        EXPECTED: * 'Won' label is present on the Singles header
        EXPECTED: * 'Won' label is present next to market
        """
        self.navigate_to_page(name='bet-history')
        self.site.wait_content_state('BetHistory')

        bet_name, bet = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type='SINGLE',
            event_names=self.event_name,
            number_of_bets=1)
        self.assertTrue(bet.bet_status == vec.betslip.WON_STAKE, msg=f'Bet {bet_name} does not have WON status on header')

        bet_legs = list(bet.items_as_ordered_dict.items())
        self.assertTrue(len(bet_legs) == 1, msg=f'Number of bet legs "{len(bet_legs)}" is not the same as expected '
                                                f'for bet type SINGLE: "1"')
        bet_leg_name, bet_leg = bet_legs[0]
        self.assertEqual(bet_leg.icon.status, 'won', msg=f'Bet {bet_name} does not have WON status next to market')
