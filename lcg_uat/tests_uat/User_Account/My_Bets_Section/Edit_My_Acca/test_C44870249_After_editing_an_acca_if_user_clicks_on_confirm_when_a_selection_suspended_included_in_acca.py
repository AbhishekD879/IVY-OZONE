import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from time import sleep


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.uat
# @pytest.mark.prod    ---> This TC works only in QA2 because it involves suspension of selection
@pytest.mark.medium
@pytest.mark.acca
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870249_After_editing_an_acca_if_user_clicks_on_confirm_when_a_selection_suspended_included_in_acca(BaseBetSlipTest):
    """
    TR_ID: C44870249
    NAME: "After editing an acca if user clicks on confirm when a selection suspended  included in acca
    """
    keep_browser_open = True
    bet_amount = 1

    def test_000_precondition(self):
        """
        PRECONDITIONS: Login with User and place a 4fold or 5fold acca bet
        PRECONDITIONS: Navigate to My Bets > open bets
        PRECONDITIONS: Tap EDIT MY BET button
        """
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event()
        event2 = self.ob_config.add_autotest_premier_league_football_event()
        event3 = self.ob_config.add_autotest_premier_league_football_event()
        event4 = self.ob_config.add_autotest_premier_league_football_event()
        self.selection_ids = [self.event.selection_ids[self.event.team1], event2.selection_ids[event2.team1],
                              event3.selection_ids[event3.team1], event4.selection_ids[event4.team1]]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.navigate_to_page('Homepage')
        self.site.wait_content_state(state_name='HomePage')
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No "Bets" are available')
        self.__class__.bet_before_EMA = list(bets.values())[0]
        self.assertTrue(self.bet_before_EMA.has_edit_my_acca_button(),
                        msg=f'"{vec.ema.EDIT_MY_BET}" button is not displayed')
        self.__class__.stake_before_EMA = self.bet_before_EMA.stake.value
        self.__class__.actual_potential_returns = self.bet_before_EMA.est_returns.stake_value
        edit_my_bet_text = self.bet_before_EMA.edit_my_acca_button.name
        self.bet_before_EMA.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(3)
        cancel_button_text = self.bet_before_EMA.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.EMA.CANCEL,
                         msg=f'actual text:"{edit_my_bet_text}" is not changed to Expected text:"{vec.EMA.CANCEL}".')

    def test_001_remove_few_selections_from_the_bet(self):
        """
        DESCRIPTION: Remove few selections from the bet
        EXPECTED: 'UNDO' button is shown for removed selections
        EXPECTED: 'CONFIRM' button is shown and enabled
        EXPECTED: Stake and Est. Returns are updated
        """
        selections = self.bet_before_EMA.items_as_ordered_dict
        self.assertTrue(selections, msg='No "Selections" are available')
        selection = list(selections.values())[0]
        selection.edit_my_acca_remove_icon.click()
        self.assertTrue(wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(), timeout=3),
                        msg=f'"{vec.ema.UNDO_LEG_REMOVE}" button not displayed')
        self.assertTrue(self.bet_before_EMA.edit_my_acca_button.is_displayed(),
                        msg=f'Bet does not have "{vec.ema.CANCEL}" button on header')
        self.__class__.stake_after_removal = self.bet_before_EMA.stake.value
        self.__class__.est_returns_after_removal = self.bet_before_EMA.est_returns.stake_value
        self.assertTrue(self.bet_before_EMA.confirm_button.is_enabled(), msg=f'"{vec.ema.CONFIRM_EDIT}" Button is not active')
        self.assertGreater(self.stake_before_EMA, self.stake_after_removal,
                           msg=f'Initial stake:"{self.stake_before_EMA}" is same as stake after removal of selection:"{self.stake_after_removal}".')
        self.assertGreater(self.actual_potential_returns, self.est_returns_after_removal,
                           msg=f'Initial Estimation Returns:"{self.stake_before_EMA}" is same as Estimation Returns after removal of selection:"{self.stake_after_removal}".')

    def test_002_suspend_any_eventmarketselectionin_acca_from_the_bet_in_tiverify_that_new_bet_is_not_placedverify_that_edit_mode_is_opened_with_an_error_message(self):
        """
        DESCRIPTION: Suspend any event/market/selection(in acca) from the bet in TI
        DESCRIPTION: Verify that new bet is NOT placed;
        DESCRIPTION: Verify that edit mode is opened with an error message
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: Error Message: "text from CMS"
        EXPECTED: 'SUSPENDED' label and disabled 'Selection Removal' button for suspended selections
        EXPECTED: Disabled 'Selection Removal' buttons for all selections
        EXPECTED: New Stake and New Est. Returns
        EXPECTED: 'CANCEL EDITING' is enabled and able to click
        """
        self.ob_config.change_event_state(event_id=self.event.event_id, displayed=True, active=False)
        sleep(5)
        selections = self.bet_before_EMA.items_as_ordered_dict
        self.assertTrue(selections, msg='No "Selections" are available')
        selection = list(selections.values())[0]
        self.assertTrue(selection.has_icon_status(), msg='"SUSP" label is not displayed for settled selection')
        actual_cms_error_message = self.bet_before_EMA.edit_my_acca_warning_message
        self.assertEqual(actual_cms_error_message, vec.EMA.SUSPENSION_WARNING,
                         msg=f'Actual error message: "{actual_cms_error_message}" is not same as Expected error message "{vec.EMA.SUSPENSION_WARNING}"')
        self.assertFalse(selection.has_edit_my_acca_remove_icon(),
                         msg='"Selection removal icon(X)" is still  displaying')
        for selection in list(self.bet_before_EMA.items_as_ordered_dict.values())[1:4]:
            self.assertTrue(selection.has_edit_my_acca_remove_icon(),
                            msg='"Selection removal icon(X)" is still  displaying')
        self.bet_before_EMA.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(3)
        stake_after_suspension = self.bet_before_EMA.stake.value
        est_returns_after_suspension = self.bet_before_EMA.est_returns.stake_value
        self.assertLess(self.stake_after_removal, stake_after_suspension,
                        msg=f'stake after removal of selection:"{self.stake_after_removal}" is same as stake after suspension:"{stake_after_suspension}".')
        self.assertLess(self.est_returns_after_removal, est_returns_after_suspension,
                        msg=f'est returns after removal of selection:"{self.est_returns_after_removal}" is same as est returns after suspension:"{est_returns_after_suspension}".')

    def test_003_verify_grey_suspended(self):
        """
        DESCRIPTION: Verify grey suspended
        EXPECTED: Edit My Acca button is not click-able when any selection is suspended
        """
        self.assertFalse(self.bet_before_EMA.edit_my_acca_button.is_enabled(), msg=f'"{vec.ema.EDIT_MY_BET}" Button is enabled')
