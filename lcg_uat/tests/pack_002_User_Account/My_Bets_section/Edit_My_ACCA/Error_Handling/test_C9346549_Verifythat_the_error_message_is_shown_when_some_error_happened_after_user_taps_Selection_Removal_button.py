import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  // we cannot uncheck cashout event in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C9346549_Verifythat_the_error_message_is_shown_when_some_error_happened_after_user_taps_Selection_Removal_button(BaseCashOutTest):
    """
    TR_ID: C9346549
    NAME: Verifythat the error message is shown when some error happened after user taps 'Selection Removal' button
    DESCRIPTION: This test case verifies that error is shown when some error happened after user taps 'Selection Removal' button
    PRECONDITIONS: User1 has 2(bets) with cash out available placed on Single line Accumulator (All selections in the placed bet are active and open)
    PRECONDITIONS: Generate Error text in CMS: CMS System Config Data>EMA
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Navigate to My Bets > Cashout
    PRECONDITIONS: Tap 'EDIT MY ACCA' button
    PRECONDITIONS: Uncheck 'Cash out' in TI for any event in the bet (to generate Validbet / reqBetBuild or reqBetPlace error)
    """
    keep_browser_open = True
    number_of_events = 2
    selection_ids = []
    event_names = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Login with User1
        PRECONDITIONS: Navigate to My Bets > Cashout
        PRECONDITIONS: Tap 'EDIT MY ACCA' button
        PRECONDITIONS: Uncheck 'Cash out' in TI for any event in the bet (to generate Validbet / reqBetBuild or reqBetPlace error)
        """
        if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
            self.cms_config.set_my_acca_section_cms_status(ema_status=True)

        self.__class__.cms_error_txt = self.cms_config.get_system_configuration_structure()['EMA']['genericErrorText']
        if not self.cms_error_txt:
            self.cms_config.update_system_configuration_structure(
                config_item='EMA', field_name='genericErrorText', field_value='Please try again later or check the selections')
            self.cms_error_txt = self.cms_config.get_system_configuration_structure()['EMA']['genericErrorText']
            self.assertTrue(self.cms_error_txt, msg='"genericErrorText" is not configured in CMS')

        event = self.ob_config.add_autotest_premier_league_football_event()
        event2 = self.ob_config.add_autotest_premier_league_football_event()
        self.selection_ids = [event.selection_ids[event.team1],
                              event2.selection_ids[event2.team1]]

        self.__class__.event_id = event.event_id

        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_cashout()
        sleep(2)
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No bets found on Cashout page')
        self.__class__.bet = list(bets.values())[0]
        self.bet.edit_my_acca_button.click()
        self.ob_config.change_event_cashout_status(event_id=self.event_id, cashout_available=False)

    def test_001_tap_selection_removal_button_for_any_selectionverify_that_an_error_message_is_shown_and_selection_is_not_removed(self):
        """
        DESCRIPTION: Tap 'Selection Removal' button for any selection
        DESCRIPTION: Verify that an error message is shown and selection is not removed
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: - Eror message "text from CMS" is shown
        EXPECTED: - Selection is not removed
        EXPECTED: - 'CONFIRM' button is disabled
        EXPECTED: - 'CANCEL EDITING' button is enabled
        """
        selection = list(self.bet.items_as_ordered_dict.values())[0]
        selection.edit_my_acca_remove_icon.click()
        sleep(2)
        # cash_out_successful_message property represents error message in ui
        self.assertEquals(self.bet.cash_out_successful_message, self.cms_error_txt,
                          msg=f'"{self.bet.cash_out_successful_message}" text is not same as "{self.cms_error_txt}"')
        self.assertTrue(selection.has_edit_my_acca_remove_icon(), msg='"Selection removal icon(X)" is not displayed"')
        self.assertFalse(self.bet.confirm_button.is_enabled(expected_result=False),
                         msg=f'"{vec.ema.CONFIRM_EDIT}" button is clickable')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.ema.CANCEL}" button is not enabled')

    def test_002_provide_same_verification_on_my_bets__open_bets_tabverify_that_an_error_message_is_shown_and_selection_is_not_removed(self):
        """
        DESCRIPTION: Provide same verification on My Bets > Open Bets tab
        DESCRIPTION: Verify that an error message is shown and selection is not removed
        EXPECTED: Edit mode is shown with appropriate elements:
        EXPECTED: - Error message "text from CMS" is shown
        EXPECTED: - Selection is not removed
        EXPECTED: - 'CONFIRM' button is disabled
        EXPECTED: - 'CANCEL EDITING' button is enabled
        """
        self.bet.edit_my_acca_button.click()
        self.ob_config.change_event_cashout_status(event_id=self.event_id, cashout_available=True)
        self.site.open_my_bets_open_bets()
        sleep(2)
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No bets found on Cashout page')
        self.__class__.bet = list(bets.values())[0]
        self.bet.edit_my_acca_button.click()
        self.ob_config.change_event_cashout_status(event_id=self.event_id, cashout_available=False)
        self.test_001_tap_selection_removal_button_for_any_selectionverify_that_an_error_message_is_shown_and_selection_is_not_removed()
