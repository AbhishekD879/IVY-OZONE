import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.open_bets
@pytest.mark.handicap
@pytest.mark.ob_smoke
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@pytest.mark.login
@vtest
class Test_C29216_C29018_Verify_Bet_Details_for_Single_Bet_with_Handicap_Value_Available_on_Open_Bets_Settled_Bets(BaseBetSlipTest):
    """
    TR_ID: C29216
    TR_ID: C29018
    NAME: Verify Bet Details for Single Bet with Handicap Value Available on Open Bets/Settled Bets
    DESCRIPTION: This test case verifies Bet Details for Bet which has handicap value available
    """
    keep_browser_open = True
    handicap_value = None
    expected_selection_name, expected_market_name = None, None
    bet_type = 'SINGLE'

    def test_001_create_event(self):
        """
        DESCRIPTION: Create test event with Handicap market
        EXPECTED: Test event was created
        """
        event_parameters = self.ob_config.add_autotest_premier_league_football_event(markets=[('handicap_match_result',
                                                                                               {'cashout': True})],
                                                                                     timeout=15)
        self.__class__.team1, self.__class__.team2 = event_parameters.team1, event_parameters.team2
        self.__class__.created_event_name = '%s v %s %s' \
                                            % (self.team1,
                                               self.team2,
                                               self.convert_time_to_local(date_time_str=event_parameters.event_date_time))
        self.__class__.selection_ids = event_parameters.selection_ids
        self.__class__.handicap_value = '+1.0'
        self.__class__.expected_selection_name = f'{self.team1} ({self.handicap_value})'
        self.__class__.expected_market_name = f'Handicap Match Result - {self.team1} {self.handicap_value} goals'

    def test_002_login(self):
        """
        DESCRIPTION: Login as user that has sufficient funds to place bet
        EXPECTED: User logged successfully
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_003_add_handicap_selection_to_betslip(self):
        """
        DESCRIPTION: Add Handicap selection to betslip
        EXPECTED: Selection is added, counter is increased by 1
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[f'handicap_match_result {self.handicap_value}'][self.team1])

    def test_004_place_bet(self):
        """
        DESCRIPTION: Place single bet
        EXPECTED: Bet receipt section is shown
        """
        self.__class__.betslip_info = self.place_and_validate_single_bet()

    def test_005_close_bet_receipt(self):
        """
        DESCRIPTION: Close bet receipt
        EXPECTED: Bet receipt is closed
        """
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_006_go_to_open_bets_page(self):
        """
        DESCRIPTION: Go to Open Bets page
        EXPECTED: Open Bets page opened with relevant content
        """
        self.site.open_my_bets_open_bets()
        if self.device_type != 'desktop':
            current_tab = self.site.open_bets.tabs_menu.current
        else:
            current_tab = self.site.betslip.tabs_menu.current
        self.assertEqual(current_tab, vec.bet_history.OPEN_BETS_TAB_NAME,
                         msg=f'"{current_tab}" is active while expected "{vec.bet_history.OPEN_BETS_TAB_NAME}"')
        current_grouping_button = self.site.open_bets.tab_content.grouping_buttons.current
        active_btn_open_bets = self.expected_active_btn_open_bets.title() if self.brand == 'ladbrokes'\
            else self.expected_active_btn_open_bets
        self.assertEqual(current_grouping_button, active_btn_open_bets,
                         msg=f'"{current_grouping_button}" grouping button is active while '
                         f'expected "{active_btn_open_bets}"')

    def test_007_verify_open_bets_bet_details(self):
        """
        DESCRIPTION: Verify bet details
        DESCRIPTION: Verify Event name and associated event type
        EXPECTED: The following information is shown in the bet overview:
        EXPECTED: Bet type
        EXPECTED: Selection name user has bet on and handicap value e.g. Tie (+2.0)
        EXPECTED: Odds of selection
        EXPECTED: Market name user has bet on - e.g., "Match Result & Both Teams to Score"
        EXPECTED: Event name and event start date and time in DD MM, HH:MM format using 12-hour clock (AM/PM) (e.g. 05 Jan, 1:49PM)
        EXPECTED: Date of bet placement and bet receipt ID are shown below bet details
        EXPECTED: Stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: Est. Returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: Event name and associated event type are hyperlinked
        EXPECTED: User is navigated to Event Details page after tapping Event name
        """
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=self.bet_type,
                                                                                event_names=self.created_event_name,
                                                                                number_of_bets=1)
        self.assertEqual(bet.bet_type, self.bet_type,
                         msg=f'Bet type "{bet.bet_type}" is not the same as expected "{self.bet_type}"')
        bet_legs = bet.items_as_ordered_dict
        self.assertEqual(len(bet_legs), 1,
                         msg=f'Number of bet legs "{len(bet_legs)}" is not the same as expected for '
                         f'bet type "{self.bet_type}": "1"')
        name, selection = list(bet_legs.items())[0]
        self.assertEqual(selection.outcome_name, self.expected_selection_name,
                         msg=f'Selection name "{selection.outcome_name}" is not the same as '
                         f'expected "{self.expected_selection_name}"')
        self.assertEqual(selection.market_name, self.expected_market_name,
                         msg=f'Market name "{selection.market_name}" is not the same as '
                         f'expected "{self.expected_market_name}"')
        expected_odds = self.betslip_info[self.expected_selection_name]['odds']
        self.assertEqual(selection.odds_value, expected_odds,
                         msg=f'Odds "{selection.odds_value}" is not the same as expected "{expected_odds}"')
        bet_amount = '%0.2f' % self.bet_amount
        self.assertEqual(bet.stake.stake_value, bet_amount,
                         msg=f'Bet amount "{bet.stake.stake_value}" is not as entered on Betslip "{bet_amount}"')
        currency = '£'
        self.assertEqual(bet.stake.currency, currency,
                         msg=f'Stake currency "{bet.stake.currency}" is not the same as expected "{currency}"')
        expected_est_returns = self.betslip_info[self.expected_selection_name]['estimate_returns']
        self.assertAlmostEqual(float(bet.est_returns.stake_value), expected_est_returns, delta=0.02,
                               msg=f'Estimate returns "{float(bet.est_returns.stake_value)}" is not the same as '
                               f'calculated on Betslip "{expected_est_returns}" within 0.02 delta')
        self.assertEqual(bet.est_returns.currency, currency,
                         msg=f'Estimate returns currency "{bet.est_returns.currency}" is not the same as '
                         f'expected "{currency}"')

        selection.click_event_name()
        self.site.wait_content_state('EventDetails')
