import pytest
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.acca
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870253_Verify_Display_of_Edited_Acca(BaseCashOutTest):
    """
    TR_ID: C44870253
    NAME: Verify Display of Edited Acca
    """
    keep_browser_open = True
    number_of_events = 4
    selection_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should be logged in
        PRECONDITIONS: User have 4 or 5+ accumulator bets.
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'),\
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)
            for event in events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                self.selection_ids.append(selection_id)
        else:
            event_params = self.create_several_autotest_premier_league_football_events(number_of_events=self.number_of_events)
            self.__class__.selection_ids = [list(event.selection_ids.values())[0] for event in event_params]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_my_bets__open_bets_tabverify_edit_my_bet_button(self):
        """
        DESCRIPTION: Navigate to My Bets > Open bets tab
        DESCRIPTION: Verify 'EDIT MY BET' button
        EXPECTED: EDIT MY BET button is displayed.
        """
        self.site.open_my_bets_open_bets()
        self.__class__.bet_before_EMB = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(self.bet_before_EMB, msg=f'"{self.bet_before_EMB}" is not displayed"')
        self.assertTrue(self.bet_before_EMB.edit_my_acca_button.is_displayed(),
                        msg=f'"{vec.ema.EDIT_MY_BET}" button is not displayed')
        self.__class__.cashout_button = self.bet_before_EMB.buttons_panel.full_cashout_button.label
        self.__class__.bet_type_before_EMB = self.bet_before_EMB.bet_type

    def test_002_tap_edit_my_bet_buttonverify_that_edit_mode_of_the_acca_is_open_and_cancel_editing_button_is_shown_instead_of_edit_my_bet_button(self):
        """
        DESCRIPTION: Tap EDIT My BET button
        DESCRIPTION: Verify that edit mode of the Acca is open and 'CANCEL EDITING' button is shown instead of 'EDIT MY BET' button
        EXPECTED: Edit mode of the ACCA is open
        EXPECTED: 'CANCEL EDITING' button is shown instead of EDIT MY BET button
        """
        self.bet_before_EMB.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(3)
        wait_for_result(lambda: self.bet_before_EMB.edit_my_acca_button.name,
                        name=f'"{vec.EMA.CANCEL}" to be displayed', timeout=30)
        cancel_button_text = self.bet_before_EMB.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.ema.CANCEL,
                         msg=f'Actual text:"{vec.ema.EDIT_MY_BET}" is not changed to Expected text:"{vec.ema.CANCEL}".')

    def test_003_select_the_selections_from_acca(self):
        """
        DESCRIPTION: select the selections from ACCA
        EXPECTED: cash out' button change as 'CONFIRM' and text display on the top of 'Confirm' button.
        EXPECTED: Undo button should be displayed when user select the selections.
        """
        selections = list(self.bet_before_EMB.items_as_ordered_dict.values())[0]
        self.assertTrue(selections, msg=f'{selections} are not displayed')
        selections.edit_my_acca_remove_icon.click()
        self.__class__.confirm_button = self.bet_before_EMB.confirm_button.name
        self.assertEqual(self.confirm_button, vec.ema.CONFIRM_EDIT.upper(),
                         msg=f'Actual text:"{self.cashout_button}" is not changed to Expected text:"{vec.ema.CONFIRM_EDIT.upper()}".')
        self.assertTrue(wait_for_result(lambda: selections.edit_my_acca_undo_icon.is_displayed(), timeout=3),
                        msg=f'"{vec.ema.UNDO_LEG_REMOVE}" not displayed')

    def test_004_tap_on_confirm_button(self):
        """
        DESCRIPTION: Tap on confirm button
        EXPECTED: confirm button changed to timer.
        EXPECTED: user has successfully edited their acca.
        """
        self.bet_before_EMB.confirm_button.click()
        self.assertEqual(self.cashout_button, vec.bet_history.CASH_OUT_TAB_NAME,
                         msg=f'Actual text:"{vec.bet_history.CASH_OUT_TAB_NAME}" is not changed to Expected text:"{vec.bet_history.CASH_OUT_TAB_NAME}".')
        bet_after_EMB = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(bet_after_EMB, msg=f'"{vec.ema.EDIT_MY_BET}" is not displayed')
        self.site.wait_splash_to_hide(3)
        EMA_success_msg = bet_after_EMB.cash_out_successful_message
        self.assertEqual(EMA_success_msg, vec.ema.EDIT_SUCCESS.caption,
                         msg=f'Actual message: {EMA_success_msg} '
                             f'is not the same as Expected message: {vec.ema.EDIT_SUCCESS.caption}')

    def test_005_navigate_to_settled_bets_tab(self):
        """
        DESCRIPTION: Navigate to settled bets tab
        EXPECTED: settled bets are displayed.
        """
        self.site.open_my_bets_settled_bets()
        self.assertTrue(self.site.bet_history.is_displayed(), msg=f'"{vec.bma.MY_ACC_BETHISTORY}" is not displayed')

    def test_006_verify_user_sees_view_of_an_edited_acca_in_settled_bet(self):
        """
        DESCRIPTION: "Verify user sees View of an edited acca in Settled bet"
        EXPECTED: Edited acca displayed when Acca has been edited.
        """
        self.__class__.bet_after_EMB = list(self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        bet_type_after_EMB = self.bet_after_EMB.bet_type
        self.assertEqual(bet_type_after_EMB, self.bet_type_before_EMB,
                         msg=f'Actual bet type "{self.bet_type_before_EMB}"  is not same as Expected bet type "{bet_type_after_EMB}"')
        status = self.bet_after_EMB.bet_status
        self.assertEqual(status, vec.Betslip.CASHOUT_STAKE,
                         msg=f'Actual status "{vec.Betslip.CASHOUT_STAKE}" is not same as Expected "{status}')

    def test_007_verify_user_sees_show_edit_history_listing_overlay_and_edited_acca_displayed(self):
        """
        DESCRIPTION: Verify user sees Show Edit History Listing Overlay and edited Acca displayed.
        EXPECTED: should be shown as per Time Order as they were Edited with below details
        EXPECTED: - Bet Type
        EXPECTED: - Original Bet / Edited Bet
        EXPECTED: - Date and Time when the bet was placed is displayed
        EXPECTED: Verify Original Bet / Edited Bet (Edit History Listing Page ),User should be able to see the bet as per below
        EXPECTED: - the selection name is displayed
        EXPECTED: - the market names are displayed
        EXPECTED: - the event name is displayed
        EXPECTED: - Event Date and Time is displayed
        EXPECTED: - Selection Price is displayed when bet was placed
        EXPECTED: - the returns status is displayed
        EXPECTED: - the total stake which was used at the time of bet placement
        EXPECTED: - Receipt ID is displayed
        EXPECTED: - Date and Time of bet placement is displayed
        EXPECTED: - Cashout History is displayed along with Stake Used and Cashed out value
        EXPECTED: - AND a message <Cashout Value> was used to Edit your bet should be
        """
        self.assertTrue(self.bet_after_EMB.show_edit_history_button, msg=f'"{vec.ema.HISTORY.show_history}" button is not present')
        self.bet_after_EMB.show_edit_history_button.click()
        if self.device_type == "mobile":
            handler = self.site.bet_history.edit_acca_history
        else:
            handler = self.site.dialog_manager.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_EDIT_ACCA_HISTORY)
        self.assertIsNotNone(handler, msg=f'"{vec.ema.HISTORY.acca_history}" pop-up is not present')
        bet = handler.content.headers.get(vec.bet_history._bet_types_ACC4.upper())
        self.assertTrue(bet.is_displayed(), msg=f'{bet} is not displayed')
        bet_type = bet.content.bet_type
        self.assertTrue(bet_type, msg=f'"{bet_type}" is not displayed')
        selections = bet.content.items_as_ordered_dict.values()
        for selection in list(selections):
            self.assertTrue(selection.event_name, msg=f'"{selection.event_name}" is not displayed')
            self.assertTrue(selection.market_name, msg=f'"{selection.market_name}" is not displayed')
            self.assertTrue(selection.outcome_name, msg=f'"{selection.outcome_name}" is not displayed')
            self.assertTrue(selection.odds_value, msg=f'"{selection.odds_value}" is not displayed')
            self.assertTrue(selection.event_time, msg=f'"{selection.event_time}" is not displayed')
        stake = bet.content.stake.value
        returns = bet.content.est_returns.value
        bet_receipt = bet.content.bet_receipt_info.bet_receipt.text
        bet_id = bet.content.bet_receipt_info.bet_id
        bet_date = bet.content.bet_receipt_info.date.text
        cashout_stake_used = bet.content.cash_out_history.stake_used.value
        cashout_value = bet.content.cash_out_history.cash_out.value
        cashout_used_message = bet.content.cash_out_history.cash_out_used_message
        self.assertTrue(stake, msg=f'"{stake} " is not displayed')
        self.assertTrue(returns, msg=f'"{returns} " is not displayed')
        self.assertTrue(bet_receipt, msg=f'"{bet_receipt}" is not displayed')
        self.assertTrue(bet_id, msg=f'"{bet_id}" is not displayed')
        self.assertTrue(bet_date, msg=f'"{bet_date}" is not displayed')
        self.assertTrue(cashout_stake_used, msg=f'"{cashout_stake_used}" is not displayed')
        self.assertTrue(cashout_value, msg=f'"{cashout_value}" is not displayed')
        self.assertTrue(cashout_used_message, msg=f'"{cashout_used_message}" is not displayed')
