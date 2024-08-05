import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C862022_Price_change_while_placing_a_bet_with_delay_on_an_In_Play_event(Common):
    """
    TR_ID: C862022
    NAME: Price change while placing a bet with delay on an In-Play event
    DESCRIPTION: Verify live updates (price change) while placing a bet with delay on an In-Play event
    DESCRIPTION: AUTOTEST: [C2352380]
    PRECONDITIONS: - 'BIR Delay' may be set on each hierarchy level in OB System (except Selection)
    PRECONDITIONS: - The highest set 'BIR Delay' value (applicable to a <Sport> selection) is used in "confirmationExpectedAt" attribute in "placeBet" response
    PRECONDITIONS: - In-Play events are available in application
    PRECONDITIONS: - Make sure you have a user account with positive balance
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Application is opened
        """
        pass

    def test_002_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in
        """
        pass

    def test_003_add_a_selections_to_the_betslip_from_any_in_play_sport_event__open_betslip(self):
        """
        DESCRIPTION: Add a selection(s) to the Betslip from any In-Play <Sport> event > Open Betslip
        EXPECTED: Added selection(s) is(are) displayed within Betslip
        """
        pass

    def test_004_in_ti_add_bir_delay_value_applicable_to_an_added_in_play_sport_selection(self):
        """
        DESCRIPTION: In TI: Add 'BIR Delay' value applicable to an added In-Play <Sport> selection
        EXPECTED: 'BIR Delay' is added
        """
        pass

    def test_005_in_applicationbetslip_enter_any_stake_value_for_selections_with_set_bir_delay(self):
        """
        DESCRIPTION: In application/Betslip: Enter any Stake value for selection(s) with set 'BIR Delay'
        EXPECTED: Entered value is displayed in 'Stake' field
        """
        pass

    def test_006_tap_place_bet_button_and_in_ti_trigger_price_change_for_a_selection_with_set_bir_delay_while_bet_is_being_processed(self):
        """
        DESCRIPTION: Tap 'Place bet' button and in TI: Trigger price change for a selection with set 'BIR Delay' while bet is being processed
        EXPECTED: - Bet placement process starts automatically
        EXPECTED: - Notification "Please wait while your bet is being placed" appears on the yellow background above the Betslip footer
        EXPECTED: - Notification box is displayed at the top of the betslip with animations 'Some of the prices have changed' - this is removed after 5 seconds (on Ladbrokes only)
        EXPECTED: - Spinner with countdown timer in format XX:XX appear on the green button (countdown timer is taken from "placeBet" response: "confirmationExpectedAt" attribute value)
        """
        pass

    def test_007_verify_betslip_once_processing_bet_time_is_up(self):
        """
        DESCRIPTION: Verify Betslip once processing bet time is up
        EXPECTED: - Notification "Please wait while your bet is being placed" disappears
        EXPECTED: - Warning message 'Some of the prices have changed' appears
        EXPECTED: - Spinner icon with countdown timer is replaced by 'Accept & Place bet (#)' label
        EXPECTED: - 'Accept & Place bet(#)' button is enabled
        EXPECTED: ![](index.php?/attachments/get/122292581)
        """
        pass

    def test_008_tap_on_accept__place_bet__button(self):
        """
        DESCRIPTION: Tap on 'Accept & Place bet (#)' button
        EXPECTED: - Bet placement process starts automatically
        EXPECTED: - Notification "Please wait while your bet is being placed" appears on the yellow background above the Betslip footer
        EXPECTED: - Spinner with countdown timer in format XX:XX appear on the green button (countdown timer is taken from "placeBet" response: "confirmationExpectedAt" attribute value)
        EXPECTED: - Once time is up the bet is successfully processed
        """
        pass

    def test_009_tap_x_on_bet_receipt(self):
        """
        DESCRIPTION: Tap 'X' on 'Bet Receipt'
        EXPECTED: Betslip is closed
        """
        pass

    def test_010_repeat_steps_1_9_for_different_types_of_bets_and_different_sports(self):
        """
        DESCRIPTION: Repeat steps 1-9 for different types of bets and different sports
        EXPECTED: 
        """
        pass
