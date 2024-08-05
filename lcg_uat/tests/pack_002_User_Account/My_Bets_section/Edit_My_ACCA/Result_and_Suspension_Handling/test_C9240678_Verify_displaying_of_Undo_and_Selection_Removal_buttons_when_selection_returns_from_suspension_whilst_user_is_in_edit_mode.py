import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C9240678_Verify_displaying_of_Undo_and_Selection_Removal_buttons_when_selection_returns_from_suspension_whilst_user_is_in_edit_mode(BaseBetSlipTest):
    """
    TR_ID: C9240678
    NAME: Verify displaying of Undo and Selection Removal buttons when selection returns from suspension whilst user is in edit mode
    DESCRIPTION: This test case verifies that initial edit mode is shown with enabled 'Selection removal' buttons when selection returns from suspension whilst user is in edit mode
    PRECONDITIONS: User1 has 2(bets) with cash out available placed on Single line Accumulator (All selections in the placed bet are active and open)
    PRECONDITIONS: 1. Login with User1
    PRECONDITIONS: 2. Navigate to My Bets > Cashout
    PRECONDITIONS: 3. Tap 'EDIT MY ACCA' button
    PRECONDITIONS: 4. Tap 'Selection Removal' button for any selection
    PRECONDITIONS: 5. Go to TI and Suspend event/market/selection which was removed in the previous step
    PRECONDITIONS: NOTE: The verifications should be done in 'List View' and in 'Card View'
    """
    keep_browser_open = True
    bet_type = 'TREBLE'

    @classmethod
    def custom_setUp(cls):
        acca_section_status = cls.get_initial_data_system_configuration().get('EMA', {})
        if not acca_section_status:
            acca_section_status = cls.get_cms_config().get_system_configuration_item('EMA')
        if not acca_section_status.get('enabled'):
            raise CmsClientException('My ACCA section is disabled in CMS')

    def get_bets(self):
        self.site.open_my_bets_open_bets()
        _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=self.bet_type,
            selection_ids=self.selection_ids)
        return self.bet

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
        self.selection_ids = [event.selection_ids[event.team1],
                              event2.selection_ids[event2.team1],
                              event3.selection_ids[event3.team1]]
        self.__class__.selection_name = event.team1
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
        if self.device_type == "mobile":
            self.site.bet_receipt.footer.click_done()
        self.get_bets()
        EMB_button = wait_for_result(lambda: self.bet.edit_my_acca_button,
                                     name=f'"{vec.ema.EDIT_MY_BET}" button will be displayed')
        self.assertTrue(EMB_button, msg=f'"{vec.ema.EDIT_MY_BET}" is not displayed')
        # selection = list(self.bet.items_as_ordered_dict.values())[0]
        # self.assertTrue(selection.has_edit_my_acca_remove_icon(),
        #                 msg='"Selection removal icon(X)" is not displayed')
        # selection.edit_my_acca_remove_icon.click()
        # self.site.wait_splash_to_hide(5)
        # self.ob_config.change_selection_state(selection_id=self.selection_ids[0], active=False, displayed=True)

    def test_001_navigate_back_to_the_applicationverify_that_disabled_selection_removal_buttons_and_susp_confirm_button_are_shown(self):
        """
        DESCRIPTION: Navigate back to the application
        DESCRIPTION: Verify that disabled 'Selection Removal' buttons and 'SUSP CONFIRM' button are shown
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: - 'SUSPENDED' label and disabled 'Selection Removal' button for suspended event/market/selection
        EXPECTED: - Disabled 'Selection Removal' buttons for all other selections
        EXPECTED: - Original Stake and Est. Returns are shown
        EXPECTED: - 'SUSP CONFIRM' button is shown and disabled
        EXPECTED: - 'CANCEL EDITING' is shown and enabled
        """
        self.__class__.est_returns_value = self.bet.est_returns.stake_value
        self.bet.edit_my_acca_button.click()
        self.__class__.selection = self.bet.items[0]
        self.assertTrue(self.selection.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')
        self.selection.edit_my_acca_remove_icon.click()
        self.__class__.edited_bet = self.get_bets()
        selection = self.edited_bet.items[0]
        self.assertEqual(selection.outcome_name, self.selection_name,
                         msg=f'Selection name for the removed selection "{self.selection_name}" is not displayed')
        self.assertTrue(selection.edit_my_acca_undo_icon.is_displayed(), msg='UNDO button is not displayed')
        actual_est_returns_value = self.edited_bet.est_returns.stake_value
        self.assertTrue(actual_est_returns_value < self.est_returns_value,
                        msg=f'New Potential Returns value "{actual_est_returns_value}" is not updated')
        actual_label = self.edited_bet.est_returns.label
        self.assertEqual(actual_label, vec.bet_history.NEW_TOTAL_RETURN,
                         msg=f'Actual label "{actual_label}" != Expected "{vec.bet_history.NEW_TOTAL_RETURN}"')
        self.assertTrue(self.edited_bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have '
                            f'"{vec.ema.CANCEL}" button on header')
        self.assertEqual(self.edited_bet.edit_my_acca_button.name, vec.ema.CANCEL,
                         msg=f'"{vec.ema.CANCEL}" button is not displayed')

    def test_002_navigate_to_ti_and_unsuspend_eventmarketselection_which_was_suspended_in_preconditions(self):
        """
        DESCRIPTION: Navigate to TI and unsuspend event/market/selection which was suspended in preconditions
        EXPECTED: The selection event/market/selection is active
        """
        pass

    def test_003_navigate_back_to_the_applicationverify_that_initial_edit_mode_is_shown_with_enabled_selection_removal_buttons(self):
        """
        DESCRIPTION: Navigate back to the application
        DESCRIPTION: Verify that initial edit mode is shown with enabled 'Selection removal' buttons
        EXPECTED: - Edit mode is shown with enabled 'Selection Removal' buttons for all selections in the bet
        EXPECTED: - Original Stake and Est. Returns are shown
        EXPECTED: - 'CONFIRM' button is shown and disabled
        EXPECTED: - 'CANCEL EDITING' is enabled
        """
        pass

    def test_004_provide_the_same_verification_on_my_bets__open_bets_tabverify_that_initial_edit_mode_is_shown_with_enabled_selection_removal_buttons_after__selection_returns_from_suspension(self):
        """
        DESCRIPTION: Provide the same verification on My Bets > Open Bets tab
        DESCRIPTION: Verify that initial edit mode is shown with enabled 'Selection removal' buttons after  selection returns from suspension
        EXPECTED: - Edit mode is shown with enabled 'Selection Removal' buttons for all selections in the bet
        EXPECTED: - 'CONFIRM' button is disabled
        EXPECTED: - 'CANCEL EDITING' is enabled
        """
        pass
