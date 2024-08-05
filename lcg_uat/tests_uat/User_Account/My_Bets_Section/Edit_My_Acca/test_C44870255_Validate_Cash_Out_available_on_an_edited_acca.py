import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870255_Validate_Cash_Out_available_on_an_edited_acca(BaseBetSlipTest):
    """
    TR_ID: C44870255
    NAME: Validate  Cash Out available on an edited acca
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User is logged in
        PRECONDITIONS: User have accumulator bets on my bets area
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=4,
                                                         is_live=True)
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
            event = self.ob_config.add_autotest_premier_league_football_event()
            event2 = self.ob_config.add_autotest_premier_league_football_event()
            event3 = self.ob_config.add_autotest_premier_league_football_event()
            event4 = self.ob_config.add_autotest_premier_league_football_event()
            self.selection_ids = [event.selection_ids[event.team1], event2.selection_ids[event2.team1],
                                  event3.selection_ids[event3.team1], event4.selection_ids[event4.team1]]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.close_button.click()
        self.site.wait_content_state(state_name='HomePage')

    def test_001_navigate_to_my_bets_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to My bets-open bets tab
        EXPECTED: Cash out option should be available for EMA
        """
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='"Bet types are not displayed"')
        self.__class__.bet_before_EMA = list(bets.values())[0]
        cashout_button = self.bet_before_EMA.buttons_panel.full_cashout_button.label
        self.assertEqual(cashout_button, vec.BetHistory.CASH_OUT_TAB_NAME,
                         msg=f'Actual text: {cashout_button} is not same as'
                             f'Expected text: {vec.BetHistory.CASH_OUT_TAB_NAME}')

    def test_002_tap_cash_out_buttonverify_that_confirm_cash_out_shown_and_enabledand_edit_my_bet_button_should_be_displayed(self):
        """
        DESCRIPTION: Tap 'Cash Out' button
        DESCRIPTION: Verify that 'Confirm Cash Out' shown and enabled
        DESCRIPTION: and 'EDIT MY BET' button should be displayed
        EXPECTED: 'Confirm Cash Out' button is shown and enabled
        EXPECTED: Confirm Cash Out' button is flashing 3 times
        EXPECTED: 'EDIT MY Bet' button is should display
        Note: colours flashing is not automated
        """
        self.bet_before_EMA.buttons_panel.full_cashout_button.click()
        self.site.contents.scroll_to_top()
        self.device.driver.implicitly_wait(5)
        self.assertTrue(self.bet_before_EMA.edit_my_acca_button.is_displayed(),
                        msg='"Edit my bet" button is not displayed')
