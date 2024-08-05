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
class Test_C60092720_Market_with_meaningMinor_code_CS_Any_other_selection_on_EDP(Common):
    """
    TR_ID: C60092720
    NAME: Market with  meaningMinor code 'CS'- Any other selection on EDP.
    DESCRIPTION: This test case verifies Correct Score market section on EDP.
    DESCRIPTION: Correct score: add option to allow 'Any Other' score selection
    DESCRIPTION: List of Correct score markets such as (Market sort "correct score" and Display sort "CS") :
    DESCRIPTION: Correct score
    DESCRIPTION: Set Betting
    DESCRIPTION: Set X correct score
    DESCRIPTION: Current Game correct score
    DESCRIPTION: Next game correct score
    DESCRIPTION: Current set correct score
    DESCRIPTION: Next set correct score
    DESCRIPTION: Current set score after X games
    DESCRIPTION: Next set score after X games
    DESCRIPTION: Tie break correct score
    DESCRIPTION: Match tie correct score
    DESCRIPTION: Match tie break correct score
    DESCRIPTION: Match correct score
    DESCRIPTION: Game X correct score
    DESCRIPTION: X innings correct score
    DESCRIPTION: Xth innings correct score
    DESCRIPTION: Series correct score
    DESCRIPTION: Correct match score
    DESCRIPTION: xth set correct score
    DESCRIPTION: Best of X correct score
    DESCRIPTION: Map X correct round score
    DESCRIPTION: Extra time correct score
    DESCRIPTION: First half correct score
    DESCRIPTION: Second half correct score
    DESCRIPTION: Extra time half time correct score
    DESCRIPTION: Any Time correct score
    DESCRIPTION: Correct score betting
    DESCRIPTION: Frame X-X correct score
    DESCRIPTION: X set correct score
    DESCRIPTION: Set X correct score
    DESCRIPTION: Period X correct score
    DESCRIPTION: X Period correct score
    DESCRIPTION: Correct score X mins
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Data should be available for Correct Score with H/D/A - Any other.
    PRECONDITIONS: From OB :
    PRECONDITIONS: Create and selection with name 'Any Other' and selection type - 'home-other'
    """
    keep_browser_open = True

    def test_001_navigate_to_ltsportgt_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Navigate to &lt;Sport&gt; Event Details page of Football event
        EXPECTED: &lt;Sport&gt; Event Details page is opened successfully representing available markets
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
        EXPECTED: *   Two pickers (&lt;Home Team&gt; &lt;Away Team&gt;)
        EXPECTED: *   **Price/Odds** button with associated price
        EXPECTED: *   **'Show All' **option with all Correct Score outcomes
        EXPECTED: *   Lowest available goals number for each team is selected by default
        """
        pass

    def test_005_verify_lthome_teamgt___ltaway_teamgt_pickers(self):
        """
        DESCRIPTION: Verify &lt;Home Team&gt; - &lt;Away Team&gt; pickers
        EXPECTED: *   Each drop down contain goal numbers (e.g. 0,1,2,3,4,5,6,7,8,9...)
        EXPECTED: *   The min/max goal numbers in drop-down is taken from SS
        """
        pass

    def test_006_clicktap_on_show_all_option(self):
        """
        DESCRIPTION: Click/Tap on 'Show All' option
        EXPECTED: *   All Correct Score outcomes are present
        EXPECTED: *   Outcomes are ordered in three columns (&lt;Home Team&gt; &lt;Draw&gt; &lt;Away Team&gt;)
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

    def test_011_add_any_any_other_selection_to_betslip(self):
        """
        DESCRIPTION: Add any Any other selection to Betslip.
        EXPECTED: Selection should be added successfully
        """
        pass

    def test_012_click_on_place_betverify_bet_receipt(self):
        """
        DESCRIPTION: Click on Place Bet
        DESCRIPTION: Verify Bet receipt
        EXPECTED: Bet should be placed and Bet receipt is displayed.
        """
        pass
