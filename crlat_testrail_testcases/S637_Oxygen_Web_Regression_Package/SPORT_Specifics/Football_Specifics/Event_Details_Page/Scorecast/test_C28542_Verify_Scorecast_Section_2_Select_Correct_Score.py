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
class Test_C28542_Verify_Scorecast_Section_2_Select_Correct_Score(Common):
    """
    TR_ID: C28542
    NAME: Verify Scorecast Section 2 (Select Correct Score)
    DESCRIPTION: This test case verifies the functionality of Scorecast market section within Football event details page.
    PRECONDITIONS: 1) In order to run this test scenario select event with market name "First Goal Scorecast" and/or "Last Goal Scorecast"
    PRECONDITIONS: 2) To get information for an event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_open_football_event_detail_page(self):
        """
        DESCRIPTION: Open Football Event Detail Page
        EXPECTED: Football Event Details page is opened
        """
        pass

    def test_002_go_to_scorecast_market_section(self):
        """
        DESCRIPTION: Go to Scorecast market section
        EXPECTED: Scorecast market section is present and shown after 'Correct Score' market
        """
        pass

    def test_003_verify_section_2_select_result(self):
        """
        DESCRIPTION: Verify section 2 (Select Result)
        EXPECTED: Section 2 consists of:
        EXPECTED: * 'Correct Score' drop down
        EXPECTED: * Lowest available goals number for each team is selected by default (0, 0)
        EXPECTED: * 'Odds calculation' button is displayed as greyed out with 'N/A' inscription if selected combination of outcomes is not valid
        EXPECTED: * 'Odds calculation' button is displayed with appropriate price button when goals are selected in both dropdowns
        """
        pass

    def test_004_verify_correct_score_drop_downs(self):
        """
        DESCRIPTION: Verify 'Correct Score' drop downs
        EXPECTED: * Each drop down contain goal numbers (e.g. 0,1,2,3,4,5,6,7,8,9...)
        EXPECTED: * Goal numbers are displayed numerically **from lowest score to highest**
        EXPECTED: * The min/max goal numbers in drop-down is taken from SS
        EXPECTED: * Combinations of goals are received from OB in  attributes that are present on the outcome level in format: **outcomeMeaningScores="X,Y," **
        EXPECTED: where X - score belongs to Home team, Y - to Away team
        """
        pass
