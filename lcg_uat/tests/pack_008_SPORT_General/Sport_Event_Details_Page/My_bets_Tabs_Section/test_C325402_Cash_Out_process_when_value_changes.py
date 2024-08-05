import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from time import sleep


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.prod #Involves event creation and price update
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C325402_Cash_Out_process_when_value_changes(BaseCashOutTest):
    """
    TR_ID: C325402
    NAME: Cash Out process when value changes
    DESCRIPTION: This test case verifies Cash Out functionality when cash out value changes during cash out process on 'My Bets' tab on Event Details page
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: * To check tolerance value on test environments please follow the next url (for information about other environments or any changes please contact UAT team):
    PRECONDITIONS: * http://backoffice-tst2.coral.co.uk/office -> Admin -> Miscellaneous -> Openbet Config -> Configurable cashout values -> COMB_TOLERANCE_VALUE. (Make sure that the tolerance is enabled with the ENABLE_COMB_TOLERANCE config)
    PRECONDITIONS: * Note: when tolerance is disabled it means that all increased values are treated as being within the tolerance
    PRECONDITIONS: **From release XXX.XX:**
    PRECONDITIONS: - Open Dev Tools -> Network tab -> WS filter (cashout request)
    PRECONDITIONS: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: - initial bets data will be returned after establishing connection
    """
    keep_browser_open = True
    bet_amount = 5
    increased_price = '14/1'
    decreased_price = '1/14'
    initial_multiple_cashout_value, initial_single_cashout_value = None, None
    initial_odds_value = None
    created_event_name2 = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Run Cash Out precondition steps which creates testing data
        EXPECTED: Test event with available Cash Out was created
        """
        events = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        self.__class__.created_event_name, created_event_name2 = \
            ['%s %s' % (event.event_name, event.local_start_time) for event in events]
        self.__class__.team1, team2 = [event.team1 for event in events]
        self.__class__.selection_ids = {event.team1: event.selection_ids[event.team1] for event in events}
        self.site.login()
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values()))
        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_bets_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets with available cash out
        """
        self.site.open_my_bets_cashout()

    def test_002_navigate_to_the_single_bet_and_check_cash_out_value_on_cash_out_button(self):
        """
        DESCRIPTION: Navigate to the **Single** bet and check cash out value on 'CASH OUT' button
        """
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.single_bet = list(bets.values())[0]
        self.__class__.multiple_bet = list(bets.values())[1]
        self.__class__.initial_single_cashout_value = self.single_bet.buttons_panel.full_cashout_button.amount.value
        betlegs = self.single_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg_name, betleg = list(betlegs.items())[0]
        self.__class__.initial_odds_value = betleg.odds_value
        self.__class__.initial_multiple_cashout_value = self.multiple_bet.buttons_panel.full_cashout_button.amount.value

    def test_003_trigger_situation_when_cash_out_value_increases_within_tolerance_value_for_less_than_cashout_value_plus_cashout_valuetolerance_value_during_cash_out_process_priceodds_should_be_decreased_change_price_in_backoffice_click_cash_out___confirm_cash_out(self):
        """
        DESCRIPTION: Trigger situation when cash out value **increases within tolerance value** (for less than cashout_value + cashout_value*tolerance_value) during cash out process (price/Odds should be decreased):
        DESCRIPTION: * Change price in backoffice
        DESCRIPTION: * Click 'CASH OUT' -> 'CONFIRM CASH OUT'
        EXPECTED: * Cash Out attempt is successful
        EXPECTED: * User balance is increased on value from step #2, not the changed one
        """
        self.ob_config.change_price(selection_id=self.selection_ids[self.team1], price=self.increased_price)
        sleep(3)
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.selection_ids[self.team1],
                                                                 price=self.increased_price)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "{self.created_event_name}" with id '
                            f'"{self.selection_ids[self.team1]}" is not received')

        self.assertTrue(self.single_bet.buttons_panel.full_cashout_button.wait_amount_to_change(
                        initial_amount=self.initial_single_cashout_value),
                        msg='Cashout amount is not changed')

        new_single_cashout_value = self.single_bet.buttons_panel.full_cashout_button.amount.value
        self.assertTrue(float(self.initial_single_cashout_value) > float(new_single_cashout_value),
                        msg='New cashout value "%s" is not lower than "%s"' %
                            (new_single_cashout_value, self.initial_single_cashout_value))

        betlegs = self.single_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg_name, betleg = list(betlegs.items())[0]
        new_single_odds_value = betleg.odds_value

        self.assertEqual(self.initial_odds_value, new_single_odds_value,
                         msg='Odds is changed from "%s" to "%s"' % (self.initial_odds_value, new_single_odds_value))

        self.assertTrue(self.multiple_bet.buttons_panel.full_cashout_button.wait_amount_to_change(
                        initial_amount=self.initial_multiple_cashout_value),
                        msg='Cashout Amount is not changed')

        new_multiple_cashout_value = self.multiple_bet.buttons_panel.full_cashout_button.amount.value
        self.assertTrue(float(self.initial_multiple_cashout_value) > float(new_multiple_cashout_value),
                        msg='New cashout value "%s" is not lower than "%s"' %
                            (self.initial_multiple_cashout_value, new_multiple_cashout_value))

        betlegs = self.multiple_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg_name = '%s - %s' % (self.team1, self.created_event_name)
        betleg = betlegs.get(betleg_name)
        self.assertTrue(betleg, msg='BetLeg %s is not found' % betleg_name)
        new_multiple_odds_value = betleg.odds_value

        self.assertEqual(self.initial_odds_value, new_multiple_odds_value,
                         msg='Odds is changed from "%s" to "%s"' % (self.initial_odds_value, new_multiple_odds_value))
        self.__class__.initial_odds_value = self.initial_odds_value
        self.__class__.initial_multiple_cashout_value = new_multiple_cashout_value
        self.__class__.initial_single_cashout_value = new_single_cashout_value

    def test_004_navigate_to_another_single_bet_and_check_cash_out_value_on_cash_out_button(self):
        """
        DESCRIPTION: Navigate to another **Single** bet and check cash out value on 'CASH OUT' button
        """
        # Covered in step 2

    def test_005_trigger_situation_when_cash_out_value_increases_above_tolerance_value_for_more_than_cashout_value_plus_cashout_valuetolerance_value_during_cash_out_process_for_cashoutbet_response_priceodds_should_be_decreased_change_price_in_backoffice_click_cash_out___confirm_cash_out(self):
        """
        DESCRIPTION: Trigger situation when cash out value **increases above tolerance value** (for more than cashout_value + cashout_value*tolerance_value) during cash out process for **cashoutBet** response (price/Odds should be decreased):
        DESCRIPTION: * Change price in backoffice
        DESCRIPTION: * Click 'CASH OUT' -> 'CONFIRM CASH OUT'
        EXPECTED: * Cash Out attempt successful
        """
        self.ob_config.change_price(selection_id=self.selection_ids[self.team1], price=self.decreased_price)
        sleep(3)
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.selection_ids[self.team1],
                                                                 price=self.decreased_price)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "{self.created_event_name}" with id '
                            f'"{self.selection_ids[self.team1]}" is not received')

        self.assertTrue(self.single_bet.buttons_panel.full_cashout_button.wait_amount_to_change(
                        initial_amount=self.initial_single_cashout_value),
                        msg='Cashout Amount is not changed')

        new_single_cashout_value = self.single_bet.buttons_panel.full_cashout_button.amount.value
        self.assertTrue(float(self.initial_single_cashout_value) < float(new_single_cashout_value),
                        msg='New cashout value "%s" is not larger than "%s"' %
                            (new_single_cashout_value, self.initial_single_cashout_value))

        betlegs = self.single_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg_name, betleg = list(betlegs.items())[0]
        new_single_odds_value = betleg.odds_value

        self.assertEqual(self.initial_odds_value, new_single_odds_value,
                         msg='Odds is changed from "%s" to "%s"' % (self.initial_odds_value, new_single_odds_value))

        self.assertTrue(self.multiple_bet.buttons_panel.full_cashout_button.wait_amount_to_change(
                        initial_amount=self.initial_multiple_cashout_value),
                        msg='Cashout Amount is not changed')

        new_multiple_cashout_value = self.multiple_bet.buttons_panel.full_cashout_button.amount.value
        self.assertTrue(float(self.initial_multiple_cashout_value) < float(new_multiple_cashout_value),
                        msg='New cashout value "%s" is not lower than "%s"' %
                            (self.initial_multiple_cashout_value, new_multiple_cashout_value))

        betlegs = self.multiple_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg_name = '%s - %s' % (self.team1, self.created_event_name)
        betleg = betlegs.get(betleg_name)
        self.assertTrue(betleg, msg='BetLeg %s is not found' % betleg_name)
        new_multiple_odds_value = betleg.odds_value

        self.assertEqual(self.initial_odds_value, new_multiple_odds_value,
                         msg='Odds is changed from "%s" to "%s"' % (self.initial_odds_value, new_multiple_odds_value))
        self.single_bet.buttons_panel.full_cashout_button.click()
        self.single_bet.buttons_panel.cashout_button.click()
        self.assertTrue(self.single_bet.has_cashed_out_mark(timeout=20),
                        msg='"Cashed out" mark is not present on Cashout page after cashout')
        self.multiple_bet.buttons_panel.full_cashout_button.click()
        self.multiple_bet.buttons_panel.cashout_button.click()
        self.assertTrue(self.multiple_bet.has_cashed_out_mark(timeout=20),
                        msg='"Cashed out" mark is not present on Cashout page after cashout')

    def test_006_verify_error_messages(self):
        """
        DESCRIPTION: Verify error messages
        EXPECTED: The error message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: * Message box with an "X" in a circle and message of 'CASH OUT UNSUCCESSFUL' is shown below bet line details. Icon and text are centered.
        EXPECTED: * Underneath previous box second message is displayed with centered text **Your Cash Out attempt was unsuccessful due to a price change. Please try again.**
        """
        # Covered in step 5

    def test_007_verify_error_messages_disappearing(self):
        """
        DESCRIPTION: Verify error messages disappearing
        EXPECTED: * Error messages disappear when getBetDetail response is received with new cash out value and without error
        EXPECTED: * 'CASH OUT' button with new value and slider set to 100% are displayed
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Error messages disappear when new WebSocket connection to Cashout MS is created with new cash out value and error is not received in cashoutBet responce
        EXPECTED: * 'CASH OUT' button with new value and slider set to 100% are displayed
        """
        # Covered in step 5

    def test_008_trigger_situation_when_cash_out_value_increases_above_tolerance_value_for_more_than_cashout_value_plus_cashout_valuetolerance_value_during_cash_out_process_for_readbet_response_priceodds_should_be_decreased_click_cash_out___confirm_cash_out_change_price_in_backoffice(self):
        """
        DESCRIPTION: Trigger situation when cash out value **increases above tolerance value** (for more than cashout_value + cashout_value*tolerance_value) during cash out process for **readBet** response (price/Odds should be decreased):
        DESCRIPTION: * Click 'CASH OUT' -> 'CONFIRM CASH OUT'
        DESCRIPTION: * Change price in backoffice
        EXPECTED: * Cash Out attempt is NOT successful
        EXPECTED: * User balance is not updated
        EXPECTED: * Error messages are displayed
        EXPECTED: * subErrorCode "CASHOUT_VALUE_CHANGE" is received in readBet response
        """
        # Covered in step 3

    def test_009_repeat_steps_6_7(self):
        """
        DESCRIPTION: Repeat steps #6-7
        EXPECTED: Results are the same
        """
        # Covered in step 5

    def test_010_repeat_steps_4_9_for_situation_when_cash_out_value_decreases_during_cash_out_process__priceodds_should_be_increased(self):
        """
        DESCRIPTION: Repeat steps #4-9 for situation when cash out value **decreases** during cash out process  (price/Odds should be increased)
        EXPECTED: Results are the same
        """
        # Covered in step 5

    def test_011_repeat_steps_2_10_for_multiple_bets(self):
        """
        DESCRIPTION: Repeat steps #2-10 for **Multiple** bets
        EXPECTED: Results are the same
        """
        # Covered in step 5

    def test_012_repeat_steps_2_11_for_partial_cash_out_attempt(self):
        """
        DESCRIPTION: Repeat steps #2-11 for Cash out attempt
        EXPECTED: Results are the same
        """
        # Covered in step 5
