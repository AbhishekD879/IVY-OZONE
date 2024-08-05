import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't change the status of selections
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.acca
@vtest
class Test_C9346555_Verify_the_flow_when_the_game_result_VOID(BaseBetSlipTest):
    """
    TR_ID: C9346555
    NAME: Verify the flow when the game result VOID
    DESCRIPTION: This test case verifies that the flow for EMA edit mode when game result VOID
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Place a bet on TREBLE or more (All selections in the placed bet are active and open)
    PRECONDITIONS: Go To My Bets>Cash Out / Open Bets
    PRECONDITIONS: Tap 'EDIT MY ACCA' button for placed bet
    PRECONDITIONS: Test case should be run on Cash out tab and on Open Bets tab
    PRECONDITIONS: NOTE: VOID result should be set to the appropriate selection in the bet
    """
    keep_browser_open = True

    def get_bets(self, open_bets=True):
        if open_bets:
            self.site.open_my_bets_open_bets()
            _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history._bet_types_ACC4.upper(),
                selection_ids=self.selection_ids)
        else:
            self.site.open_my_bets_cashout()
            _, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history._bet_types_ACC4.upper(),
                selection_ids=self.selection_ids)

    def test_000_preconditions(self):
        """
        event creation
        """
        edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
        if not edit_my_acca_status:
            self.cms_config.set_my_acca_section_cms_status(ema_status=True)
            self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in CMS')
        upcoming = self.get_date_time_formatted_string(hours=2)
        event = self.ob_config.add_autotest_premier_league_football_event(start_time=upcoming)
        event2 = self.ob_config.add_autotest_premier_league_football_event(start_time=upcoming)
        event3 = self.ob_config.add_autotest_premier_league_football_event(start_time=upcoming)
        event4 = self.ob_config.add_autotest_premier_league_football_event(start_time=upcoming)
        self.selection_ids = [event.selection_ids[event.team1],
                              event2.selection_ids[event2.team1],
                              event3.selection_ids[event3.team1],
                              event4.selection_ids[event4.team1]]

        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()

        self.__class__.event_id = event.event_id
        self.__class__.market_id = self.ob_config.market_ids[event.event_id][market_short_name]
        self.__class__.selection_id = event.selection_ids[event.team1]
        self.site.login()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state(state_name='HomePage')

    def test_001_go_to_ti_and_set_void_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event(self, open_bets=True):
        """
        DESCRIPTION: Go to TI and set 'VOID' result for any event in the placed bet
        DESCRIPTION: Verify that 'Selection Removal' button is not shown for resulted event
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: - 'VOID' label is shown for resulted event
        EXPECTED: - 'Selection Removal' button is NOT shown for resulted event
        EXPECTED: - 'Selection Removal' button is shown and clickable for other events
        EXPECTED: - 'CANCEL EDITING' button is shown and clickable
        EXPECTED: - 'CONFIRM' button is shown and NOT clickable
        EXPECTED: - Est. Returns are updated
        """
        self.get_bets(open_bets=open_bets)
        self.__class__.returns_before_settlement = self.bet.est_returns.value
        EMB_button = wait_for_result(lambda: self.bet.edit_my_acca_button,
                                     name=f'"{vec.ema.EDIT_MY_BET}" button will be displayed')
        self.assertTrue(EMB_button, msg=f'"{vec.ema.EDIT_MY_BET}" is not displayed')
        self.bet.edit_my_acca_button.click()
        self.ob_config.update_selection_result(event_id=self.event_id, market_id=self.market_id,
                                               selection_id=self.selection_id, result='V')
        sleep(7)
        self.device.refresh_page()
        self.get_bets(open_bets=open_bets)
        self.bet.edit_my_acca_button.click()
        for selection in list(self.bet.items_as_ordered_dict.values())[1:]:
            self.assertTrue(selection.has_edit_my_acca_remove_icon(),
                            msg='"Selection removal icon(X)" is not displayed')
        selection = list(self.bet.items_as_ordered_dict.values())[0]
        self.site.wait_splash_to_hide(5)
        self.assertTrue(selection.icon.is_displayed(),
                        msg=f'Void label "{vec.betslip.CANCELLED_STAKE.title()}" is not displayed')
        self.assertFalse(selection.has_edit_my_acca_remove_icon(expected_result=False),
                         msg='"Selection removal icon(X)" is displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.ema.CANCEL.upper()}" button is not enabled')
        self.assertFalse(self.bet.confirm_button.is_enabled(expected_result=False),
                         msg=f'"{vec.ema.CONFIRM_EDIT}" button is enabled')
        returns_after_settlement = self.bet.est_returns.value
        self.assertNotEqual(returns_after_settlement, self.returns_before_settlement,
                            msg=f'Returns after settlement "{returns_after_settlement}" is still same as Returns before settlement "{self.returns_before_settlement}"')
        selection = list(self.bet.items_as_ordered_dict.values())[1]
        selection.edit_my_acca_remove_icon.click()
        self.site.wait_splash_to_hide(5)
        result = wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(),
                                 name='"UNDO button" to be displayed', timeout=10)
        self.assertTrue(result,
                        msg='"UNDO button" is not displayed when the user clicks on the "Selection removal icon(X)"')
        self.assertTrue(self.bet.confirm_button.is_enabled(),
                        msg=f'"{vec.ema.CONFIRM_EDIT}" button is not clickable')

    def test_002_tap_selection_removal_button_for_any_other_selection_in_the_betverify_that_confirm_button_is_clickable_and_undo_button_is_shown_for_removed_selection(self):
        """
        DESCRIPTION: Tap 'Selection Removal' button for any other selection in the bet
        DESCRIPTION: Verify that 'CONFIRM' button is clickable and 'UNDO' button is shown for removed selection
        EXPECTED: - 'UNDO' button is shown for removed selection
        EXPECTED: - 'CONFIRM' button is shown and clickable
        """
        # this step is already covered in step 1 and same functionality covered for cashout tab in this step

        if self.brand == 'bma':
            self.bet.edit_my_acca_button.click()
            self.test_001_go_to_ti_and_set_void_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event(open_bets=False)
