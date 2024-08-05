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
class Test_C28526_First_Second_Half_Correct_Score_market_section(Common):
    """
    TR_ID: C28526
    NAME: First/Second Half Correct Score market section
    DESCRIPTION: This test case verifies First/Second Half Correct Score market sections.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First Half Correct Score"
    PRECONDITIONS: *   PROD: name="1st Half Correct Score"
    PRECONDITIONS: **Jira ticket: **BMA-3861
    PRECONDITIONS: Data should be available for Correct Score with H/D/A - Any other.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        pass

    def test_003_go_to_first_halfcorrect_score_market_section(self):
        """
        DESCRIPTION: Go to 'First Half Correct Score' market section
        EXPECTED: *   Section is present on Event Details Page (e.g. All Markets tab)
        EXPECTED: *   It is possible to collapse/expand section
        """
        pass

    def test_004_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If Correct Score has **cashoutAvail="Y"** then label Cash out should be displayed next to market section name
        """
        pass

    def test_005_expand_first_halfcorrect_score_market_section(self):
        """
        DESCRIPTION: Expand 'First Half Correct Score' market section
        EXPECTED: Section consists of:
        EXPECTED: *   Two pickers (&lt;Home Team&gt; &lt;Away Team&gt;)
        EXPECTED: *   **'Add to Betslip'** button with associated price
        EXPECTED: *   **'Show All' **option with all Correct Score outcomes
        EXPECTED: *   Lowest available goals number for each team is selected by default
        """
        pass

    def test_006_verify_lthome_teamgt___ltaway_teamgt_pickers(self):
        """
        DESCRIPTION: Verify &lt;Home Team&gt; - &lt;Away Team&gt; pickers
        EXPECTED: *   Each drop down contain goal numbers (e.g. 0,1,2,3,4,5,6,7,8,9...)
        EXPECTED: *   The min/max goal numbers in drop-down is taken from SS
        """
        pass

    def test_007_clicktap_show_all_option(self):
        """
        DESCRIPTION: Click/Tap 'Show All' option
        EXPECTED: *   All Correct Score outcomes are present
        EXPECTED: *   Outcomes are ordered in three columns (&lt;Home Team&gt; &lt;Draw&gt; &lt;Away Team&gt;)
        EXPECTED: *   Button name is changed to 'Show less'
        """
        pass

    def test_008_verify_selections_displaying_for_markets(self):
        """
        DESCRIPTION: Verify selections displaying for markets
        EXPECTED: *   selection of 'Home Team' are shown on the left side
        EXPECTED: *   selection of 'Draw' are shown in the middle
        EXPECTED: *   selection of 'Away Team are shownon the right side
        EXPECTED: *   If any outcome is not available in SS - it is not shown
        """
        pass

    def test_009_verify_any_other_selections_displaying(self):
        """
        DESCRIPTION: Verify Any other selections displaying
        EXPECTED: *   selection of 'Home Any other' are shown on the bottom left side
        EXPECTED: *   selection of 'Draw Any other' are shown in the middle bottom
        EXPECTED: *   selection of 'Away Any other' are shown on the bottom right side
        EXPECTED: *   If any outcome is not available in SS - it is not shown
        """
        pass

    def test_010_verify_selections_sortening(self):
        """
        DESCRIPTION: Verify selections sortening
        EXPECTED: Selection are sorted by Team score (**outcomeMeaningScores** attribute) from lowest to highest
        """
        pass

    def test_011_clicktap_show_less_button(self):
        """
        DESCRIPTION: Click/Tap 'Show Less' button
        EXPECTED: *   Section with Correct Score outcomes is collapsed
        EXPECTED: *   Button name is changed to 'Show All'
        """
        pass

    def test_012_verify_first_halfcorrect_score_section_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify 'First Half Correct Score' section in case of data absence
        EXPECTED: 'First Half Correct Score' section is not shown if:
        EXPECTED: *   all markets of that section are absent
        EXPECTED: *   all outcomes of that section are absent
        """
        pass

    def test_013_repeat_3_11_steps_for_second_half_correct_score_market_section(self):
        """
        DESCRIPTION: Repeat 3-11 steps for 'Second Half Correct Score' market section
        EXPECTED: 
        """
        pass
