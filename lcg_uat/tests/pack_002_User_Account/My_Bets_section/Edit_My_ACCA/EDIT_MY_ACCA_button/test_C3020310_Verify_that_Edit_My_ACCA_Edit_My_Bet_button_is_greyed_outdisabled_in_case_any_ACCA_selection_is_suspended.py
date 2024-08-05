import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod   # can't do event suspension
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C3020310_Verify_that_Edit_My_ACCA_Edit_My_Bet_button_is_greyed_outdisabled_in_case_any_ACCA_selection_is_suspended(BaseCashOutTest):
    """
    TR_ID: C3020310
    NAME: Verify that 'Edit My ACCA/Edit My Bet' button is greyed out(disabled) in case any ACCA selection is suspended
    DESCRIPTION: This test case verifies that the 'EDIT MY ACCA/Bet' button is greyed out(disabled) and the button is NOT clickable.
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add 3 (three) selections to Betslip and place a bet on TREBLE and SINGLES
    PRECONDITIONS: All selections in the placed bet are active
    PRECONDITIONS: All selections in the placed bet are open
    PRECONDITIONS: **Coral** has 'EDIT MY BET' button
    PRECONDITIONS: **Ladbrokes** has 'EDIT MY ACCA' button
    """
    keep_browser_open = True
    number_of_events = 3
    event_names = []
    selection_ids = []
    event_ids = []
    bet_amount = 0.1

    def test_000_preconditions(self):
        """
        PRECONDITIONS: EMA is enabled in CMS
        PRECONDITIONS: User should be logged in
        PRECONDITIONS: User have placed a 4 fold or 5 fold accumulator bet.
        """
        self.site.login()
        if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
            self.cms_config.set_my_acca_section_cms_status(ema_status=True)
        for i in range(0, 3):
            event = self.ob_config.add_autotest_premier_league_football_event()
            eventID = event.event_id
            self.event_ids.append(eventID)
            self.event_names.append(event.ss_response['event']['name'])
            self.selection_ids.append(list(event.selection_ids.values())[0])
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_single_bet(number_of_stakes=3)
        self.site.bet_receipt.close_button.click()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_my_bets__cashout_and_open_betsverify_that_edit_my_betedit_my_acca_button_is_shown_for_treble_only(
            self):
        """
        DESCRIPTION: Navigate to My Bets > Cashout and Open Bets
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown for TREBLE only
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is shown only for TREBLE bet
        EXPECTED: - Stake is shown
        EXPECTED: - Est. Returns ( **Coral** )/ Potential Returns ( **Ladbrokes** ) is shown
        """
        for event in self.event_names:
            self.site.open_my_bets_open_bets()
            _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                event_names=event)
            stake = bet.stake.value
            actual_potential_returns = bet.est_returns.value
            self.assertFalse(bet.has_edit_my_acca_button(expected_result=False),
                             msg=f'"{vec.EMA.EDIT_MY_BET}" button is displayed')
            self.assertTrue(stake,
                            msg=f'The stake: "{stake}" is not displayed')
            self.assertTrue(actual_potential_returns,
                            msg=f'Potential returns: "{actual_potential_returns}" is not displayed')
        _, bet_before_EMA = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history._bet_types_TBL.upper(),
            event_names=self.event_names)
        self.assertTrue(bet_before_EMA, msg=f' The bet : "{bet_before_EMA.bet_type}" is not displayed"')
        actual_potential_returns = bet_before_EMA.est_returns.value
        stake_before_EMA = bet_before_EMA.stake.value
        self.assertTrue(bet_before_EMA.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(stake_before_EMA,
                        msg=f'The stake: "{stake_before_EMA}" is not displayed')
        self.assertTrue(actual_potential_returns,
                        msg=f'Potential returns: "{actual_potential_returns}" is not displayed')

    def test_002_suspended_one_of_the_selections_of_the_treble_in_backoffice(self):
        """
        DESCRIPTION: Suspended one of the selections of the TREBLE in Backoffice
        EXPECTED: Selection is suspended
        """
        self.ob_config.change_event_state(event_id=self.event_ids[0], displayed=True, active=False)
        sleep(7)
        self.device.refresh_page()
        self.site.open_my_bets_open_bets()
        _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history._bet_types_TBL.upper(),
            event_names=self.event_names)
        selection = list(bet.items_as_ordered_dict.values())[0]
        self.site.wait_splash_to_hide(7)
        self.assertTrue(selection.icon.is_displayed(), msg='"SUSP" label is not displayed')

    def test_003_navigate_to_my_bets__cashout(self):
        """
        DESCRIPTION: Navigate to My Bets > Cashout
        EXPECTED: The cashout page is displayed
        """
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            self.site.wait_content_state_changed()
            _, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history._bet_types_TBL.upper(),
                event_names=self.event_names)

    def test_004_verify_that_the_edit_my_accabet_button_is_greyed_out_disabled_and_the_button_is_not_clickable(self):
        """
        DESCRIPTION: Verify that the 'EDIT MY ACCA/Bet' button is greyed out (disabled) and the button is NOT clickable
        EXPECTED: - Grey (disabled) 'EDIT MY BET/EDIT MY ACCA' button is shown for TREBLE
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is NOT clickable
        EXPECTED: - Suspended selection is greyed out and has 'SUSP' label
        EXPECTED: - Stake is shown
        EXPECTED: - Est. Returns ( **Coral** )/ Potential Returns ( **Ladbrokes** ) is shown
        """
        if self.brand == 'bma':
            self.assertTrue(self.bet, msg=f' The bet : "{self.bet.bet_type}" is not displayed"')
            actual_potential_returns = self.bet.est_returns.value
            stake = self.bet.stake.value
            self.assertFalse(self.bet.edit_my_acca_button.is_enabled(expected_result=False),
                             msg=f'"{vec.EMA.EDIT_MY_BET}" button is enabled')
            self.assertTrue(stake,
                            msg=f'The stake: "{stake}" is not displayed')
            self.assertTrue(actual_potential_returns,
                            msg=f'Potential returns: "{self.actual_potential_returns}" is not displayed')

    def test_005_navigate_to_my_bets__open_bets(self):
        """
        DESCRIPTION: Navigate to My Bets > Open Bets
        EXPECTED: The Open bets tab is displayed
        """
        self.site.open_my_bets_open_bets()

    def test_006_verify_that_the_edit_my_betedit_my_acca_button_is_greyed_out_disabled_and_the_button_is_not_clickable(
            self):
        """
        DESCRIPTION: Verify that the 'EDIT MY BET/EDIT MY ACCA' button is greyed out (disabled) and the button is NOT clickable
        EXPECTED: - Grey (disabled) 'EDIT MY BET/EDIT MY ACCA' button is shown for TREBLE
        EXPECTED: - 'EDIT MY ACCA/Bet' button is NOT clickable
        EXPECTED: - Suspended selection is greyed out and has 'SUSP' label
        EXPECTED: - Stake is shown
        EXPECTED: - Est. Returns ( **Coral** )/ Potential Returns ( **Ladbrokes** ) is shown
        """
        _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history._bet_types_TBL.upper(),
            event_names=self.event_names)
        self.assertTrue(bet, msg=f' The bet : "{bet.bet_type}" is not displayed"')
        actual_potential_returns = bet.est_returns.value
        stake = bet.stake.value
        self.assertFalse(bet.edit_my_acca_button.is_enabled(expected_result=False),
                         msg=f'"{vec.EMA.EDIT_MY_BET}" button is enabled')
        self.assertTrue(stake,
                        msg=f'The stake: "{stake}" is not displayed')
        self.assertTrue(actual_potential_returns,
                        msg=f'Potential returns: "{actual_potential_returns}" is not displayed')
