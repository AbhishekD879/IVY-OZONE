import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C49299411_Place_bet_via_Quick_Bet_Races(Common):
    """
    TR_ID: C49299411
    NAME: Place bet via Quick Bet (Races)
    DESCRIPTION: This test case verifies placing bet by using Quick Bet for races (Horse racing, Greyhounds - SP/LP prices)
    DESCRIPTION: NOTE! Quick Bet is NOT present for Desktop
    PRECONDITIONS: 1. Quick Bet functionality is enabled in CMS and user`s settings
    PRECONDITIONS: 2. Load the app
    PRECONDITIONS: 3. Log in with a user that has a positive balance
    PRECONDITIONS: 4. Navigate to any racing landing page (for example, Horse racing or Greyhounds)
    """
    keep_browser_open = True

    def test_001_add_any_race_lpsp_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add any <Race> LP/SP selection to Quick Bet
        EXPECTED: Quick Bet is displayed at the bottom of the page:
        EXPECTED: * Quick Bet header and 'X' button
        EXPECTED: * Selection name, Market name and Event name
        EXPECTED: * 'Use Freebet' under event details (if available)
        EXPECTED: * Quick Stakes (For example, "+£5", "+£10" "+£50", "+£100")
        EXPECTED: * Price odds 'SP' or 'LP' and Stake box
        EXPECTED: * The button 'Add to betslip' is active and 'Place bet' is disabled
        EXPECTED: * E/W box
        EXPECTED: * 'Boost' button (if available, for LP)
        EXPECTED: * 'Total Stake', 'Estimated Returns' - Coral, 'Total Stake', 'Potential Returns' - Ladbrokes
        EXPECTED: Please note that some prices can be switched between SP/LP (it depends on set up in backoffice)
        EXPECTED: ![](index.php?/attachments/get/58771202)![](index.php?/attachments/get/58771203)
        """
        pass

    def test_002_tap_on_the_stake_field___enter_any_value(self):
        """
        DESCRIPTION: Tap on the 'Stake' field &  enter any value
        EXPECTED: * The keyboard appears
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Total Stake', 'Estimated Returns'  (Coral), 'Total Stake', 'Potential Returns' (Ladbrokes) are calculated
        EXPECTED: * The buttons 'Add to betslip' and 'Place bet' are active
        EXPECTED: * The 'Boost' button is active and can be boosted (if available)
        EXPECTED: Please note The keyboard doesn't appear when using 'Quick Stake' buttons
        """
        pass

    def test_003_check_the_ew_box(self):
        """
        DESCRIPTION: Check the 'E/W' box
        EXPECTED: * The 'E/W' box is checked
        EXPECTED: * The keyboard is not shown anymore
        """
        pass

    def test_004_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on 'Place bet' button
        EXPECTED: * Spinner is displayed on 'Place bet' for a few seconds
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User balance is decreased by stake entered on step #2
        """
        pass

    def test_005_verify_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Bet Receipt
        EXPECTED: * 'Bet Receipt' header and 'X' button
        EXPECTED: * The message '✓Bet Placed Successfully'
        EXPECTED: * Date and time of the placed bet (format DD/MM/YYYY, HH:MM)
        EXPECTED: * Type of bet @ price odds (for example, Single @ 1/1)
        EXPECTED: * Bet receipt ID
        EXPECTED: * Selection name
        EXPECTED: * Market name/Event name
        EXPECTED: * E/W odds are mentioned with places(for example, 'Each Way Odds 1/2 Places 1-2')
        EXPECTED: * The number of lines are mentioned with stakes(for example, '2 lines at £1 per line')
        EXPECTED: * Cashout label (if available)
        EXPECTED: * Stake & Est. Returns - Coral, Stake for this bet, Potential returns - Ladbrokes
        EXPECTED: * Message 'This bet has been boosted' (if the price was boosted)
        EXPECTED: ![](index.php?/attachments/get/58810503)![](index.php?/attachments/get/58810504)
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
        EXPECTED: The 'Open Bets' tab is opened
        """
        pass

    def test_008_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and verify that the Bet Receipt fields are correct
        EXPECTED: Check the following data correctness:
        EXPECTED: * Type of bet (for example, Single(Each Way))
        EXPECTED: * Selection @ price odds (for example, Adelaide Utd @ 1/1)
        EXPECTED: * Market name with odds and places
        EXPECTED: * Event name
        EXPECTED: * Time of the event in format HH:MM, DD Month(for example, 10:30, 17 Jan)
        EXPECTED: * The currency is as user set during registration
        EXPECTED: * Unit stake, Total Stake, Est. Returns/Potential returns
        EXPECTED: * Full/Partial Cashout buttons - if available
        EXPECTED: * 'Watch'/'Watch Live' label (if the event is live with streaming)
        EXPECTED: * '>' Sign to navigate to event page
        EXPECTED: ![](index.php?/attachments/get/59007990)![](index.php?/attachments/get/58810510)
        """
        pass
