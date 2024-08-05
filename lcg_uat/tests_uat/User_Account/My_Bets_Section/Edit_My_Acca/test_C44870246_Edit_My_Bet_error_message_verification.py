from time import sleep
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec
from voltron.pages.shared.contents.my_bets.my_bets import MyBetsHeaderLine


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # suspending the events in ob, hence commented for pod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870246_Edit_My_Bet_error_message_verification(BaseBetSlipTest, MyBetsHeaderLine):
    """
    TR_ID: C44870246
    NAME: Edit My Bet error message verification
    DESCRIPTION:
    PRECONDITIONS: Login with User
    PRECONDITIONS: Navigate to My Bets > open bets
    PRECONDITIONS: Tap EDIT MY BET button
    """
    keep_browser_open = True
    bet_amount = 3

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Create events
        DESCRIPTION: 2. Login into App
        DESCRIPTION: 3. Place Multiple bet
        DESCRIPTION: 4. Navigate to the Bet History
        DESCRIPTION: 5. Go to 'Open Bets' tab -> verify that Edit My Bet button is available
        """
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event()
        event2 = self.ob_config.add_autotest_premier_league_football_event()
        event3 = self.ob_config.add_autotest_premier_league_football_event()
        event4 = self.ob_config.add_autotest_premier_league_football_event()
        self.selection_ids = [self.event.selection_ids[self.event.team1], event2.selection_ids[event2.team1],
                              event3.selection_ids[event3.team1], event4.selection_ids[event4.team1]]
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)
        self.open_betslip_with_selections(selection_ids=self.selection_ids, timeout=10)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state(state_name='HomePage')
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.bet_before_EMA = list(bets.values())[0]
        self.assertTrue(self.bet_before_EMA.has_edit_my_acca_button(),
                        msg='"Edit my bet" button is not displayed')
        self.__class__.bet_type_before_EMA = self.bet_before_EMA.bet_type
        self.__class__.stake_before_EMA = self.bet_before_EMA.stake.value
        self.__class__.est_returns_before_EMA = self.bet_before_EMA.est_returns.stake_value
        edit_my_bet_text = self.bet_before_EMA.edit_my_acca_button.name
        self.bet_before_EMA.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(3)
        cancel_button_text = self.bet_before_EMA.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.ema.CANCEL,
                         msg=f'actual text:"{edit_my_bet_text}" is not changed to Expected text:"{vec.ema.CANCEL}".')

    def test_001_remove_few_selections_from_the_bet(self):
        """
        DESCRIPTION: Remove few selections from the bet
        EXPECTED: 'UNDO' button is shown for removed selections
        EXPECTED: 'CONFIRM' button is shown and enabled
        EXPECTED: Stake and Est. Returns are updated
        """
        selections = self.bet_before_EMA.items_as_ordered_dict.values()
        selection = list(selections)[0]
        self.__class__.event_name = selection.event_name
        selection.edit_my_acca_remove_icon.click()
        self.assertTrue(wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(), timeout=3),
                        msg="undo button not displayed")
        self.assertTrue(self.bet_before_EMA.confirm_button.is_enabled(), msg='CONFIRM button is not enabled')
        self.__class__.confirm_button = self.bet_before_EMA.confirm_button.name
        _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type='ACCA (4)')
        self.assertTrue(self.bet.edit_my_acca_button.is_displayed(),
                        msg='Bet does not have My ACCA button on header')
        new_stake = self.bet.stake.value
        new_est_returns = self.bet.est_returns.stake_value
        self.assertNotEqual(self.stake_before_EMA, new_stake, msg='Stake is not updated')
        self.assertNotEqual(self.est_returns_before_EMA, new_est_returns, msg='Est. Returns is not updated')

    def test_002_provide_the_same_verification_on_my_bets__open_bets_tabverify_that_new_bet_is_not_placedverify_that_edit_mode_is_opened_with_an_error_message_and_removed_selections_are_remembered(self):
        """
        DESCRIPTION: Provide the same verification on My Bets > Open Bets tab
        DESCRIPTION: Verify that new bet is NOT placed;
        DESCRIPTION: Verify that edit mode is opened with an error message and removed selections are remembered
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: Error Message: "text from CMS"
        EXPECTED: 'SUSPENDED' label and disabled 'Selection Removal' button for suspended selections
        EXPECTED: Disabled 'Selection Removal' buttons for all other selections
        EXPECTED: Original Stake and Est. Returns
        EXPECTED: 'SUSP CONFIRM' button is disabled
        EXPECTED: 'CANCEL EDITING' is disabled
        """
        self.ob_config.change_event_state(event_id=self.event.event_id, displayed=True, active=False)
        self.assertTrue(self.bet.confirm_button.is_enabled(), msg='"Confirm" Button is not enabled')
        self.bet.confirm_button.click()
        self.assertTrue(self.bet.edit_my_acca_warning_message, vec.ema.SUSPENSION_WARNING)
        self.assertTrue(self.bet.confirm_button.name, vec.ema.CONFIRM_SUSPENDED.upper())
        sleep(7)
        selection = list(self.bet.items_as_ordered_dict.values())[0]
        self.site.wait_splash_to_hide(7)
        self.assertTrue(selection.icon.is_displayed(), msg='"SUSP" label is not displayed')
        bet_selections = list(self.bet.items_as_ordered_dict.values())
        for selection in bet_selections[1:]:
            self.assertTrue(selection.has_edit_my_acca_remove_icon(expected_result=False),
                            msg='"Selection removal icon(X)" is displayed')
        stake_after_confirm = self.bet.stake.value
        est_returns_after_confirm = self.bet.est_returns.stake_value
        self.assertNotEqual(self.stake_before_EMA, stake_after_confirm, msg='Stake is not updated')
        self.assertNotEqual(self.est_returns_before_EMA, est_returns_after_confirm, msg='Est. Returns is not updated')
        self.assertFalse(self.bet.confirm_button.is_enabled(), msg='CONFIRM button is enabled')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(), msg='CANCEL EDITING button is enabled')

    def test_003_verify_the_pop_up_msg(self):
        """
        DESCRIPTION: Verify the pop up msg
        EXPECTED: Leave the EMB page  before confirming EMB, pop up msg should be displayed.
        EXPECTED: Note: Do you want to cancel editing msg should be displayed.
        """
        self.device.driver.implicitly_wait(1)
        self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.LOTTO_TAB_NAME)
        if self.brand == 'bma':
            self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_DO_YOU_WANT_TO_CANCEL_EDITING.upper())
        else:
            self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_DO_YOU_WANT_TO_CANCEL_EDITING)
        self.assertTrue(self.dialog, msg='Cancel EDIT ACCA dialog is not present on page')
