import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28556_Over_Under_Home_Away_Team_Goals_sections_order_in_markets_list(Common):
    """
    TR_ID: C28556
    NAME: Over/Under <Home/Away Team> Goals sections order in markets list
    DESCRIPTION: This test case verifies ordering of 'Over/Under <Home/Away Team> Goals' market sections on Event Details Page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with 'Over/Under <Home/Away Team> Goals' markets (Over/Under <Home/Away Team> Goals <figure afterward>, Over/Under First Half <Home/Away Team> Goals <figure afterward>, Over/Under Second Half  <Home/Away Team> Goals <figure afterward>)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: *   **<figure afterward> **- variable part of market name shown in format 'X.5' as an amount of goals (e.g. 0.5, 1.5, 2.5 etc)
    PRECONDITIONS: *   **<Home Team>** - name of the team that is shown first in the Event Name
    PRECONDITIONS: *   **<Away Team>** - name of the team that is shown second in the Event Name
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Total Goals Over/Under x.x"
    PRECONDITIONS: *   PROD: name="Over/Under Total Goals x.x"
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

    def test_003_go_to_overunder_home_team_goals_section(self):
        """
        DESCRIPTION: Go to 'Over/Under <Home Team> Goals' section
        EXPECTED: Section contains data from the following goalscorer markets:
        EXPECTED: *   Over/Under <Home Team> Goals <figure afterward>
        EXPECTED: *   Over/Under First Half <Home Team> Goals <figure afterward>
        EXPECTED: *   Over/Under Second Half <Home Team> Goals <figure afterward>
        """
        pass

    def test_004_check_displayorder_attribute_values_of_all_markets_available_in_overunder_team_name_goals_section_in_ss_response(self):
        """
        DESCRIPTION: Check '**displayOrder**' attribute values of all markets available in 'Over/Under <Team Name> Goals' section in SS response
        EXPECTED: **Smallest displayOrder** of markets **is set as section's display order**
        """
        pass

    def test_005_check_sections_order_in_markets_list(self):
        """
        DESCRIPTION: Check section's order in markets list
        EXPECTED: Section is ordered by:
        EXPECTED: *   by displayOrder in ascending
        EXPECTED: *   if displayOrder is the same then alphanumerically
        """
        pass

    def test_006_go_to_overunder_away_team_goals_section(self):
        """
        DESCRIPTION: Go to 'Over/Under <Away Team> Goals' section
        EXPECTED: Section contains data from the following goalscorer markets:
        EXPECTED: *   Over/Under <Away Team> Goals <figure afterward>
        EXPECTED: *   Over/Under First Half <Away Team> Goals <figure afterward>
        EXPECTED: *   Over/Under Second Half  <Away Team> Goals <figure afterward>
        """
        pass

    def test_007_verify_location_of_overunder_away_team_goals(self):
        """
        DESCRIPTION: Verify location of 'Over/Under <Away Team> Goals'
        EXPECTED: *   'Over/Under <Away Team> Goals' section is located right after 'Over/Under  <Home Team> Goals'
        EXPECTED: *   If  'Over/Under <Home Team> Goals' is absent repeat step №4-5
        """
        pass
