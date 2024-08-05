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
class Test_C28548_Other_Goalscorer_Markets_section(Common):
    """
    TR_ID: C28548
    NAME: Other Goalscorer Markets section
    DESCRIPTION: This test case verifies Other Goalscorer Markets section on Football Event Details pages.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with goalscorer markets (Last Goalscorer, Hat trick)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Hat trick"
    PRECONDITIONS: *   PROD: name="Goal Scorer - Hat-Trick"
    PRECONDITIONS: **Jira tickets: **BMA-3868
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

    def test_003_go_to_other_goalscorer_markets_section(self):
        """
        DESCRIPTION: Go to 'Other Goalscorer Markets' section
        EXPECTED: *   Section is present on Event Details Page and titled ‘Other Goalscorer Markets’
        EXPECTED: *   It is possible to collapse/expand section
        """
        pass

    def test_004_verify_cash_out_label_next_to_market_seection_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market seection name
        EXPECTED: If one of markets (Last Goalscorer/Hat trick) has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        pass

    def test_005_expand_other_goalscorer_markets_section(self):
        """
        DESCRIPTION: Expand 'Other Goalscorer Markets' section
        EXPECTED: Section consists of:
        EXPECTED: *   Team selector
        EXPECTED: *   ‘Players’ column with players names of corresponding team
        EXPECTED: *   ‘Last’ and ‘Hatrick’ columns with price/odds buttons
        EXPECTED: *   ‘No goalscorer’ line in the end of the list if available
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

    def test_007_verify_players_column_content_when_home_team_is_selected(self):
        """
        DESCRIPTION: Verify ‘Players’ column content when <Home team> is selected
        EXPECTED: 1) All outcomes with attribute:
        EXPECTED: *   **outcomeMeaningMinorCode="H"** (if <Home Team> is selected)
        EXPECTED: OR
        EXPECTED: *   **outcomeMeaningMinorCode="A" **(if <Away Team> is selected)
        EXPECTED: of first available goalscorer market are shown ('Last Goalscorer', 'Hat trick' in respective order)
        EXPECTED: 2) Outcome with attribute** outcomeMeaningMinorCode="N" **is shown in the end of the list if available
        """
        pass

    def test_008_verify_other_goalscorer_markets_section_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify 'Other Goalscorer Markets' section in case of data absence
        EXPECTED: 'Other Goalscorer Markets' section is not shown if:
        EXPECTED: *   all markets that section consists of are absent
        EXPECTED: *   all markets that section consists of do not have any outcomes
        """
        pass
