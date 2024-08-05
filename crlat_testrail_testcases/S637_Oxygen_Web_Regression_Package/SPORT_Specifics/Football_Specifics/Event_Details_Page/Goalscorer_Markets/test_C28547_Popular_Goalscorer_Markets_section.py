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
class Test_C28547_Popular_Goalscorer_Markets_section(Common):
    """
    TR_ID: C28547
    NAME: Popular Goalscorer Markets section
    DESCRIPTION: This test case verifies Popular Goalscorer Markets section on Football Event Details pages.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with goalscorer markets (First Goalscorer, Anytime Goalscorer, Goalscorer - 2 or more)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Anytime Goalscorer"
    PRECONDITIONS: *   PROD: name="Goal Scorer - Anytime"
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

    def test_003_go_to_popular_goalscorer_markets_section(self):
        """
        DESCRIPTION: Go to 'Popular Goalscorer Markets' section
        EXPECTED: *   Section is present on Event Details Page and titled ‘Popular Goalscorer Markets’
        EXPECTED: *   It is possible to collapse/expand section
        """
        pass

    def test_004_verify_cash_out_label_next_to_goalscorer_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Goalscorer Market section name
        EXPECTED: If one of markets (First Goalscorer/Anytime Goalscorer/Goalscorer-2 or More) has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        pass

    def test_005_expand_popular_goalscorer_markets_section(self):
        """
        DESCRIPTION: Expand 'Popular Goalscorer Markets' section
        EXPECTED: Section consists of:
        EXPECTED: *   Team selector
        EXPECTED: *   ‘Players’ column with players names of corresponding team
        EXPECTED: *   ‘1st’, ‘Anytime’ and ‘2 or More’ columns with price/odds buttons
        EXPECTED: *   ‘No goalscorer’ line at the end of the list if available (note - 'No goalscorer' selection is NOT applicable to '2 or More' market)
        """
        pass

    def test_006_verify_team_selector(self):
        """
        DESCRIPTION: Verify Team selector
        EXPECTED: Team selector is represented by two buttons with teams names:
        EXPECTED: *   <Home team name> is selected by default
        EXPECTED: *   <Away team name>
        EXPECTED: Selected button is highlighted accordingly.
        """
        pass

    def test_007_verify_players_column_content(self):
        """
        DESCRIPTION: Verify ‘Players’ column content
        EXPECTED: 1) All outcomes with attribute:
        EXPECTED: *   **outcomeMeaningMinorCode="H"** (if <Home Team> is selected)
        EXPECTED: OR
        EXPECTED: *   **outcomeMeaningMinorCode="A" **(if <Away Team> is selected)
        EXPECTED: of first available goalscorer market for event in SS are shown ('First Goalscorer', 'Anytime Goalscorer', 'Goalscorer - 2 or More' in respective order)
        EXPECTED: 2) Outcome with attribute** outcomeMeaningMinorCode="N" **is shown at the end of the list if available
        """
        pass

    def test_008_verify_popular_goalscorer_markets_section_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify 'Popular Goalscorer Markets' section in case of data absence
        EXPECTED: 'Popular Goalscorer Markets' section is not shown if:
        EXPECTED: *   all markets that section consists of are absent
        EXPECTED: *   all markets that section consists of do not have any outcomes
        """
        pass
