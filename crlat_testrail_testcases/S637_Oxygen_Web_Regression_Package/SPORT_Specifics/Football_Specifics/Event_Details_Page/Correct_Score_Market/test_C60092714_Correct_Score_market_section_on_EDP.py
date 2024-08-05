import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60092714_Correct_Score_market_section_on_EDP(Common):
    """
    TR_ID: C60092714
    NAME: Correct Score market section on EDP
    DESCRIPTION: This test case verifies Correct Score market section on EDP.
    DESCRIPTION: Correct score: add option to allow 'Any Other' score selection
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Data should be available for Correct Score with H/D/A - Any other.
    """
    keep_browser_open = True

    def test_001_navigate_to_sport_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Navigate to <Sport> Event Details page of Football event
        EXPECTED: <Sport> Event Details page is opened successfully representing available markets
        """
        pass

    def test_002_go_to_correct_score_market_section(self):
        """
        DESCRIPTION: Go to 'Correct Score' market section
        EXPECTED: *   Section is present on Event Details Page
        EXPECTED: *   It is possible to collapse/expand section
        """
        pass

    def test_003_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If Correct Score has **cashoutAvail="Y"** on Market level then label Cash out is displayed
        """
        pass

    def test_004_expand_correct_score_market_section(self):
        """
        DESCRIPTION: Expand 'Correct Score' market section
        EXPECTED: Section consists of:
        EXPECTED: *   Two pickers (<Home Team> <Away Team>)
        EXPECTED: *   **Price/Odds** button with associated price
        EXPECTED: *   **'Show All' **option with all Correct Score outcomes
        EXPECTED: *   Lowest available goals number for each team is selected by default
        """
        pass

    def test_005_verify_home_team___away_team_pickers(self):
        """
        DESCRIPTION: Verify <Home Team> - <Away Team> pickers
        EXPECTED: *   Each drop down contain goal numbers (e.g. 0,1,2,3,4,5,6,7,8,9...)
        EXPECTED: *   The min/max goal numbers in drop-down is taken from SS
        """
        pass

    def test_006_clicktap_on_show_all_option(self):
        """
        DESCRIPTION: Click/Tap on 'Show All' option
        EXPECTED: *   All Correct Score outcomes are present
        EXPECTED: *   Outcomes are ordered in three columns (<Home Team> <Draw> <Away Team>)
        EXPECTED: *   Button name is changed to 'Show less'
        """
        pass

    def test_007_verify_selections_displaying_for_markets(self):
        """
        DESCRIPTION: Verify selections displaying for markets
        EXPECTED: *   selection of 'Home Team' are shown on the left side
        EXPECTED: *   selection of 'Draw' are shown in the middle
        EXPECTED: *   selection of 'Away Team' are shown on the right side
        EXPECTED: *   If any outcome is not available in SS - it is not shown
        """
        pass

    def test_008_verify_any_other_selections_displaying(self):
        """
        DESCRIPTION: Verify Any other selections displaying
        EXPECTED: *   selection of 'Home Any other' are shown on the bottom left side
        EXPECTED: *   selection of 'Draw Any other' are shown in the middle bottom
        EXPECTED: *   selection of 'Away Any other' are shown on the bottom right side
        EXPECTED: *   If any outcome is not available in SS - it is not shown
        """
        pass

    def test_009_verify_selections_sortening(self):
        """
        DESCRIPTION: Verify selections sortening
        EXPECTED: Selection are sorted by Team score (**outcomeMeaningScores** attribute) from lowest to highest
        """
        pass

    def test_010_clicktap_on_show_less_button(self):
        """
        DESCRIPTION: Click/Tap on 'Show Less' button
        EXPECTED: *   Section with Correct Score outcomes is collapsed
        EXPECTED: *   Button name is changed to 'Show All'
        """
        pass
