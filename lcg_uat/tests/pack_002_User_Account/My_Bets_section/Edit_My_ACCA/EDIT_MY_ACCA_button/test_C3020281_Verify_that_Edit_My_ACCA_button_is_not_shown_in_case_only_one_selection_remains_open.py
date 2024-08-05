import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod     //can't create events
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.acca
@pytest.mark.betslip
@vtest
class Test_C3020281_Verify_that_Edit_My_ACCA_button_is_not_shown_in_case_only_one_selection_remains_open(BaseCashOutTest):
    """
    TR_ID: C3020281
    NAME: Verify that 'Edit My ACCA' button is not shown in case only one selection remains open
    DESCRIPTION: This test case verifies that 'EDIT MY ACCA' button is NOT displaying when the bet on an ACCA is placed and only one selection remains open
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add 3 (three) selections to Betslip and place a bet on TREBLE and SINGLES
    PRECONDITIONS: All selections in the placed bet are active
    PRECONDITIONS: All selections in the placed bet are open
    PRECONDITIONS: NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: **Ladbrokes** has 'EDIT MY ACCA' button
    PRECONDITIONS: **Coral** has 'EDIT MY BET' button
    """
    keep_browser_open = True

    def get_bet_with_my_acca_edit(self, bet_type, event_name, open_bets=True):
        """
        Get bet with My ACCA edit functionality
        """
        if open_bets:
            _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=bet_type, event_names=event_name, number_of_bets=2)
        else:
            _, bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type=bet_type, event_names=event_name,
                number_of_bets=2)
        self.assertTrue(bet, msg=f'Cannot find bet for "{event_name}"')
        return bet

    def test_000_precondition(self):
        self.__class__.event_params = self.create_several_autotest_premier_league_football_events(number_of_events=3)
        selection_ids = [self.event_params[0].selection_ids, self.event_params[1].selection_ids,
                         self.event_params[2].selection_ids]
        self.__class__.selection_name = self.event_params[0].team1
        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=[list(i.values())[0] for i in selection_ids])
        sections = self.get_betslip_sections(multiples=True)
        single_selection = sections.Singles[self.selection_name]
        single_selection.amount_form.enter_amount('0.5')
        multiple_section = sections.Multiples[vec.betslip.TBL]
        multiple_section.amount_form.enter_amount('0.9')
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        if self.device_type == 'mobile':
            self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_my_bets__cashoutverify_that_edit_my_betedit_my_acca_button_is_shown_for_treble_only(self):
        """
        DESCRIPTION: Navigate to My Bets > Cashout
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown for TREBLE only
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is shown only for TREBLE bet
        EXPECTED: - Stake is shown
        EXPECTED: - Est. Returns ( **Coral** )/ Potential Returns ( **Ladbrokes** ) is shown
        """
        self.site.open_my_bets_cashout()
        open_bets = False if self.brand == 'bma' else True
        self.__class__.bet = self.get_bet_with_my_acca_edit(bet_type=vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE,
                                                            event_name=self.event_params[0].event_name,
                                                            open_bets=open_bets)
        single_bet = self.get_bet_with_my_acca_edit(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
            event_name=self.event_params[0].event_name, open_bets=open_bets)

        self.assertFalse(single_bet.has_edit_my_acca_button(),
                         msg=f'Bet have My ACCA button on header')
        self.assertTrue(self.bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')
        self.assertEqual(self.bet.edit_my_acca_button.name, vec.ema.EDIT_MY_BET,
                         msg=f'"{vec.ema.EDIT_MY_BET}" button has incorrect name')
        self.__class__.est_returns_value = self.bet.est_returns.stake_value
        self.assertTrue(self.bet.est_returns.is_displayed(), msg="est returns value is not displayed")
        self.__class__.stake_value = self.bet.stake.stake_value
        self.assertTrue(self.bet.stake.is_displayed(), msg="stake value is not displayed")

    def test_002_click_on_edit_my_betedit_my_acca_buttondelete_one_of_the_selections_and_confirm_changes_or_add_a_result_in_tinavigate_back_to_my_bets__cashoutverify_that_edit_my_betedit_my_acca_button_is_shown_for_double_only(
            self):
        """
        DESCRIPTION: Click on 'EDIT MY BET/EDIT MY ACCA' button
        DESCRIPTION: Delete one of the selections and confirm changes OR add a result in TI
        DESCRIPTION: Navigate back to My Bets > Cashout
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown for DOUBLE only
        EXPECTED: - Two selections remained in edited ACCA
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE bet
        EXPECTED: - New Stake is shown
        EXPECTED: - New Est. Returns ( **Coral** )/New Potential Returns ( **Ladbrokes** ) is shown
        """
        self.bet.edit_my_acca_button.click()
        selection = self.bet.items[0]
        self.assertTrue(selection.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')
        selection.edit_my_acca_remove_icon.click()
        self.assertTrue(wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(), timeout=3),
                        msg='"undo button" not displayed')
        confirm_button = self.bet.confirm_button.name
        self.assertEqual(confirm_button, vec.ema.CONFIRM_EDIT.upper(),
                         msg=f'Actual text:"{confirm_button}" is not same as Expected text:"{vec.ema.CONFIRM_EDIT.upper()}".')
        self.bet.confirm_button.click()
        _, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE', event_names=self.event_params[0].event_name,
            raise_exceptions=False, number_of_bets=2)
        self.assertFalse(bet, msg=f'Bet for "{self.event_params[0].event_name}" still exists')
        self.site.open_my_bets_cashout()
        open_bets = False if self.brand == 'bma' else True
        edited_bet = self.get_bet_with_my_acca_edit(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
            event_name=self.event_params[1].event_name,
            open_bets=open_bets)
        self.__class__.actual_est_returns_value = edited_bet.est_returns.stake_value
        self.__class__.actual_stake_value = edited_bet.stake.stake_value
        self.assertTrue(self.actual_est_returns_value < self.est_returns_value,
                        msg=f'New Potential Returns value "{self.actual_est_returns_value}" is not updated')
        self.assertTrue(self.actual_stake_value < self.stake_value,
                        msg=f'New stake value "{self.actual_stake_value}" is not updated')

    def test_003_navigate_back_to_my_bets__open_betsverify_that_edit_my_betedit_my_acca_button_is_shown_for_double_only(
            self):
        """
        DESCRIPTION: Navigate back to My Bets > Open Bets
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown for DOUBLE only
        EXPECTED: - Two selections remained in edited ACCA
        EXPECTED: - Removed selection is shown and marked as 'REMOVED'
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE bet
        EXPECTED: - New Stake is shown
        EXPECTED: - New Est. Returns ( **Coral** )/New Potential Returns ( **Ladbrokes** ) is shown
          """
        self.site.open_my_bets_open_bets()
        self.__class__.edited_bet = self.get_bet_with_my_acca_edit(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
            event_name=self.event_params[1].event_name, open_bets=True)
        selection = self.edited_bet.items[2]
        self.assertTrue(selection.leg_remove_marker.is_displayed(), msg='Remove icon is not displayed')

        self.assertTrue(self.edited_bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')
        self.assertEqual(self.edited_bet.edit_my_acca_button.name, vec.ema.EDIT_MY_BET,
                         msg=f'"{vec.ema.EDIT_MY_BET}" button has incorrect name')
        self.__class__.est_returns_value = self.edited_bet.est_returns.stake_value
        self.__class__.stake_value = self.edited_bet.stake.stake_value
        self.assertTrue(self.actual_est_returns_value == self.est_returns_value,
                        msg=f'New Potential Returns value "{self.actual_est_returns_value}" is not updated')
        self.assertTrue(self.actual_stake_value == self.stake_value,
                        msg=f'New stake value "{self.actual_stake_value}" is not updated')

    def test_004_click_on_edit_my_betedit_my_acca_button_one_more_timedelete_one_of_the_selections_and_confirm_changes_or_add_a_result_in_tinavigate_back_to_my_bets__cashoutverify_that_edit_my_betedit_my_acca_button_is_not_shown_for_the_edited_acca(
            self):
        """
        DESCRIPTION: Click on 'EDIT MY BET/EDIT MY ACCA' button one more time
        DESCRIPTION: Delete one of the selections and confirm changes OR add a result in TI
        DESCRIPTION: Navigate back to My Bets > Cashout
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is NOT shown for the edited ACCA
        EXPECTED: - ONE selection remained in edited ACCA
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is NOT shown for SINGLE bet
        EXPECTED: - New Stake is shown
        EXPECTED: - New Est. Returns ( **Coral** )/New Potential Returns ( **Ladbrokes** ) is shown
        """
        self.edited_bet.edit_my_acca_button.click()
        self.assertTrue(self.edited_bet, msg=f'Cannot find bet for "{self.event_params[1].event_name}"')
        selection = self.edited_bet.items[0]
        self.assertTrue(selection.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')
        selection.edit_my_acca_remove_icon.click()
        self.assertTrue(wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(), timeout=3),
                        msg='"undo button" not displayed')
        confirm_button = self.edited_bet.confirm_button.name
        self.assertEqual(confirm_button, vec.ema.CONFIRM_EDIT.upper(),
                         msg=f'Actual text:"{confirm_button}" is not same as Expected text:"{vec.ema.CONFIRM_EDIT.upper()}".')
        self.edited_bet.confirm_button.click()
        _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE', event_names=self.event_params[1].event_name,
            raise_exceptions=False, number_of_bets=1)
        self.assertFalse(bet, msg=f'Bet for "{self.event_params[1].event_name}" still exists')
        self.site.open_my_bets_cashout()
        open_bets = False if self.brand == 'bma' else True
        single_bet = self.get_bet_with_my_acca_edit(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
            event_name=self.event_params[2].event_name,
            open_bets=open_bets)

        self.assertTrue(single_bet, msg=f'Cannot find bet for "{self.event_params[2].event_name}"')
        self.assertFalse(single_bet.has_edit_my_acca_button(),
                         msg=f'Bet have My ACCA button on header')
        self.__class__.actual_est_returns_value = single_bet.est_returns.stake_value
        self.__class__.actual_stake_value = single_bet.stake.stake_value
        self.assertTrue(self.actual_est_returns_value < self.est_returns_value,
                        msg=f'New Potential Returns value "{self.actual_est_returns_value}" is not updated')
        self.assertTrue(self.actual_stake_value < self.stake_value,
                        msg=f'New stake value "{self.actual_stake_value}" is not updated')

    def test_005_navigate_back_to_my_bets__open_betsverify_that_edit_my_betedit_my_acca_button_is_not_shown_for_the_edited_acca(
            self):
        """
        DESCRIPTION: Navigate back to My Bets > Open Bets
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is NOT shown for the edited ACCA
        EXPECTED: - ONE selection remained in edited ACCA
        EXPECTED: - Two removed selections are shown and marked as 'REMOVED'
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is NOT shown for SINGLE bet
        EXPECTED: - New Stake is shown
        EXPECTED: - New Est. Returns ( **Coral** )/New Potential Returns ( **Ladbrokes** ) is shown
        """
        self.site.open_my_bets_open_bets()
        single_open_bet = self.get_bet_with_my_acca_edit(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                         event_name=self.event_params[2].event_name,
                                                         open_bets=True)
        selection = single_open_bet.items[1]
        self.assertTrue(selection.leg_remove_marker.is_displayed(), msg='Remove icon is not displayed')
        selection = single_open_bet.items[2]
        self.assertTrue(selection.leg_remove_marker.is_displayed(), msg='Remove icon is not displayed')
        self.assertFalse(single_open_bet.has_edit_my_acca_button(),
                         msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')
        est_returns_value = single_open_bet.est_returns.stake_value
        stake_value = single_open_bet.stake.stake_value
        self.assertTrue(self.actual_est_returns_value == est_returns_value,
                        msg=f'New Potential Returns value "{self.actual_est_returns_value}" is not updated')
        self.assertTrue(self.actual_stake_value == stake_value,
                        msg=f'New stake value "{self.actual_stake_value}" is not updated')
