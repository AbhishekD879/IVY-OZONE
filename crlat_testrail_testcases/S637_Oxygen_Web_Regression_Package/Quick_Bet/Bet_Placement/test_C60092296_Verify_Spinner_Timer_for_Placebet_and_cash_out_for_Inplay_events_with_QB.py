import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C60092296_Verify_Spinner_Timer_for_Placebet_and_cash_out_for_Inplay_events_with_QB(Common):
    """
    TR_ID: C60092296
    NAME: Verify Spinner + Timer for  Placebet and cash out for Inplay events with QB.
    DESCRIPTION: This test case verifies displaying for Spinner + Count down timer on clicking on 'Place Bet' button and Spinner + Count down timer on clicking on 'cashout' button for Inplay events
    PRECONDITIONS: 1. Quick Bet functionality is enabled in CMS and user`s settings
    PRECONDITIONS: 2. Load the app
    PRECONDITIONS: 3. Log in with a user that has a positive balance
    PRECONDITIONS: 4. Cash out should be available
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Application is opened.
        """
        pass

    def test_002_add_a_selection_to_the_quickbet_from_any_inplay_events(self):
        """
        DESCRIPTION: Add a selection to the QuickBet from any Inplay events
        EXPECTED: Quick Bet is displayed at the bottom of the page:
        EXPECTED: * Quick Bet header and 'X' button
        EXPECTED: * User should able to see Ladbrokes/Coral main header
        EXPECTED: * User is able to see his balance in main header
        EXPECTED: * Selection name, Market name and Event name
        EXPECTED: * "Use Freebet" under event details (if available)
        EXPECTED: * Quick Stakes (For example, "+£5", "+£10" "+£50", "+£100")
        EXPECTED: * Price odds and Stake box
        EXPECTED: * Total Stake & Estimated returns
        EXPECTED: * The button "Add to betslip" is active and "Place bet" is disabled
        EXPECTED: "Boost" button (if available)
        EXPECTED: ![](index.php?/attachments/get/122293729)
        """
        pass

    def test_003_tap_on_the_stake_field_and_enter_any_value(self):
        """
        DESCRIPTION: Tap on the 'Stake' field and enter any value
        EXPECTED: * The keyboard appears
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Total Stake', 'Estimated Returns' - Coral, 'Total Stake', 'Potential Returns' - Ladbrokes are calculated
        EXPECTED: * The buttons 'Add to betslip' and 'Place bet' are active
        EXPECTED: * The 'Boost' button is active and can be boosted (if available)
        EXPECTED: Please note The keyboard doesn't appear when using 'Quick Stake' buttons
        """
        pass

    def test_004_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on 'Place bet' button
        EXPECTED: * Spinner + Count down timer is displayed on clicking on 'Place bet' for a few seconds
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User balance is decreased by stake entered on step #3
        EXPECTED: For In-Play :
        EXPECTED: ![](index.php?/attachments/get/122293741)
        EXPECTED: Note:
        EXPECTED: 1.Countdown timer is determined by the BIR delay set in Openbet
        EXPECTED: 2.We have a single bet -> Countdown timer will be BIR delay set in OB for that particular selection
        EXPECTED: we have a Double bet(Different BIR delay for both selections)-> Timer would be the longest timer that is on any selection in the bet. So if one selection has 4 seconds BIR delay and other has 7 seconds, it will take 7 seconds.
        EXPECTED: 3.Double bet(one preplay and other Inplay selection)-> If any in-play selection is in the bet, it will have the spinner + timer
        """
        pass

    def test_005_verify_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Bet Receipt
        EXPECTED: Bet Receipt consists of:
        EXPECTED: * 'Bet Receipt' header and 'X' button
        EXPECTED: * The message '✓Bet Placed Successfully'
        EXPECTED: * Date and time of the placed bet (format DD/MM/YYYY, HH:MM)
        EXPECTED: * Type of bet @ price odds (for example, Single @ 1/1)
        EXPECTED: * Bet receipt ID
        EXPECTED: * Selection name
        EXPECTED: * Market name/Event name
        EXPECTED: * Cashout label (if available)
        EXPECTED: * Stake & Est. Returns - Coral, Stake for this bet, Potential returns - Ladbrokes
        EXPECTED: * Message 'This bet has been boosted' (if the price was boosted)
        """
        pass

    def test_006_click_on_the_x_button(self):
        """
        DESCRIPTION: Click on the 'X' button
        EXPECTED: The Quick Bet is closed
        """
        pass

    def test_007_click_on_my_bets_button_from_the_header_for_coral_and_for_ladbrokes_my_account___my_bets(self):
        """
        DESCRIPTION: Click on 'My Bets' button from the header for Coral and for Ladbrokes 'My account' -> 'My Bets'
        EXPECTED: 'Open Bets' tab is opened
        """
        pass

    def test_008_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and verify that the Bet Receipt fields are correct
        EXPECTED: Check the following data correctness:
        EXPECTED: * Type of bet (for example, Single)
        EXPECTED: * Selection @ price odds (for example, Adelaide Utd @ 1/1)
        EXPECTED: * Market name
        EXPECTED: * Event name
        EXPECTED: * Time of the event in format HH:MM, DD Month(for example, 10:30, 17 Jan)
        EXPECTED: * The currency is as user set during registration
        EXPECTED: * Full/Partial Cashout (if available)
        EXPECTED: * Stake & Est. Returns - Coral, Stake, Potential returns - Ladbrokes
        EXPECTED: * '>' Sign to navigate to event page
        EXPECTED: ![](index.php?/attachments/get/59204800) ![](index.php?/attachments/get/59204801)
        """
        pass

    def test_009_now_click_on_cashout(self):
        """
        DESCRIPTION: Now click on cashout
        EXPECTED: User should be able to cashout and Spinner + Count down timer should be seen
        EXPECTED: ![](index.php?/attachments/get/122293760)
        EXPECTED: Note:
        EXPECTED: Coral: For coral Inplay cash out is coming from OB (Openbet Config -> Configurable cash out values -> CASH OUT_SINGLE_DELAY (Single bet) and CASHOUT_MULTI_DELAY field (Multi bet))
        EXPECTED: Lads: Reading the values from BIR delay set in OB
        """
        pass

    def test_010_repeat_steps_1_9_with_using_boost_button_and_free_bets_for_inplay_events_with_quickbet_functionality(self):
        """
        DESCRIPTION: Repeat steps 1-9 with using Boost button and Free bets for Inplay events with Quickbet functionality
        EXPECTED: 
        """
        pass

    def test_011_log_out_from_the_appilication(self):
        """
        DESCRIPTION: Log out from the appilication
        EXPECTED: User should be logged out
        """
        pass

    def test_012_repeat_steps_1_11except_step4_and_follow_below_steps_for_the_logged_out_user(self):
        """
        DESCRIPTION: Repeat steps 1-11(except step4) and follow below steps for the Logged out user
        EXPECTED: 
        """
        pass

    def test_013_in_application_tap_log_in__bet_buttonfrom_ox99button_namecoral_login__place_betladbrokes_login_and_place_bet(self):
        """
        DESCRIPTION: In application: Tap 'Log In & Bet' button
        DESCRIPTION: From OX99
        DESCRIPTION: Button name:
        DESCRIPTION: Coral: 'Login & Place Bet'
        DESCRIPTION: Ladbrokes: 'Login and Place bet
        EXPECTED: 'Log In' pop-up is opened
        """
        pass

    def test_014_log_in_with_user_with_positive_balance_that_will_cover_stake_amount_entered_in_step_3_and_no_pop_ups_are_expected_after_login(self):
        """
        DESCRIPTION: Log in with user with positive balance that will cover Stake amount (entered in Step 3) and NO pop-ups are expected after login
        EXPECTED: * Spinner + Count down timer is displayed on clicking on 'Place bet' for a few seconds
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User balance is decreased by stake entered on step #3
        """
        pass
