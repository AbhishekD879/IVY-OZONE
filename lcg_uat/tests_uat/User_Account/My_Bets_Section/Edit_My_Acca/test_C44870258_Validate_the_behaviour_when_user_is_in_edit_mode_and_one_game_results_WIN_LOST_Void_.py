import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.acca
@pytest.mark.stg2
# @pytest.mark.prod -As bets needs to be settled, cannot script it on prod.
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870258_Validate_the_behaviour_when_user_is_in_edit_mode_and_one_game_results_WIN_LOST_Void_(BaseBetSlipTest):
    """
    TR_ID: C44870258
    NAME: Validate the behaviour when user is in edit mode and one game results (WIN/LOST/Void) )
    """
    keep_browser_open = True

    def test_000_preconditions(self, expected_betslip_counter_value=0):
        """
        PRECONDITIONS: Login with User
        PRECONDITIONS: User must have accumulator bets
        PRECONDITIONS: Navigate to My Bets > open bets
        """
        self.site.login()
        self.cms_config.set_my_acca_section_cms_status(ema_status='True')
        upcoming = self.get_date_time_formatted_string(hours=2)
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event(start_time=upcoming)
        self.__class__.event2 = self.ob_config.add_autotest_premier_league_football_event(start_time=upcoming)
        self.__class__.event3 = self.ob_config.add_autotest_premier_league_football_event(start_time=upcoming)
        self.__class__.event4 = self.ob_config.add_autotest_premier_league_football_event(start_time=upcoming)
        self.__class__.event5 = self.ob_config.add_autotest_premier_league_football_event(start_time=upcoming)
        self.selection_ids = [self.event.selection_ids[self.event.team1],
                              self.event2.selection_ids[self.event2.team1],
                              self.event3.selection_ids[self.event3.team1],
                              self.event4.selection_ids[self.event4.team1],
                              self.event5.selection_ids[self.event5.team1]]

        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()

        self.__class__.event_id = self.event.event_id
        self.__class__.event_name = '%s v %s' % (self.event.team1, self.event.team2)
        self.__class__.market_id = self.ob_config.market_ids[self.event.event_id][market_short_name]
        self.__class__.selection_id = self.event.selection_ids[self.event.team1]

        self.__class__.event2_id = self.event2.event_id
        self.__class__.market2_id = self.ob_config.market_ids[self.event2.event_id][market_short_name]
        self.__class__.selection2_id = self.event2.selection_ids[self.event2.team1]

        self.__class__.event3_id = self.event3.event_id

        self.__class__.event4_id = self.event4.event_id
        self.__class__.market4_id = self.ob_config.market_ids[self.event4.event_id][market_short_name]
        self.__class__.selection4_id = self.event4.selection_ids[self.event4.team1]

        self.__class__.expected_betslip_counter_value = expected_betslip_counter_value
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state(state_name='HomePage')
        self.site.open_my_bets_open_bets()

    def test_001_user_is_in_edit_modego_to_ti_and_set_win_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event(self):
        """
        DESCRIPTION: User is in EDIT MODE
        DESCRIPTION: Go to TI and set 'WIN' result for any event in the placed bet
        DESCRIPTION: Verify that 'Selection Removal' button is not shown for resulted event
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: WIN' label (green tick icon) is shown for resulted event
        EXPECTED: 'Selection Removal' button is NOT shown for resulted event
        EXPECTED: 'Selection Removal' button is shown and clickable for other events
        EXPECTED: 'CANCEL EDITING' button is shown and clickable
        EXPECTED: 'CONFIRM' button is shown and NOT clickable
        EXPECTED: Est. Returns are updated
        """
        _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type='ACCA (5)',
                                                                                        selection_ids=self.selection_ids)
        self.__class__.returns_before_settlement = self.bet.est_returns.value
        self.ob_config.update_selection_result(event_id=self.event_id, market_id=self.market_id,
                                               selection_id=self.selection_id, result='W')
        self.device.refresh_page()
        sleep(7)
        self.device.refresh_page()
        if self.device_type == 'desktop':
            self.site.open_my_bets_open_bets()
        _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type='ACCA (5)',
                                                                                        selection_ids=self.selection_ids)
        EMB_button = wait_for_result(lambda: self.bet.edit_my_acca_button,
                                     name=f'"{vec.ema.EDIT_MY_BET}" button will be displayed')
        self.assertTrue(EMB_button, msg=f'"{vec.ema.EDIT_MY_BET}" is not displayed')
        self.bet.edit_my_acca_button.click()
        sleep(5)
        selection = list(self.bet.items_as_ordered_dict.values())[0]
        self.assertTrue(selection.icon.is_displayed(), msg='"Green tick" icon is not displayed')
        self.assertFalse(selection.has_edit_my_acca_remove_icon(),
                         msg='"Selection removal icon(X)" is displayed')
        for selection in list(self.bet.items_as_ordered_dict.values())[1:5]:
            self.assertTrue(selection.edit_my_acca_remove_icon.is_displayed(),
                            msg='"Selection removal icon(X)" is not displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.ema.CANCEL.upper()}" button is not enabled')
        cancel_button_text = self.bet.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.ema.CANCEL.upper(),
                         msg=f'Actual Cancel button text: "{cancel_button_text}" is not same as Expected Cancel button text: "{vec.ema.CANCEL.upper()}"')
        self.assertFalse(self.bet.confirm_button.is_enabled(expected_result=False),
                         msg=f'"{vec.ema.CONFIRM_EDIT}" button is not clickable and displayed')
        returns_after_settlement = self.bet.est_returns.value
        self.assertNotEqual(returns_after_settlement, self.returns_before_settlement,
                            msg=f'Actual returns "{returns_after_settlement}" is same as Expected returns "{self.returns_before_settlement}"')

    def test_002_tap_selection_removal_button_for_any_other_selection_in_the_betverify_that_confirm_button_is_clickable_and_undo_button_is_shown_for_removed_selection(self):
        """
        DESCRIPTION: Tap 'Selection Removal' button for any other selection in the bet
        DESCRIPTION: Verify that 'CONFIRM' button is clickable and 'UNDO' button is shown for removed selection
        EXPECTED: 'UNDO' button is shown for removed selection
        EXPECTED: 'CONFIRM' button is shown and clickable
        """
        selection = list(self.bet.items_as_ordered_dict.values())[1]
        selection.edit_my_acca_remove_icon.click()
        self.assertTrue(selection.edit_my_acca_undo_icon.is_displayed(),
                        msg=f'"{vec.ema.UNDO_LEG_REMOVE.upper()}" button is not displayed')
        self.assertTrue(self.bet.confirm_button.is_enabled(), msg=f'"{vec.ema.CONFIRM_EDIT}" button is not enabled')

    def test_003_go_to_ti_and_set_lose_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event_and_error_message_is_displayed_your_acca_is_no_longer_active(self):
        """
        DESCRIPTION: Go to TI and set 'LOSE' result for any event in the placed bet
        DESCRIPTION: Verify that 'Selection Removal' button is not shown for resulted event and error message is displayed "Your Acca is no longer active
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: 'LOST' label (red cross icon) is shown for resulted event
        EXPECTED: 'Selection Removal' button is NOT shown for resulted event
        EXPECTED: 'Selection Removal' button is NOT shown for other events
        EXPECTED: Error message is displayed "Your Acca is no longer active"
        EXPECTED: 'CANCEL EDITING' button is shown and clickable
        EXPECTED: 'CONFIRM' button is shown and NOT clickable
        EXPECTED: NOTE: On Cash Out tab the bet will disappear after setting result
        """
        self.ob_config.update_selection_result(event_id=self.event2_id, market_id=self.market2_id,
                                               selection_id=self.selection2_id, result='L')
        sleep(7)
        self.device.refresh_page()
        if self.device_type == 'desktop':
            self.site.open_my_bets_open_bets()
        _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type='ACCA (5)',
                                                                                        selection_ids=self.selection_ids)
        self.bet.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(5)
        selection = list(self.bet.items_as_ordered_dict.values())[1]
        self.assertTrue(selection.icon.is_displayed(), msg='"Red cross" icon is not displayed')
        self.assertFalse(selection.has_edit_my_acca_remove_icon(),
                         msg='"Selection removal icon(X)" is still  displaying')
        for selection in list(self.bet.items_as_ordered_dict.values())[2:5]:
            self.assertFalse(selection.has_edit_my_acca_remove_icon(),
                             msg='"Selection removal icon(X)" is still  displaying')
        self.site.wait_splash_to_hide(3)
        error_message = self.bet.edit_my_acca_warning_message
        self.assertEqual(error_message, vec.ema.NO_ACTIVE_WARNING,
                         msg=f'Actual ACCA inactive message: "{error_message}" is not same as Expected ACCA inactive message: "{vec.ema.NO_ACTIVE_WARNING}"')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.ema.CANCEL.upper()}" button is not enabled')
        cancel_button_text = self.bet.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.ema.CANCEL.upper(),
                         msg=f'Actual Cancel button text: "{cancel_button_text}" is not same as Expected Cancel button text: "{vec.ema.CANCEL.upper()}"')
        self.assertFalse(self.bet.confirm_button.is_enabled(expected_result=False),
                         msg=f'"{vec.ema.CONFIRM_EDIT}" button displayed and clickable')

    def test_004_in_the_same_time_suspend_any_eventmarketselection_from_the_bet_in_tiverify_that_edit_mode_is_opened(self):
        """
        DESCRIPTION: In the same time suspend any event/market/selection from the bet in TI
        DESCRIPTION: Verify that edit mode is opened
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: 'SUSPENDED' label is displayed
        EXPECTED: Disabled 'Selection Removal' buttons for all selections
        EXPECTED: 'SUSP CONFIRM' button is disabled
        EXPECTED: 'CANCEL EDITING' is still displayed.
        """
        self.ob_config.change_event_state(event_id=self.event3_id, displayed=True, active=False)
        sleep(7)
        selection = list(self.bet.items_as_ordered_dict.values())[2]
        self.site.wait_splash_to_hide(7)
        self.assertTrue(selection.icon.is_displayed(), msg='"SUSP" label is not displayed')
        for selection in list(self.bet.items_as_ordered_dict.values()):
            self.assertFalse(selection.has_edit_my_acca_remove_icon(),
                             msg='"Selection removal icon(X)" is still  displaying')
        self.assertFalse(self.bet.confirm_button.is_enabled(expected_result=False),
                         msg=f'"{vec.ema.CONFIRM_SUSPENDED.upper()}" button is enabled')
        susp_confirm_text = self.bet.confirm_button.name
        self.assertEqual(susp_confirm_text, vec.ema.CONFIRM_SUSPENDED.upper(),
                         msg=f'Actual text: "{susp_confirm_text}" is not same as Expected text: "{vec.ema.CONFIRM_SUSPENDED.upper()}"')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.ema.CANCEL.upper()}" button is not in enabled state')
        cancel_button_text = self.bet.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.ema.CANCEL.upper(),
                         msg=f'Actual Cancel button text: "{cancel_button_text}" is not same as Expected Cancel button text: "{vec.ema.CANCEL.upper()}"')

    def test_005_go_to_ti_and_set_void_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event(self):
        """
        DESCRIPTION: Go to TI and set 'VOID' result for any event in the placed bet
        DESCRIPTION: Verify that 'Selection Removal' button is not shown for resulted event
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: 'VOID' label is shown for resulted event
        EXPECTED: 'Selection Removal' button is NOT shown for resulted event
        EXPECTED: 'Selection Removal' button is NOT shown and NOT clickable for other events
        EXPECTED: 'CANCEL EDITING' button is shown and clickable
        EXPECTED: 'CONFIRM' button is shown and NOT clickable
        EXPECTED: Est. Returns are updated
        """
        self.ob_config.update_selection_result(event_id=self.event4_id, market_id=self.market4_id,
                                               selection_id=self.selection4_id, result='V')
        for selection in list(self.bet.items_as_ordered_dict.values()):
            self.assertFalse(selection.has_edit_my_acca_remove_icon(),
                             msg='"Selection removal icon(X)" is displayed')
        selection = list(self.bet.items_as_ordered_dict.values())[3]
        self.site.wait_splash_to_hide(5)
        self.assertTrue(selection.icon.is_displayed(),
                        msg=f'"{vec.betslip.CANCELLED_STAKE.title()}" label is not displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.ema.CANCEL.upper()}" button is not enabled')
        self.assertFalse(self.bet.confirm_button.is_enabled(expected_result=False),
                         msg=f'"{vec.ema.CONFIRM_EDIT}" button is enabled')
        returns_after_settlement = self.bet.est_returns.value
        self.assertNotEqual(returns_after_settlement, self.returns_before_settlement,
                            msg=f'Actual returns "{returns_after_settlement}" is same as Expected returns "{self.returns_before_settlement}"')

    def test_006_verify_that_confirm_button_is_disabled(self):
        """
        DESCRIPTION: Verify that 'CONFIRM' button is disabled
        EXPECTED: CONFIRM button is disabled
        """
        self.assertFalse(self.bet.confirm_button.is_enabled(expected_result=False),
                         msg=f'"{vec.ema.CONFIRM_EDIT}" button is clickable')
