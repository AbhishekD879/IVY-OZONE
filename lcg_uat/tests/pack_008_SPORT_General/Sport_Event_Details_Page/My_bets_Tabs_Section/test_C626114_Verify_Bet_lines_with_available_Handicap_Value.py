import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.handicap
@pytest.mark.event_details
@pytest.mark.bet_placement
@pytest.mark.my_bets
@pytest.mark.medium
@pytest.mark.cash_out
@pytest.mark.safari
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C626114_Verify_Bet_lines_with_available_Handicap_Value(BaseCashOutTest):
    """
    TR_ID: C626114
    NAME: Bet lines with available Handicap Value
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed a bet on Pre Match or In-Play match (Singles and Multiple bets) where Cash Out offer is available
    PRECONDITIONS: Make sure user has placed Singles and Multiple bets with available handicap value
    """
    keep_browser_open = True

    handicap_positive = 'handicap_match_result +3.0'
    handicap_negative = 'handicap_match_result -3.0'
    selection_name, selection_name2 = None, None
    created_event_name2 = None
    bet = None
    bet_amount = 1.00

    def test_000_preconditions(self):
        """
        DESCRIPTION: Run Cash Out precondition steps which creates testing data
        EXPECTED: Created events with cashout available
        EXPECTED: User have placed bets for bots Single and Multiple bets
        """
        events = self.create_several_autotest_premier_league_football_events(markets=[('handicap', {'cashout': True})],
                                                                             number_of_events=2)
        event1, event2 = events
        self.__class__.eventID = event1.event_id
        self.__class__.selection_name = '%s (+3.0)' % event1.team1
        self.__class__.selection_name2 = '%s (-3.0)' % event2.team1
        self.__class__.team1 = event1.team1
        self.__class__.team2 = event2.team1
        self.__class__.created_event_name = event1.event_name
        self.__class__.created_event_name2 = event2.event_name

        self.site.login()

        self.open_betslip_with_selections(selection_ids=(event1.selection_ids[self.handicap_positive][event1.team1],
                                                         event2.selection_ids[self.handicap_negative][event2.team1]))
        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_event_details_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets from preconditions
        """
        self.navigate_to_edp(self.eventID)
        self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)

    def test_002_go_to_verified_single_cash_out_bet_line(self):
        """
        DESCRIPTION: Go to verified **Single** Cash Out bet line
        """
        bet_name, self.__class__.bet = \
            self.site.sport_event_details.my_bets.accordions_list.get_bet(event_names=self.team1)

    def test_003_verify_handicap_value_and_sign(self):
        """
        DESCRIPTION: Verify handicap value and sign
        EXPECTED: Handicap value is displayed directly to the right of the outcome names in parentheses (e.g. <Outcome Name> (handicap value))
        EXPECTED: If **'handicapValueDec'** contains '-' sign - display it with this '-' sign (negative value) on the front end
        EXPECTED: If **'handicapValueDec'** contains '+' sign in the response - display '+' sign before the value on front end
        """
        self.__class__.bet_legs = self.bet.items_as_ordered_dict
        self.assertTrue(self.bet_legs, msg='No bet legs found')
        name = self.selection_name
        self.assertTrue(name in self.bet_legs, msg=f'"{name}" not found in "{self.bet_legs.keys()}"')
        bet_leg = self.bet_legs[name]
        expected_market = f'Handicap Match Result - {self.team1} +3.0 goals'
        self.assertEqual(bet_leg.market_name, expected_market,
                         msg=f'Market "{bet_leg.market_name,}" is not same as expected "{expected_market}"')

    def test_004_go_to_verified_multiple_cash_out_bet_line(self):
        """
        DESCRIPTION: Go to verified **Multiple** Cash Out bet line
        """
        bet_name, self.__class__.bet = \
            self.site.sport_event_details.my_bets.accordions_list.get_bet(event_names=[self.team1, self.team2])

    def test_005_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step 3
        DESCRIPTION: Verify handicap value and sign
        EXPECTED: Handicap value is displayed directly to the right of the outcome names in parentheses (e.g. <Outcome Name> (handicap value))
        EXPECTED: If **'handicapValueDec'** contains '-' sign - display it with this '-' sign (negative value) on the front end
        EXPECTED: If **'handicapValueDec'** contains '+' sign in the response - display '+' sign before the value on front end
        """
        self.test_003_verify_handicap_value_and_sign()

        name = self.selection_name2
        self.assertTrue(name in self.bet_legs, msg=f'"{name}" not found in "{self.bet_legs.keys()}"')
        expected_market = 'Handicap Match Result - %s -3.0 goals' % self.team2
        self.assertEqual(self.bet_legs[name].market_name, expected_market,
                         msg=f'Market "{self.bet_legs[name].market_name}" is not same as expected "{expected_market}"')
