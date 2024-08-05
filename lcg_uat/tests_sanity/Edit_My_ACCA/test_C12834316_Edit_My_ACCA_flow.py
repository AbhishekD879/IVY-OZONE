import pytest
import tests
from time import sleep
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_prod  # EMA is NA for Coral prod, Applicable for other envs
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.sanity
@pytest.mark.bet_history_open_bets
@vtest
class Test_C12834316_Edit_My_ACCA_flow(BaseCashOutTest):
    """
    TR_ID: C12834316
    NAME: Edit My ACCA flow
    DESCRIPTION: This test case verifies that user can edit acca bet on My Bets>Cash out tab (Coral only) and Open Bets tab
    PRECONDITIONS: 1. Enable My ACCA feature toggle in CMS:
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 2. Login into App
    PRECONDITIONS: 3. Place single bet and multiple bet with more than 4 selection (e.g. ACCA 5) (selections should have cash out available)
    PRECONDITIONS: NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: Note: this test case should be run on 'Cash out' and on 'Open Bets' tabs
    """
    keep_browser_open = True
    number_of_events = 4
    event_names = []
    selection_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: EMA is enabled in CMS
        PRECONDITIONS: User should be logged in
        PRECONDITIONS: User have placed a 4 fold or 5 fold accumulator bet.
        """
        if tests.settings.backend_env == 'prod':
            edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
            self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in CMS')
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)
            for event in events:
                event_name = normalize_name(event['event']['name'])
                self.event_names.append(event_name)
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                self.selection_ids.append(selection_id)
        else:
            if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
                self.cms_config.set_my_acca_section_cms_status(ema_status=True)
            event_params = self.create_several_autotest_premier_league_football_events(number_of_events=self.number_of_events)
            for event in event_params:
                self.__class__.event_names = f'{event.team1} v {event.team2}'
            self.__class__.selection_ids = [list(event.selection_ids.values())[0] for event in event_params]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids[0])
        self.place_single_bet()
        self.site.bet_receipt.footer.click_done()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_my_bets__cashoutopen_bets_tab_for_coralopen_bets_tab_for_ladbrokesverify_that_edit_my_bet_for_coraledit_my_acca_for_ladbrokes_button_is_shown_only_for_multiple_bet_from_preconditions(self):
        """
        DESCRIPTION: Navigate to My Bets > Cashout/Open Bets tab (for Coral)/Open Bets tab (for Ladbrokes)
        DESCRIPTION: Verify that 'EDIT MY BET' (for Coral)/'EDIT MY ACCA' (for Ladbrokes) button is shown only for Multiple bet from preconditions
        EXPECTED: * 'EDIT MY BET' (for Coral)/'EDIT MY ACCA' (for Ladbroke button is shown only for Multiple bet
        EXPECTED: * Stake is shown
        EXPECTED: * Est. Returns is shown
        """
        self.site.open_my_bets_open_bets()
        _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
            event_names=self.event_names[0])
        self.assertFalse(bet.has_edit_my_acca_button(expected_result=False),
                         msg=f'"{vec.EMA.EDIT_MY_BET}" button is displayed')
        _, self.__class__.bet_before_EMA = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history._bet_types_ACC4.upper(),
            event_names=self.event_names)
        self.assertTrue(self.bet_before_EMA, msg=f' The bet : "{self.bet_before_EMA.bet_type}" is not displayed"')
        self.__class__.cashout_button = self.bet_before_EMA.buttons_panel.full_cashout_button.label
        self.__class__.actual_potential_returns = self.bet_before_EMA.est_returns.value
        stake_before_EMA = self.bet_before_EMA.stake.value
        self.assertTrue(self.bet_before_EMA.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(stake_before_EMA,
                        msg=f'The stake: "{stake_before_EMA}" is not displayed')
        self.assertTrue(self.actual_potential_returns,
                        msg=f'Potential returns: "{self.actual_potential_returns}" is not displayed')

    def test_002_tap_edit_my_bet_for_coraledit_my_acca_for_ladbrokes_buttonverify_that_edit_mode_of_the_acca_is_shown(self):
        """
        DESCRIPTION: Tap 'EDIT MY BET' (for Coral)/'EDIT MY ACCA' (for Ladbrokes) button
        DESCRIPTION: Verify that edit mode of the Acca is shown
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: * Selection details
        EXPECTED: * Event Name
        EXPECTED: * Event Time
        EXPECTED: * Scores (For Inplay Events)
        EXPECTED: * Winning / Losing Arrow (For Inplay Events)
        EXPECTED: * Selection removal button
        EXPECTED: * Message "Edit My Acca uses the cash out value of this bet and the latest odds of each selection" is shown as per design
        EXPECTED: * 'Cancel Editing' button
        EXPECTED: * 'CONFIRM' button is shown and is NOT be clickable
        EXPECTED: * 'Cash Out' button is NOT shown
        """
        self.bet_before_EMA.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(10)
        selections = self.bet_before_EMA.items_as_ordered_dict.values()
        for selection in list(selections):
            self.assertTrue(selection.has_edit_my_acca_remove_icon(), msg='"removal button" is not displayed')
            self.assertTrue(selection.event_name, msg=f'The event name: "{selection.event_name}" is not displayed')
            self.assertTrue(selection.outcome_name, msg=f'The outcome name: "{selection.outcome_name}" is not displayed')
            self.assertTrue(selection.odds_value, msg=f'The odd: "{selection.odds_value}" is not displayed')
            self.assertTrue(selection.event_time, msg=f'The event time: "{selection.event_time}" is not displayed')
        cancel_button_text = self.bet_before_EMA.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.EMA.CANCEL,
                         msg=f'Actual text:"{vec.EMA.EDIT_MY_BET}" is not changed to Expected text:"{vec.EMA.CANCEL}".')
        edit_warning_msg = self.bet_before_EMA.edit_my_acca_warning_message
        self.assertEqual(edit_warning_msg, vec.ema.EDIT_WARNING,
                         msg=f'Actual message: "{edit_warning_msg}" is not the same as Expected message: "{vec.ema.EDIT_WARNING}"')
        self.assertFalse(self.bet_before_EMA.confirm_button.is_enabled(expected_result=False),
                         msg=f'"{vec.ema.CONFIRM_EDIT}" button is not clickable and displayed')
        self.assertFalse(self.bet_before_EMA.has_buttons_panel(expected_result=False), msg=f'"{self.bet_before_EMA.has_buttons_panel()}" is displayed')

    def test_003_tap_selection_removal_button_for_any_selectionverify_that_selection_removal_button_is_no_longer_displayed_adjacent_to_the_removed_selection(self):
        """
        DESCRIPTION: Tap 'Selection Removal' button for any selection
        DESCRIPTION: Verify that 'Selection Removal' button is no longer displayed adjacent to the removed selection
        EXPECTED: * 'Selection Removal' button is no longer displayed adjacent to the removed selection
        EXPECTED: * 'Selection Removal' buttons remain displayed adjacent to all other open selections
        EXPECTED: * 'UNDO' button displayed adjacent to the removed selection
        EXPECTED: * 'REMOVED' label for the removed selection
        EXPECTED: * Updated potential returns are displayed
        """
        self.__class__.selections = self.bet_before_EMA.items_as_ordered_dict.values()
        self.assertTrue(self.selections, msg=f'Selections: "{self.selections}"not displayed')
        self.__class__.selection = list(self.selections)[0]
        self.__class__.event_name = self.selection.event_name
        self.selection.edit_my_acca_remove_icon.click()
        result = wait_for_result(lambda: self.selection.edit_my_acca_undo_icon.is_displayed(),
                                 name='"UNDO button" to be displayed', timeout=60)
        self.assertTrue(result,
                        msg='"UNDO button" is not displayed when the user clicks on the "Selection removal icon(X)"')
        self.assertTrue(self.selection.leg_remove_marker.is_displayed(), msg='"REMOVED" icon is not displayed')
        self.assertFalse(self.selection.has_edit_my_acca_remove_icon(), msg='"Selection removal icon(X)" is still displayed"')
        for selection in list(self.selections)[1:]:
            self.assertTrue(selection.has_edit_my_acca_remove_icon(), msg='"Selection removal icon(X)" is not displayed"')
        self.__class__.potential_returns = self.bet_before_EMA.est_returns.value
        self.assertNotEqual(self.potential_returns, self.actual_potential_returns,
                            msg=f'"{self.potential_returns}" is same as "{self.actual_potential_returns}"')

    def test_004_tap_on_cancel_editing_buttonverify_that_cancel_popup_is_not_shown(self):
        """
        DESCRIPTION: Tap on 'Cancel Editing' button
        DESCRIPTION: Verify that 'Cancel' popup is not shown
        EXPECTED: * Cancel message is not shown.
        EXPECTED: * Removed selection is restored.
        EXPECTED: * User is on Openbet /Cashout Tab
        """
        self.bet_before_EMA.edit_my_acca_button.click()
        sleep(1)
        result = wait_for_result(lambda: self.bet_before_EMA.edit_my_acca_warning_message, timeout=60, name=f'"{vec.ema.EDIT_WARNING}" not to be displayed')
        self.assertFalse(result, msg=f'"{vec.ema.EDIT_WARNING}" is still displayed')
        new_selection = list(self.bet_before_EMA.items_as_ordered_dict.values())[0]
        new_selection_event_name = new_selection.event_name
        self.assertEqual(new_selection_event_name, self.event_name,
                         msg=f'"Actual event name {new_selection_event_name}" is not same as Expected event name "{self.event_name}"')
        if self.device_type == 'mobile':
            current_tab_name = self.site.open_bets.tabs_menu.current
        else:
            current_tab_name = self.site.betslip.tabs_menu.current
        self.assertEqual(current_tab_name, vec.BetHistory.OPEN_BETS_TAB_NAME,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{vec.BetHistory.OPEN_BETS_TAB_NAME}".')

    def test_005_tap_edit_my_bet_for_coraledit_my_acca_for_ladbrokes_button_and_tap_selection_removal_button_for_more_than_one_selectionverify_that_selection_removal_button_is_no_longer_displayed_adjacent_to_the_removed_selection(self):
        """
        DESCRIPTION: Tap 'EDIT MY BET' (for Coral)/'EDIT MY ACCA' (for Ladbrokes) button and Tap 'Selection Removal' button for more than one selection
        DESCRIPTION: Verify that 'Selection Removal' button is no longer displayed adjacent to the removed selection
        EXPECTED: * 'Selection Removal' button is no longer displayed adjacent to the removed selections
        EXPECTED: * 'Selection Removal' buttons remain displayed adjacent to all other open selections
        EXPECTED: * 'UNDO' button displayed adjacent to the removed selections
        EXPECTED: * 'REMOVED' label for the removed selections
        """
        self.test_002_tap_edit_my_bet_for_coraledit_my_acca_for_ladbrokes_buttonverify_that_edit_mode_of_the_acca_is_shown()
        self.test_003_tap_selection_removal_button_for_any_selectionverify_that_selection_removal_button_is_no_longer_displayed_adjacent_to_the_removed_selection()

    def test_006_click_on_the_selection_undo_button(self):
        """
        DESCRIPTION: Click on the Selection 'Undo' button
        EXPECTED: * The removed selection is re-displayed
        EXPECTED: * The Selection Removal button is re-displayed adjacent to the selection
        EXPECTED: * Updated potential returns are displayed
        """
        self.selection.edit_my_acca_undo_icon.click()
        result = wait_for_result(lambda: self.selection.edit_my_acca_remove_icon.is_displayed(),
                                 name='"UNDO button" to be displayed', timeout=40)
        self.assertTrue(result,
                        msg='"Selection removal icon(X)" is not displayed when the user clicks on the "UNDO button"')
        self.selection.edit_my_acca_remove_icon.click()

    def test_007_click_the_confirm_buttonverify_that_new_bet_is_placed_on_all_open_remaining_selections_at_their_current_price_spot_price_simultaneously(self):
        """
        DESCRIPTION: Click the 'Confirm' button
        DESCRIPTION: Verify that new bet is placed on all open remaining selections at their current price (spot price) simultaneously
        EXPECTED: * New bet is placed on all open remaining selections at their current price (spot price) simultaneously
        EXPECTED: * NO funds are sent or requested from the users account
        EXPECTED: * message is shown confirming that the edit was successful: "ACCA edited successfully" (Green tick message under cash-out buttin)
        """
        confirm_button = self.bet_before_EMA.confirm_button.name
        self.assertEqual(confirm_button, vec.EMA.CONFIRM_EDIT.upper(),
                         msg=f'Actual text:"{self.cashout_button}" is not changed to Expected text:"{vec.EMA.CONFIRM_EDIT.upper()}".')
        sleep(4)
        self.bet_before_EMA.confirm_button.click()
        self.assertEqual(self.cashout_button, vec.bet_history.CASH_OUT_TAB_NAME,
                         msg=f'Actual text:"{vec.bet_history.CASH_OUT_TAB_NAME}" is not changed to Expected text:"{vec.bet_history.CASH_OUT_TAB_NAME}".')
        _, self.__class__.bet_after_EMA = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history._bet_types_TBL.upper(),
            event_names=self.event_names)
        self.assertTrue(self.bet_after_EMA, msg=f'"{vec.EMA.EDIT_MY_BET}" is not displayed')
        potential_returns = self.bet_after_EMA.est_returns.value
        self.assertEqual(potential_returns, self.potential_returns,
                         msg=f'Actual returns: "{potential_returns}" is not same as Expected returns: "{self.potential_returns}"')

        # TODO for Ladbrokes as it is taking time to reflect on jenkins
        if self.brand == 'bma':
            EMA_success_msg = self.bet_after_EMA.cash_out_successful_message
            self.assertEqual(EMA_success_msg, vec.EMA.EDIT_SUCCESS.caption,
                             msg=f'Actual message: "{EMA_success_msg}" is not the same as Expected message: "{vec.EMA.EDIT_SUCCESS.caption}"')

    def test_008_verify_that_new_bet_type_is_shownin_case_the_bet_was_acca4_and_you_removed_1_selection___the_new_bet_type_is_treble(self):
        """
        DESCRIPTION: Verify that new bet type is shown
        DESCRIPTION: (in case the bet was ACCA4 and you removed 1 selection - the new bet type is treble)
        EXPECTED: New bet type is shown
        """
        bet_type_after_EMA = self.bet_after_EMA.bet_type
        self.assertEqual(bet_type_after_EMA, vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE.upper(),
                         msg=f'Actual  bet type: "{bet_type_after_EMA}" is same as Expected bet type: "{vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE.upper()}"')

    def test_009_verify_that_removed_bet_is_shown(self):
        """
        DESCRIPTION: Verify that Removed bet is shown
        EXPECTED: * Removed bet is shown on 'Open Bets' tab
        EXPECTED: * Removed bet is NOT shown on 'Cashout' tab (for Coral only)
        """
        new_selection = list(self.bet_after_EMA.items_as_ordered_dict.values())[-1]
        self.assertTrue(new_selection.leg_remove_marker.is_displayed(),
                        msg=f'"{new_selection.leg_remove_marker}" is not displayed')
        if self.brand == 'bma':
            if self.device_type == 'mobile':
                self.site.open_bets.tabs_menu.items_as_ordered_dict.get('CASH OUT').click()
                self.site.wait_splash_to_hide(timeout=30)
                bet_after_EMA = list(self.site.cashout.tab_content.accordions_list.items_as_ordered_dict.values())[0]
            else:
                self.site.betslip.tabs_menu.items_as_ordered_dict.get('CASH OUT').click()
                self.site.wait_splash_to_hide(timeout=30)
                bet_after_EMA = list(self.site.cashout.tab_content.accordions_list.items_as_ordered_dict.values())[0]
            new_selection = bet_after_EMA.items_as_ordered_dict.values()
            self.assertNotEqual(len(new_selection), len(self.selections),
                                msg=f'"Actual length: {len(new_selection)}" is same as Expected length: "{len(self.selections)}"')
            if self.device_type == 'mobile':
                self.site.cashout.tabs_menu.items_as_ordered_dict.get('OPEN BETS').click()
            else:
                self.site.betslip.tabs_menu.items_as_ordered_dict.get('OPEN BETS').click()

    def test_010_tap_edit_my_acca_button_one_more_timetap_selection_removal_buttons_to_leave_just_one_selection_in_the_betverify_that_the_selection_removal_button_is_not_shown_for_last_selection_is_the_bet(self):
        """
        DESCRIPTION: Tap 'Edit My Acca' button one more time
        DESCRIPTION: Tap 'Selection Removal' buttons to leave just one selection in the bet
        DESCRIPTION: Verify that the 'Selection Removal' button is not shown for last selection is the bet
        EXPECTED: 'Selection Removal' button is not shown for last selection is the bet
        """
        _, bet_after_EMA = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=vec.bet_history._bet_types_TBL.upper(),
                                                                                   event_names=self.event_names)
        bet_after_EMA.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(5)
        self.__class__.selections = bet_after_EMA.items_as_ordered_dict.values()
        self.assertTrue(self.selections, msg=f'"{self.selections}"not displayed')
        for selection in list(self.selections)[:2]:
            selection.edit_my_acca_remove_icon.click()
            result = wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(),
                                     name='"UNDO button" to be displayed', timeout=30)
            self.assertTrue(result,
                            msg='"UNDO button" is not displayed when the user clicks on the "Selection removal icon(X)"')
        for selection in list(self.selections)[2:3]:
            self.assertFalse(selection.edit_my_acca_remove_icon.click(),
                             msg='"Last Open Selection" is still in clickable state')
            self.assertTrue(selection.edit_my_acca_remove_icon.is_displayed(), msg='"UNDO button" is not displayed')

    def test_011_confirm_edittingverify_that_edit_my_bet_for_coraledit_my_acca_for_ladbrokes_button_is_not_shown_any_more_for_this_bet(self):
        """
        DESCRIPTION: Confirm editting
        DESCRIPTION: Verify that 'EDIT MY BET' (for Coral)/'EDIT MY ACCA' (for Ladbrokes) button is not shown any more for this bet
        EXPECTED: * 'EDIT MY BET' (for Coral)/'EDIT MY ACCA' (for Ladbrokes) button is not shown
        EXPECTED: * 'Single' bet type is shown for the bet
        """
        _, bet_after_EMA = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history._bet_types_TBL.upper(),
            event_names=self.event_names)
        bet_after_EMA.confirm_button.click()
        _, bet_after_EMA = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.betslip.BETSLIP_SINGLES_NAME.upper(),
            event_names=self.event_names)
        self.assertEqual(bet_after_EMA.bet_type, vec.betslip.BETSLIP_SINGLES_NAME.upper(), msg=f'Actual bet type "{bet_after_EMA.bet_type}" is not same as Expected bet type"{vec.betslip.BETSLIP_SINGLES_NAME.upper()}"')
        result = wait_for_result(lambda: bet_after_EMA.has_edit_my_acca_button, timeout=60,
                                 name=f'"{vec.EMA.EDIT_MY_BET}" is not be displayed')
        self.assertFalse(result(expected_result=False), msg=f'"{vec.EMA.EDIT_MY_BET}" is displayed')
