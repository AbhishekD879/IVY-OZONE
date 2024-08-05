import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C861981_Sport_selection_suspended_while_placing_a_bet_with_BIR_delay_on_an_In_Play_event(Common):
    """
    TR_ID: C861981
    NAME: <Sport> selection suspended while placing a bet with BIR delay on an In-Play event
    DESCRIPTION: Verify live updates (<Sport> selection suspended) while placing a bet with delay on an In-Play event
    DESCRIPTION: AUTOTEST: [C2610574]
    PRECONDITIONS: - 'BIR Delay' is set ('BIR Delay' may be set on each hierarchy level in OB System (except for Selection))
    PRECONDITIONS: - The highest set 'BIR Delay' value (applicable to a <Sport> selection) is used in "confirmationExpectedAt" attribute in "placeBet" response
    PRECONDITIONS: - In-Play events are available in application
    PRECONDITIONS: - Make sure you have a user account with positive balance
    """
    keep_browser_open = True

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_a_selection_with_bir_delay_to_the_betslip_from_any_in_play_sport_event_and_open_the_betslip(self):
        """
        DESCRIPTION: Add a selection with BIR delay to the Betslip from any In-Play <Sport> event and Open the Betslip
        EXPECTED: Added selection is displayed within Betslip
        """
        pass

    def test_003_enter_stake_for_selection_with_set_bir_delay(self):
        """
        DESCRIPTION: Enter Stake for selection with set 'BIR Delay'
        EXPECTED: Entered value is displayed in 'Stake' field
        """
        pass

    def test_004_tap_bet_now_buttonfrom_ox99button_namecoral_and_ladbrokes_place_bet(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        DESCRIPTION: **From OX99**
        DESCRIPTION: Button name:
        DESCRIPTION: Coral and Ladbrokes: 'Place Bet'
        EXPECTED: - Bet placement process starts automatically
        EXPECTED: - Notification "Please wait while your bet is being placed" appears on the yellow background above the Betslip footer
        EXPECTED: - Spinner with countdown timer in format XX:XX appear on the green button (countdown timer is taken from "placeBet" response: "confirmationExpectedAt" attribute value)
        """
        pass

    def test_005_in_ti_suspend_outcome_with_set_bir_delay_while_bet_is_being_processed(self):
        """
        DESCRIPTION: In TI: Suspend outcome with set 'BIR Delay' while bet is being processed
        EXPECTED: Outcome becomes suspended
        """
        pass

    def test_006_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * Count down timer is still displayed on green button
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections has been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * Count down timer is still displayed on green button
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended'
        EXPECTED: * Notification "Please wait while your bet is being placed"
        EXPECTED: ![](index.php?/attachments/get/122292573)
        """
        pass

    def test_007_verify_betslip_once_processing_bet_time_is_up(self):
        """
        DESCRIPTION: Verify Betslip once processing bet time is up
        EXPECTED: - Notification "Please wait while your bet is being placed" disappears
        EXPECTED: - Spinner icon with countdown timer is replaced by 'Place bet' label
        EXPECTED: - 'Place Bet' button is disabled
        EXPECTED: ![](index.php?/attachments/get/122292574)
        """
        pass
