import pytest
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870245_Verify_edited_ACCA_displayed_in_the_openbet(BaseBetSlipTest):
    """
    TR_ID: C44870245
    NAME: Verify edited ACCA displayed in the openbet.
    """
    keep_browser_open = True
    number_of_events = 4
    bet_amount = 5

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should be logged in
        PRECONDITIONS: User have placed a 4 fold or 5 fold accumulator bet.
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events,
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

    def test_001_navigate_to_my_bets__open_bets_tabverify_edit_my_bet_button(self):
        """
        DESCRIPTION: Navigate to My Bets > Open bets tab
        DESCRIPTION: Verify 'EDIT MY BET' button
        EXPECTED: EDIT MY BET button is displayed.
        """
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='"Bet types are not displayed"')
        self.__class__.bet_before_EMA = list(bets.values())[0]
        self.__class__.stake_before_EMA = self.bet_before_EMA.stake.value
        self.assertTrue(self.bet_before_EMA.edit_my_acca_button.is_displayed(),
                        msg='"Edit my bet" button is not displayed')
        self.__class__.cashout_button = self.bet_before_EMA.buttons_panel.full_cashout_button.label
        self.__class__.bet_type_before_EMA = self.bet_before_EMA.bet_type
        self.__class__.actual_potential_returns = self.bet_before_EMA.est_returns.value

    def test_002_tap_edit_my_bet_buttonverify_that_edit_mode_of_the_acca_is_open_and_cancel_editing_button_is_shown_instead_of_edit_my_bet_button(self):
        """
        DESCRIPTION: Tap EDIT My BET button
        DESCRIPTION: Verify that edit mode of the Acca is open and 'CANCEL EDITING' button is shown instead of 'EDIT MY BET' button
        EXPECTED: Edit mode of the ACCA is open
        EXPECTED: 'CANCEL EDITING' button is shown instead of EDIT MY BET button
        EXPECTED: cash out' button change as 'CONFIRM'  and text display on the top of 'Confirm' button.
        """
        edit_my_bet_text = self.bet_before_EMA.edit_my_acca_button.name
        self.assertEqual(edit_my_bet_text, vec.EMA.EDIT_MY_BET,
                         msg=f'Actual text:"{edit_my_bet_text}" is not same as Expected text:"{vec.EMA.EDIT_MY_BET}".')
        self.assertEqual(self.cashout_button, vec.bet_history.CASH_OUT_TAB_NAME, msg='"cash out button" is not displayed')
        self.bet_before_EMA.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(3)
        cancel_button_text = self.bet_before_EMA.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.EMA.CANCEL,
                         msg=f'Actual text:"{edit_my_bet_text}" is not changed to Expected text:"{vec.EMA.CANCEL}"')
        self.__class__.confirm_button = self.bet_before_EMA.confirm_button.name
        self.assertEqual(self.confirm_button, vec.EMA.CONFIRM_EDIT.upper(),
                         msg=f'Actual text:"{self.cashout_button}" is not changed to Expected text:"{vec.EMA.CONFIRM_EDIT.upper()}".')

    def test_003_select_the_selections_from_acca(self):
        """
        DESCRIPTION: select the selections from ACCA
        EXPECTED: Undo button should be displayed when user select the selections.
        """
        selection = list(self.bet_before_EMA.items_as_ordered_dict.values())[0]
        self.__class__.event_name = selection.event_name
        selection.edit_my_acca_remove_icon.click()
        self.assertTrue(wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(), timeout=3),
                        msg='"undo button" not displayed')

    def test_004_tap_on_confirm_button(self):
        """
        DESCRIPTION: Tap on confirm button
        EXPECTED: user has successfully edited their acca.
        """
        self.bet_before_EMA.confirm_button.click()
        new_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(new_bets, msg='"New bet" types are not displayed')
        self.__class__.bet_after_EMA = list(new_bets.values())[0]
        self.site.wait_splash_to_hide(3)
        EMA_success_msg = self.bet_after_EMA.cash_out_successful_message
        self.assertEqual(EMA_success_msg, vec.EMA.EDIT_SUCCESS.caption,
                         msg=f'Actual message: {EMA_success_msg} '
                             f'is not the same as Expected message: {vec.EMA.EDIT_SUCCESS.caption}')

    def test_005_verify_the_my_betsopen_bets_area_after_remove_the_selections(self):
        """
        DESCRIPTION: verify the my bets(open bets) area after remove the selections
        EXPECTED: The new bet type name is displayed.
        EXPECTED: The selection(s) which were removed have a Removed token displayed
        EXPECTED: Removed selections should appear below Open selections
        EXPECTED: The changed stake is displayed.
        EXPECTED: odds are displayed for any selection
        EXPECTED: The new potential returns are displayed
        """
        self.bet_type_after_EMA = self.bet_after_EMA.bet_type
        self.assertNotEqual(self.bet_type_after_EMA, self.bet_type_before_EMA,
                            msg='"New bet type" is  not changed')
        new_selections = self.bet_after_EMA.items_as_ordered_dict.values()
        new_selection = list(new_selections)[-1]
        self.assertTrue(new_selection.leg_remove_marker.is_displayed(),
                        msg=f'"Removed" text is not displayed')
        actual_event_name = new_selection.event_name
        self.assertEqual(actual_event_name, self.event_name,
                         msg='"Removed selection" went to last')
        self.assertTrue(new_selection.odds_value, msg='"Price" not displayed')
        self.site.wait_splash_to_hide(3)
        self.assertNotEqual(self.stake_before_EMA, self.bet_after_EMA.stake.value,
                            msg=f'stake :"{self.stake_before_EMA}" is same as New stake:"{self.bet_after_EMA.stake.value}".')
        new_potential_returns = self.bet_after_EMA.est_returns.value
        self.assertNotEqual(self.actual_potential_returns, new_potential_returns,
                            msg=f'Actual potential returns:"{self.actual_potential_returns}" is same as New potential returns:"{new_potential_returns}".')
