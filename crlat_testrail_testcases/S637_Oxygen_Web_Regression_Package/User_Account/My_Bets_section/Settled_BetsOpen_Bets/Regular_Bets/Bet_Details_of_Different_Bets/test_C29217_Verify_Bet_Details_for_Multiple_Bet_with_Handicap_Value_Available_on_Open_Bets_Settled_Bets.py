import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C29217_Verify_Bet_Details_for_Multiple_Bet_with_Handicap_Value_Available_on_Open_Bets_Settled_Bets(Common):
    """
    TR_ID: C29217
    NAME: Verify Bet Details for Multiple Bet with Handicap Value Available on Open Bets/Settled Bets
    DESCRIPTION: This test case verifies Bet Details for Multiple Bet if selections have handicap value availabl
    DESCRIPTION: AUTOTEST [C9697980]
    PRECONDITIONS: 1. User should be logged in
    PRECONDITIONS: 2. User has placed a multiple bet with Handicap
    PRECONDITIONS: 3. User has a settled multiple bet with Handicap
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'handicapValueDec' **on outcome level- to see whether handicap value is available for outcome
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tabverify_bet_details_for_multiple_bet_with_handicap_value_available(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab
        DESCRIPTION: Verify bet details for Multiple Bet with Handicap Value Available
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type
        EXPECTED: * Selection name user has bet on and handicap value e.g. Tie (+2.0)
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Tie (+3.0) @1/4)
        EXPECTED: * Market name user has bet on - e.g., "Match Result & Both Teams to Score"
        EXPECTED: * Event name and event start date and time in DD MM, HH:MM format using 12-hour clock (AM/PM) (e.g. 05 Jan, 1:49PM)
        EXPECTED: * The above described details are shown for each selection, included in the multiple, one under another
        EXPECTED: At the bottom of the multiple section the following details are shown:
        EXPECTED: * Stake value <currency symbol> <value> (e.g., £30.00)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass

    def test_002_verify_event_name_and_associated_event_type_for_each_section(self):
        """
        DESCRIPTION: Verify Event name and associated event type for each section
        EXPECTED: *   Event name and associated event type are hyperlinked
        EXPECTED: *   User is navigated to Event Details page after tapping Event name
        EXPECTED: **Note:** Event name is NOT hyperlinked if bet was placed on selections from Enhanced Multiples market
        """
        pass

    def test_003_verify_handicap_value_correctness(self):
        """
        DESCRIPTION: Verify handicap value correctness
        EXPECTED: Handicap value corresponds to the **'handicapValueDec'** from the Site Server response
        """
        pass

    def test_004_verify_the_handicap_value_displaying(self):
        """
        DESCRIPTION: Verify the handicap value displaying
        EXPECTED: Handicap value is displayed directly to the right of the outcome names
        EXPECTED: Handicap value is displayed in parentheses
        EXPECTED: (e.g. <Outcome Name> (handicap value))
        """
        pass

    def test_005_verify_sign_for_handicap_value(self):
        """
        DESCRIPTION: Verify sign for handicap value
        EXPECTED: *   If **'handicapValueDec' **contains '-' sign - display it with this '-' sign (negative value) on the front end
        EXPECTED: *   If **'handicapValueDec'** contains '+' sign in the response - display '+' sign before the value on front end
        EXPECTED: *   If **'handicapValueDec'** doesn't contain any sign (e.g. 2) - display '+' sign before the value on the front end
        """
        pass

    def test_006_navigate_to_settled_bets_tabrepeat_steps_1_5verify_that_bet_details_for_settled_single_bet_with_handicap_value_available(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab
        DESCRIPTION: Repeat steps 1-5
        DESCRIPTION: Verify that bet details for settled Single Bet with Handicap Value Available
        EXPECTED: The appropriate information for settled multiple bet with handicap is shown on 'Settled Bets' tab
        """
        pass
