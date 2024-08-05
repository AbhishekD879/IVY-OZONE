import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.high
@pytest.mark.bet_history
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C2507412_Winning_a_Multiple_Bet(BaseBetSlipTest):
    """
    TR_ID: C2507412
    NAME: Winning a Multiple Bet
    DESCRIPTION: This test case verifies Winning a Bet for multiple selections
    PRECONDITIONS: 1. User should be Log in
    PRECONDITIONS: 2. User should have sufficient funds to place a bet
    PRECONDITIONS: 3. How to trigger the situation when user wins a bet https://confluence.egalacoral.com/pages/viewpage.action?pageId=96150627
    """
    keep_browser_open = True
    bet_amount = 1
    odds = 1.5

    def test_001_add_couple_selections_from_different_events_to_the_betlsip(self):
        """
        DESCRIPTION: Add couple selections from different events to the Betlsip
        EXPECTED:
        """
        event_params_1 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.first_selection, self.__class__.selection_ids_1 = event_params_1.team1, event_params_1.selection_ids

        event_params_2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.second_selection, self.__class__.selection_ids_2 = event_params_2.team1, event_params_2.selection_ids

        self.__class__.eventID_1 = event_params_1.event_id
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.marketID_1 = self.ob_config.market_ids[event_params_1.event_id][market_short_name]
        self.__class__.event_name_1 = f'{event_params_1.team1} v {event_params_1.team2}'

        self.__class__.eventID_2 = event_params_2.event_id
        self.__class__.marketID_2 = self.ob_config.market_ids[event_params_2.event_id][market_short_name]
        self.__class__.event_name_2 = f'{event_params_2.team1} v {event_params_2.team2}'

        self.site.login(username=tests.settings.betplacement_user)

    def test_002_open_betslip_multiples_section(self):
        """
        DESCRIPTION: Open Betslip, 'Multiples' section
        EXPECTED: 'Multiples' section is opened
        """
        self.__class__.balance = self.site.header.user_balance
        self.open_betslip_with_selections(selection_ids=(self.selection_ids_1[self.first_selection],
                                                         self.selection_ids_2[self.second_selection]))

        selection_list = self.get_betslip_content().betslip_sections_list
        self.assertEqual(selection_list.multiple_selections_label, vec.betslip.MULTIPLES,
                         msg=f'Section name "{selection_list.multiple_selections_label}" '
                         f'is not the same as expected "{vec.betslip.MULTIPLES}"')

    def test_003_enter_correct_stake_in_stake_field_and_tap_bet_now(self):
        """
        DESCRIPTION: Enter correct Stake in 'Stake' field and tap 'Bet Now'
        EXPECTED: *  Bet is placed successfully
        EXPECTED: *  User 'Balance' is decreased by value entered in 'Stake' field
        EXPECTED: *  Bet Slip is replaced with a Bet Receipt view
        """
        self.place_multiple_bet(number_of_stakes=1, multiples=True)
        self.check_bet_receipt_is_displayed()
        if self.device_type != 'desktop':
            self.__class__.new_balance = self.site.bet_receipt.user_header.user_balance
        else:
            self.__class__.new_balance = self.site.header.user_balance
        self.verify_user_balance(expected_user_balance=self.balance - self.bet_amount)

        self.assertTrue(self.site.bet_receipt.footer.has_done_button(),
                        msg='Done button is not shown, Bet was not placed')
        try:
            self.assertEqual(self.site.bet_receipt.bet_receipt_header_name, vec.betslip.BET_RECEIPT,
                             msg=f'Page title "{self.site.bet_receipt.bet_receipt_header_name}" is '
                                 f'not the same as expected "{vec.betslip.BET_RECEIPT}"')
        except NotImplementedError as e:
            self._logger.warning(e)

    def test_004_trigger_the_situation_when_user_wins_multiple_bet_each_of_selections_is_won(self):
        """
        DESCRIPTION: Trigger the situation when user wins Multiple bet (each of selections is won)
        EXPECTED: User balance is increased on bet win amount immediately
        """
        self.result_event(selection_ids=self.selection_ids_1[self.first_selection],
                          market_id=self.marketID_1, event_id=self.eventID_1)
        self.result_event(selection_ids=self.selection_ids_2[self.second_selection],
                          market_id=self.marketID_2, event_id=self.eventID_2)

        self.verify_user_balance(expected_user_balance=self.new_balance + self.bet_amount * self.odds * self.odds, timeout=15)

    def test_005_go_to_bet_history(self):
        """
        DESCRIPTION: Go to Settled Bets
        EXPECTED: * 'Won' label is present on the Multiples header
        EXPECTED: * 'Won' label is present next to each market
        """
        self.navigate_to_page(name='bet-history')
        self.site.wait_content_state('BetHistory')

        bet_name, bet = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
            event_names=[self.event_name_1, self.event_name_2],
            number_of_bets=2)
        self.assertTrue(bet.bet_status == vec.betslip.WON_STAKE, msg=f'Bet {bet_name} does not have WON status on header')

        bet_legs = list(bet.items_as_ordered_dict.items())
        self.assertTrue(len(bet_legs) == 2, msg=f'Number of bet legs "{len(bet_legs)}" is not the same as expected '
                                                f'for bet type DOUBLE: "2"')
        for bet_leg_name, bet_leg in bet_legs:
            self.assertEqual(bet_leg.icon.status, 'won', msg=f'Bet {bet_leg_name} does not have WON status next to market')
