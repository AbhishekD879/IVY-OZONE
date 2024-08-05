import pytest
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create events
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.acca
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@vtest
class Test_C3020263_Verify_that_Edit_My_ACCA_button_is_displaying(BaseBetSlipTest):
    """
    TR_ID: C3020263
    NAME: Verify that 'Edit My ACCA' button is displaying
    DESCRIPTION: This test case verifies that ''Edit My Bet/Edit My ACCA' button is displaying when the bet on an ACCA is placed and two or more selections are open and all of selections are active
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add 2 (two) selections to Betslip and Place a bet for DOUBLE and SINGLES (Bet1)
    PRECONDITIONS: Add 3 (three) selections to Betslip and place a bet on TREBLE, DOUBLE, TRIXIE and SINGLES (Bet2)
    PRECONDITIONS: All selections in the placed bet are active
    PRECONDITIONS: All selections in the placed bet are open
    PRECONDITIONS: NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: **Coral** has 'EDIT MY BET' button
    PRECONDITIONS: **Ladbrokes** has 'EDIT MY ACCA' button
    """
    keep_browser_open = True

    def place_single_and_multiple_bet(self, selection_ids, single, multiples):
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=selection_ids)
        sections = self.get_betslip_sections(multiples=True)
        single_selection = sections.Singles[single]
        single_selection.amount_form.enter_amount('0.5')
        for multiple in multiples:
            multiple_section = sections.Multiples[multiple]
            multiple_section.amount_form.enter_amount('0.9')
        self.get_betslip_content().bet_now_button.click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add 2 (two) selections to Betslip and Place a bet for DOUBLE and SINGLES (Bet1)
        DESCRIPTION: Add 3 (three) selections to Betslip and place a bet on TREBLE, DOUBLE, TRIXIE and SINGLES (Bet2)
        """
        self.__class__.event1 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        event2 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        self.__class__.event3 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        event4 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        event5 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        selection_id1 = list(self.event1.selection_ids.values())[0]
        selection_id2 = list(event2.selection_ids.values())[0]
        selection_id3 = list(self.event3.selection_ids.values())[0]
        selection_id4 = list(event4.selection_ids.values())[0]
        selection_id5 = list(event5.selection_ids.values())[0]
        self.site.login()
        self.place_single_and_multiple_bet(selection_ids=(selection_id1, selection_id2), single=list(self.event1.selection_ids.keys())[0], multiples=['Double'])
        self.site.bet_receipt.footer.click_done()
        self.place_single_and_multiple_bet(selection_ids=(selection_id3, selection_id4, selection_id5), single=list(self.event3.selection_ids.keys())[0], multiples=['Double', 'Treble', 'Trixie'])

    def test_001_navigate_to_my_bets__cashout_verify_that_edit_my_bet_edit_my_acca_button_is_shown_only_for_double_from_bet1_and_treble_from_bet2(self, open_bets=False):
        """
        DESCRIPTION: Navigate to My Bets > Cashout
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE (from Bet1) and TREBLE (from Bet2)
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE (from Bet1) and TREBLE (from Bet2) bets
        EXPECTED: - Stake is shown
        EXPECTED: - Est. Returns ( **Coral** )/ Potential Returns ( **Ladbrokes** ) is shown
        """
        event_name1 = self.event1.team1 + ' v ' + self.event1.team2
        event_name2 = self.event3.team1 + ' v ' + self.event3.team2
        if self.device_type == 'mobile':
            self.navigate_to_page('homepage')
        if not open_bets and self.brand == 'bma':
            self.site.open_my_bets_cashout()
            bets = self.site.cashout.tab_content.accordions_list
            self.assertTrue(bets.items_as_ordered_dict, msg='No bets found on Cashout page')
        else:
            self.site.open_my_bets_open_bets()
            bets = self.site.open_bets.tab_content.accordions_list
            self.assertTrue(bets.items_as_ordered_dict, msg='No bets found on openbets page')
        single_bet_1 = bets.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=event_name1)

        single_bet_2 = bets.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=event_name2)

        double_bet_1 = bets.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=event_name1)

        double_bet_2 = bets.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=event_name2)

        treble_bet = bets.get_bet(
            bet_type=vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE, event_names=event_name2)

        trixie_bet = bets.get_bet(
            bet_type=vec.betslip.TRX.upper(), event_names=event_name2)

        acca_bets = [double_bet_1[1], treble_bet[1]]
        non_acca_bets = [single_bet_1[1], single_bet_2[1], double_bet_2[1], trixie_bet[1]]
        for bet in acca_bets:
            self.assertTrue(bet.has_edit_my_acca_button(), msg=f'edit my acca is not displayed for "{bet}"')
            bet.edit_my_acca_button.click()
            sleep(2)
            self.assertTrue(bet.stake.is_displayed(), msg=f'stake is not displayed for "{bet}"')
            self.assertTrue(bet.est_returns.is_displayed(), msg=f'stake is not displayed for "{bet}"')
            cancel_button_text = bet.edit_my_acca_button.name
            self.assertEqual(cancel_button_text, vec.ema.CANCEL.upper(),
                             msg=f'actual text:"{cancel_button_text}" is not changed to Expected text:"{vec.ema.CANCEL.upper()}".')
        for bet in non_acca_bets:
            self.assertFalse(bet.has_edit_my_acca_button(expected_result=False), msg=f'edit my acca is displayed for "{bet}"')
            self.assertTrue(bet.stake.is_displayed(), msg=f'stake is not displayed for "{bet}"')
            self.assertTrue(bet.est_returns.is_displayed(), msg=f'stake is not displayed for "{bet}"')

    def test_002_click_on_edit_my_bet_edit_my_acca_button_verify_that_edit_mode_of_the_acca_is_shown(self):
        """
        DESCRIPTION: Click on 'EDIT MY BET/EDIT MY ACCA' button
        DESCRIPTION: Verify that edit mode of the Acca is shown
        EXPECTED: - Edit mode of the Acca is shown
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button changes to the 'CANCEL EDITING' button
        """
        # covered in step 001

    def test_003_navigate_to_my_bets__open_bets_verify_that_edit_my_bet_edit_my_acca_button_is_shown_only_for_double_from_bet1_and_treble_from_bet2(self):
        """
        DESCRIPTION: Navigate to My Bets > Open Bets
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE (from Bet1) and TREBLE (from Bet2)
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE (from Bet1) and TREBLE (from Bet2) bets
        EXPECTED: - Stake is shown
        EXPECTED: - Est. Returns (**Coral**)/ Potential Returns(**Ladbrokes**) is shown
        """
        self.test_001_navigate_to_my_bets__cashout_verify_that_edit_my_bet_edit_my_acca_button_is_shown_only_for_double_from_bet1_and_treble_from_bet2(open_bets=True)

    def test_004_click_on_edit_my_bet_edit_my_acca_button_verify_that_edit_mode_of_the_acca_is_shown(self):
        """
        DESCRIPTION: Click on 'EDIT MY BET/EDIT MY ACCA' button
        DESCRIPTION: Verify that edit mode of the Acca is shown
        EXPECTED: - Edit mode of the Acca is shown
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button changes to the 'CANCEL EDITING' button
        """
        # covered in step 003
