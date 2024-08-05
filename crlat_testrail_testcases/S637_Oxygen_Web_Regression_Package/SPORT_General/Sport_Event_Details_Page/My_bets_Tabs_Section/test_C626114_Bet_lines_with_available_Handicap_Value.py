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
class Test_C626114_Bet_lines_with_available_Handicap_Value(Common):
    """
    TR_ID: C626114
    NAME: Bet lines with available Handicap Value
    DESCRIPTION: This test case verifies bet lines with available Handicap Value
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed bets on Pre Match or In-Play events (Singles and Multiple bets) with and without available cash out
    PRECONDITIONS: * Make sure user has placed Singles and Multiple bets with available handicap value
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: See attributes: **handicapValueDec** on outcome level - to see whether handicap value is available for outcome
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_single_bet_with_available_cash_out_and_handicap_value(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Single** bet **with** available cash out and handicap value
        EXPECTED: 'My Bets' tab is opened
        """
        pass

    def test_002_verify_selection_name(self):
        """
        DESCRIPTION: Verify Selection Name
        EXPECTED: Selection Name contains handicap value in it
        """
        pass

    def test_003_verify_the_handicap_value(self):
        """
        DESCRIPTION: Verify the handicap value
        EXPECTED: * Handicap value corresponds to the **handicapValueDec** from the Site Server response
        EXPECTED: * Handicap value is displayed directly to the right of the outcome names in parentheses (e.g. <Outcome Name> (handicap value))
        """
        pass

    def test_004_verify_sign_for_handicap_value(self):
        """
        DESCRIPTION: Verify sign for handicap value
        EXPECTED: * If **handicapValueDec** contains '-' sign - display it with this '-' sign (negative value) on the front end
        EXPECTED: * If **handicapValueDec** contains '+' sign in the response - display '+' sign before the value on front end
        EXPECTED: * If **handicapValueDec** doesn't contain any sign (e.g. 2) - display '+' sign before the value on the front end
        """
        pass

    def test_005_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_multiple_bet_with_available_cash_out_and_handicap_value(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Multiple** bet **with** available cash out and handicap value
        EXPECTED: 'My Bets' tab is opened
        """
        pass

    def test_006_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps #2-4
        EXPECTED: Results are the same
        """
        pass

    def test_007_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_single_bet_with_handicap_value_and_without_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Single** bet with handicap value and **without** available cash out
        EXPECTED: 'My Bets' tab is opened
        """
        pass

    def test_008_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps #2-4
        EXPECTED: Results are the same
        """
        pass

    def test_009_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_multiple_bet_with_handicap_value_and_without_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Multiple** bet with handicap value and **without** available cash out
        EXPECTED: 'My Bets' tab is opened
        """
        pass

    def test_010_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps #2-4
        EXPECTED: Results are the same
        """
        pass
