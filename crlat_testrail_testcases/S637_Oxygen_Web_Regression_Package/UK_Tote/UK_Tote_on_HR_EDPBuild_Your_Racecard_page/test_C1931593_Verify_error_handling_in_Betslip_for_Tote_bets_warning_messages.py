import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1931593_Verify_error_handling_in_Betslip_for_Tote_bets_warning_messages(Common):
    """
    TR_ID: C1931593
    NAME: Verify error handling in Betslip for Tote bets (warning messages)
    DESCRIPTION: This test case verifies error messages, which are displayed in the betslip for Tote bets in case errors from OpenBet are returned
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User's balance is sufficient to cover the bet stake
    PRECONDITIONS: * Overask is disabled for the user in TI tool
    PRECONDITIONS: * User has added UK Tote bet (any pool type) to the betslip
    PRECONDITIONS: * Betslip is opened
    """
    keep_browser_open = True

    def test_001_tap_bet_now_and_trigger_the_following_errors_from_openbet_tote_bet_error_meeting_cancelled_tote_bet_error_sales_not_opened_tote_bet_error_pool_cancelled(self):
        """
        DESCRIPTION: Tap "BET NOW" and trigger the following errors from OpenBet:
        DESCRIPTION: * TOTE_BET_ERROR_MEETING_CANCELLED
        DESCRIPTION: * TOTE_BET_ERROR_SALES_NOT_OPENED
        DESCRIPTION: * TOTE_BET_ERROR_POOL_CANCELLED
        EXPECTED: * Error message is displayed in the Betslip: **"Sorry, the event has been suspended"**
        EXPECTED: * 'BET NOW' button is disabled
        EXPECTED: * User is able to remove the bet from the Betslip
        """
        pass

    def test_002_tap_bet_now_and_trigger_the_following_errors_from_openbet_tote_bet_error_race_cancelled_tote_bet_error_race_void_tote_bet_error_race_off_tote_bet_error_race_closed(self):
        """
        DESCRIPTION: Tap "BET NOW" and trigger the following errors from OpenBet:
        DESCRIPTION: * TOTE_BET_ERROR_RACE_CANCELLED
        DESCRIPTION: * TOTE_BET_ERROR_RACE_VOID
        DESCRIPTION: * TOTE_BET_ERROR_RACE_OFF
        DESCRIPTION: * TOTE_BET_ERROR_RACE_CLOSED
        EXPECTED: * Error message is displayed in the Betslip: **"Unfortunately, the race has been suspended"**
        EXPECTED: * 'BET NOW' button is disabled
        EXPECTED: * User is able to remove the bet from the Betslip
        """
        pass

    def test_003_tap_bet_now_and_trigger_the_following_errors_from_openbet_tote_bet_error_unit_stake(self):
        """
        DESCRIPTION: Tap "BET NOW" and trigger the following errors from OpenBet:
        DESCRIPTION: * TOTE_BET_ERROR_UNIT_STAKE
        EXPECTED: * Error message is displayed in the Betslip: **"Invalid unit stake, please amend"**
        EXPECTED: * 'BET NOW' button is disabled
        EXPECTED: * User is able to remove the bet from the Betslip
        """
        pass

    def test_004_tap_bet_now_and_trigger_the_following_error_from_openbettote_bet_error_non_runner(self):
        """
        DESCRIPTION: Tap "BET NOW" and trigger the following error from OpenBet:
        DESCRIPTION: TOTE_BET_ERROR_NON_RUNNER
        EXPECTED: * Error message is displayed in the Betslip: **"Chosen selection is now a Non-Runner"**
        EXPECTED: * 'BET NOW' button is disabled
        EXPECTED: * User is able to remove the bet from the Betslip
        """
        pass
