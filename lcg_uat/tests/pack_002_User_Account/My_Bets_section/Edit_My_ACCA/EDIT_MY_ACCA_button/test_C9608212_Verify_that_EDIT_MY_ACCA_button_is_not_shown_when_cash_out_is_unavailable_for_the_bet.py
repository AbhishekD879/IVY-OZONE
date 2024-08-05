import pytest
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.cash_out
@pytest.mark.portal_dependant
@vtest
class Test_C9608212_Verify_that_EDIT_MY_ACCA_button_is_not_shown_when_cash_out_is_unavailable_for_the_bet(BaseBetSlipTest):
    """
    TR_ID: C9608212
    NAME: Verify that 'EDIT MY ACCA' button is not shown when cash out is unavailable for the bet
    DESCRIPTION: This test case verifies that 'EDIT MY ACCA' button is not shown when cash out is unavailable for the bet
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Place a MULTIPLE bet where one of the events in the bet with CASH OUT unavailable (- In AccountHistory?DetailLevel... response: cashoutValue: "CASHOUT_SELN_NO_CASH)
    PRECONDITIONS: **Coral** has 'EDIT MY BET' button
    PRECONDITIONS: **Ladbrokes** has 'EDIT MY ACCA' button
    """
    keep_browser_open = True
    number_of_events = 4
    bet_amount = 5

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should be logged in
        PRECONDITIONS: Place a MULTIPLE bet where one of the events in the bet with CASH OUT unavailable (- In AccountHistory?DetailLevel... response: cashoutValue: "CASHOUT_SELN_NO_CASH).
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.NOT_EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.NOT_EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)
            outcomes = next(((market['market']['children']) for market in events[0]['event']['children']), None)
            outcomes2 = next(((market['market']['children']) for market in events[1]['event']['children']), None)
            outcomes3 = next(((market['market']['children']) for market in events[2]['event']['children']), None)
            outcomes4 = next(((market['market']['children']) for market in events[3]['event']['children']), None)
            event_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            event2_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes2}
            event3_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes3}
            event4_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes4}
            # outcomeMeaningMinorCode: A - away, H - home, D - draw
            team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'))
            team2 = next((outcome['outcome']['name'] for outcome in outcomes2 if
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'))
            team3 = next((outcome['outcome']['name'] for outcome in outcomes3 if
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'))
            team4 = next((outcome['outcome']['name'] for outcome in outcomes4 if
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'))
            self.selection_ids = [event_selection_ids[team1], event2_selection_ids[team2],
                                  event3_selection_ids[team3], event4_selection_ids[team4]]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(cashout=False)
            event2 = self.ob_config.add_autotest_premier_league_football_event(cashout=False)
            event3 = self.ob_config.add_autotest_premier_league_football_event(cashout=False)
            event4 = self.ob_config.add_autotest_premier_league_football_event(cashout=False)
            self.selection_ids = [event.selection_ids[event.team1], event2.selection_ids[event2.team1],
                                  event3.selection_ids[event3.team1], event4.selection_ids[event4.team1]]
        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        if self.device_type == 'mobile':
            self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state(state_name='HomePage')

    def test_001_navigate_to_my_betsopen_betsverify_that_edit_my_betedit_my_acca_button_is_not_shown_for_the_bet(self):
        """
        DESCRIPTION: Navigate to My Bets>Open Bets
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is not shown for the bet
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is not shown
        """
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='"Bet types are not displayed"')
        bet = list(bets.values())[0]
        self.assertFalse(bet.has_edit_my_acca_button(),
                         msg='"Edit my bet" button is displayed')

    def test_002_navigate_to_my_betssettled_betsverify_that_edit_my_betedit_my_acca_button_is_not_shown_for_the_bet(self):
        """
        DESCRIPTION: Navigate to My Bets>Settled Bets
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is not shown for the bet
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is not shown
        """
        self.site.open_my_bets_settled_bets()
        bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='"Bet types are not displayed"')
        bet = list(bets.values())[0]
        self.assertFalse(bet.has_edit_my_acca_button(),
                         msg='"Edit my bet" button is displayed')
