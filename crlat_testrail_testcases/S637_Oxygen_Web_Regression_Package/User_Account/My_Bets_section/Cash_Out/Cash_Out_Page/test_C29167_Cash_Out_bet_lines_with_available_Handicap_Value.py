import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C29167_Cash_Out_bet_lines_with_available_Handicap_Value(Common):
    """
    TR_ID: C29167
    NAME: Cash Out bet lines with available Handicap Value
    DESCRIPTION: This test case verifies Cash Out bet lines with available Handicap Value.
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-5049 Handicap Value should be taken from handicapValueDec in SS
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed a bet on Pre Match or In-Play match (Singles and Multiple bets) where Cash Out offer is available (on SS see cashoutAvail="Y" on Event and Market level to be sure whether COMB option is available);
    PRECONDITIONS: *   Make sure user has placed Singles and Multiple bets with available handicap value.
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: See attributes: **'handicapValueDec'** on outcome level - to see whether handicap value is available for outcome
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: 'Cash Out' tab is opened
        """
        pass

    def test_002_go_to_verified_single_cash_outbet_line(self):
        """
        DESCRIPTION: Go to verified **Single** Cash Out bet line
        EXPECTED: 
        """
        pass

    def test_003_verify_selection_name(self):
        """
        DESCRIPTION: Verify Selection Name
        EXPECTED: Selection Name contains handicap value in it
        """
        pass

    def test_004_verify_the_handicap_value(self):
        """
        DESCRIPTION: Verify the handicap value
        EXPECTED: *   Handicap value corresponds to the **'handicapValueDec'** from the Site Server response
        EXPECTED: *   Handicap value is displayed directly to the right of the outcome names in parentheses (e.g. <Outcome Name> (handicap value))
        """
        pass

    def test_005_verify_sign_for_handicap_value(self):
        """
        DESCRIPTION: Verify sign for handicap value
        EXPECTED: *   If **'handicapValueDec'** contains '-' sign - display it with this '-' sign (negative value) on the front end
        EXPECTED: *   If **'handicapValueDec'** contains '+' sign in the response - display '+' sign before the value on front end
        EXPECTED: *   If **'handicapValueDec'** doesn't contain any sign (e.g. 2) - display '+' sign before the value on the front end
        """
        pass

    def test_006_go_to_verifiedmultiple_cash_outbet_line(self):
        """
        DESCRIPTION: Go to verified **Multiple** Cash Out bet line
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_3_5(self):
        """
        DESCRIPTION: Repeat steps #3-5
        EXPECTED: 
        """
        pass
