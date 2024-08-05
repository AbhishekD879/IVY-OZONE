import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.open_bets
@pytest.mark.handicap
@pytest.mark.ob_smoke
@pytest.mark.bet_placement
@pytest.mark.bet_history_open_bets
@pytest.mark.login
@vtest
class Test_C29217_Verify_Bet_Details_for_Multiple_Bet_with_Handicap_Value_Available_on_Open_Bets_Settled_Bets(BaseBetSlipTest):
    """
    TR_ID: C29217
    VOL_ID: C9697980
    NAME: Verify Bet Details for Multiple Bet with Handicap Value Available on Open Bets/Settled Bets
    DESCRIPTION: This test case verifies Bet Details for Multiple Bet if selections have handicap value availabl
    DESCRIPTION: AUTOTEST [C9697980]
    PRECONDITIONS: 1. User should be logged in
    PRECONDITIONS: 2. User has placed a multiple bet with Handicap
    PRECONDITIONS: 3. User has a settled multiple bet with Handicap
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'handicapValueDec' **on outcome level- to see whether handicap value is available for outcome
    """
    keep_browser_open = True
    bet_amount = 1.00
    handicap_value_event1_plus, handicap_value_event2_minus, handicap_value_event2_plus = None, None, None
    expected_selection_name1, expected_selection_name2, expected_selection_with_event_name2_ob_page, expected_selection_name2_ob_page, \
        expected_market_name1, expected_market_name2 = None, None, None, None, None, None
    bet_type = 'DOUBLE'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event with Handicap market
        EXPECTED: Test event was created
        """
        params1 = self.ob_config.add_autotest_premier_league_football_event(
            markets=[('handicap_match_result', {'cashout': True})],
            timeout=15)
        params2 = self.ob_config.add_autotest_premier_league_football_event(
            markets=[('handicap_match_result', {'cashout': True})],
            timeout=15)
        self.__class__.team1, self.__class__.team2 = params1.team1, params1.team2
        self.__class__.team2_1, self.__class__.team2_2 = params2.team1, params2.team2
        self.__class__.created_event_name = self.team1 + ' v ' + self.team2
        self.__class__.created_event_name2 = self.team2_1 + ' v ' + self.team2_2
        event1_start_time_local = self.convert_time_to_local(date_time_str=params1.event_date_time)
        event2_start_time_local = self.convert_time_to_local(date_time_str=params2.event_date_time)
        self.__class__.selection_ids, self.__class__.selection_ids2 = params1.selection_ids, params2.selection_ids
        self.__class__.handicap_value_event1_minus, self.__class__.handicap_value_event1_plus = '-1.0', '+1.0'
        self.__class__.handicap_value_event2_minus, self.__class__.handicap_value_event2_plus = '-3.0', '+3.0'
        self.__class__.expected_selection_name1 = '%s (%s)' % (self.team1, self.handicap_value_event1_plus)
        self.__class__.expected_selection_name2 = '%s (%s)' % (self.team2_2, self.handicap_value_event2_minus)
        self.__class__.expected_selection_name2_ob_page = self.expected_selection_name2.replace(self.handicap_value_event2_minus, self.handicap_value_event2_plus)
        self.__class__.expected_selection_with_event_name1_ob_page = ('%s - %s %s' %
                                                                      (self.expected_selection_name1,
                                                                       self.created_event_name.replace(
                                                                           self.handicap_value_event1_minus,
                                                                           self.handicap_value_event1_plus),
                                                                       event1_start_time_local))
        self.__class__.expected_selection_with_event_name2_ob_page = ('%s - %s %s' %
                                                                      (self.expected_selection_name2.replace(
                                                                          self.handicap_value_event2_minus,
                                                                          self.handicap_value_event2_plus),
                                                                       self.created_event_name2,
                                                                       event2_start_time_local))

        self.__class__.expected_market_name1 = f'Handicap Match Result - {self.team1} {self.handicap_value_event1_plus} goals'
        self.__class__.expected_market_name2 = f'Handicap Match Result - {self.team2_1} {self.handicap_value_event2_minus} goals'

    def test_001_login(self):
        """
        DESCRIPTION: Login as user that has sufficient funds to place bet
        EXPECTED: User logged successfully
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_add_handicap_selection_to_betslip(self):
        """
        DESCRIPTION: Add 2 Handicap selection from different events to betslip
        EXPECTED: Selections are added, counter is increased by 2
        """
        selection_ids = (self.selection_ids[f'handicap_match_result {self.handicap_value_event1_plus}'][self.team1],
                         self.selection_ids2[f'handicap_match_result {self.handicap_value_event2_minus}'][self.team2_2])
        self.open_betslip_with_selections(selection_ids=selection_ids)

    def test_003_place_bet(self):
        """
        DESCRIPTION: Place multiple bet
        EXPECTED: Bet receipt section is shown
        """
        self.__class__.betslip_info = self.place_and_validate_multiple_bet()

    def test_004_close_bet_receipt(self):
        """
        DESCRIPTION: Close bet receipt
        EXPECTED: Bet receipt is closed
        """
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_005_go_to_open_bets_page(self):
        """
        DESCRIPTION: Go to Open Bets page
        EXPECTED: Open Bets page opened with relevant content
        """
        self.site.open_my_bets_open_bets()
        if self.device_type != 'desktop':
            page_title = self.site.open_bets.header_line.page_title.title
        else:
            page_title = self.get_betslip_content().name
        my_bets_page_title = self.expected_my_bets_page_title.title() if \
            (self.device_type != 'desktop' and self.brand == 'ladbrokes') else self.expected_my_bets_page_title
        self.assertEqual(page_title, my_bets_page_title,
                         msg=f'Page title "{page_title}" doesn\'t match expected text "{my_bets_page_title}"')
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
                         msg=f'"{current_grouping_button}" grouping button is active while expected "{active_btn_open_bets}"')

    def test_006_verify_open_bets_bet_details(self):
        """
        DESCRIPTION: Verify bet details
        DESCRIPTION: Verify Event name and associated event type
        EXPECTED: The following information is shown in the bet overview:
        EXPECTED: * Bet type
        EXPECTED: * Selection name user has bet on and handicap value e.g. Tie (+2.0)
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Tie (+3.0) @1/4)
        EXPECTED: * Market name user has bet on - e.g., "Match Result & Both Teams to Score"
        EXPECTED: * Event name and event start date and time in DD MM, HH:MM format using 12-hour clock (AM/PM) (e.g. 05 Jan, 1:49PM)
        EXPECTED: * The above described details are shown for each selection, included in the multiple, one under another
        EXPECTED: At the bottom of the multiple section the following details are shown:
        EXPECTED: * Stake value <currency symbol> <value> (e.g., £30.00)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: At the bottom of the multiple section the following details are shown:
        """
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=self.bet_type,
                                                                                event_names=self.created_event_name,
                                                                                number_of_bets=5)
        self.assertEqual(bet.bet_type, self.bet_type,
                         msg=f'Bet type "{bet.bet_type}" is not the same as expected "{self.bet_type}"')
        bet_legs = bet.items_as_ordered_dict
        self.assertEqual(len(bet_legs), 2, msg=f'Number of bet legs "{len(bet_legs)}" is not the same as expected for bet type "{self.bet_type}": "2"')

        selection1 = bet_legs.get(self.expected_selection_with_event_name1_ob_page)
        self.assertTrue(selection1,
                        msg=f'Selection "{self.expected_selection_with_event_name1_ob_page}" was not found in "{bet_legs.keys()}"')
        selection2 = bet_legs.get(self.expected_selection_with_event_name2_ob_page)
        self.assertTrue(selection2, msg=f'Selection "{self.expected_selection_with_event_name2_ob_page}" was not found')
        self.assertEqual(selection1.outcome_name, self.expected_selection_name1,
                         msg=f'Selection name "{selection1.outcome_name}" is not the same as expected "{self.expected_selection_name1}"')

        self.assertEqual(selection2.outcome_name, self.expected_selection_name2_ob_page,
                         msg=f'Selection name "{selection2.outcome_name}" is not the same as expected "{self.expected_selection_name2_ob_page}"')

        self.assertEqual(selection1.market_name, self.expected_market_name1,
                         msg=f'Market name "{selection1.market_name}" is not the same as expected "{self.expected_market_name1}"')
        self.assertEqual(selection2.market_name, self.expected_market_name2,
                         msg=f'Market name "{selection2.market_name}" is not the same as expected "{self.expected_market_name2}"')

        expected_odds1 = self.betslip_info[self.expected_selection_name1]['odds']
        expected_odds2 = self.betslip_info[self.expected_selection_name2_ob_page]['odds']
        self.assertEqual(selection1.odds_value, expected_odds1,
                         msg=f'Odds "{selection1.odds_value}" is not the same as expected "{expected_odds1}"')
        self.assertEqual(selection2.odds_value, expected_odds2,
                         msg=f'Odds "{selection2.odds_value}" is not the same as expected "{expected_odds2}"')

        bet_amount = '%0.2f' % self.bet_amount
        self.assertEqual(bet.stake.stake_value, bet_amount,
                         msg=f'Bet amount "{bet.stake.stake_value}" is not as entered on Betslip "{bet_amount}"')
        currency = '£'
        self.assertEqual(bet.stake.currency, currency,
                         msg=f'Stake currency "{bet.stake.currency}" is not the same as expected "{currency}"')
        expected_est_returns = self.betslip_info[self.bet_type.title()]['estimate_returns']
        self.assertEqual(bet.est_returns.stake_value, str(expected_est_returns),
                         msg=f'Estimate returns "{bet.est_returns.stake_value}" is not the same as '
                         f'calculated on Betslip "{str(expected_est_returns)}"')
        self.assertEqual(bet.est_returns.currency, currency,
                         msg=f'Estimate returns currency "{bet.est_returns.currency}" is not the same '
                         f'as expected "{currency}"')
