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
class Test_C28557_Verify_ordering_of_markets_within_Over_Under_Total_Goals_sections(Common):
    """
    TR_ID: C28557
    NAME: Verify ordering of markets within Over/Under Total Goals sections
    DESCRIPTION: This test case verifies ordering of markets within Over/Under Total Goals sections ('Over/Under Total Goals', 'Over/Under Total Goals <Home team>', 'Over/Under Total Goals <Away Team>').
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with over/under markets
    PRECONDITIONS: - Over/Under Total Goals: Total Goals Over/Under <figure afterward>, Over/Under First Half <figure afterward>, Over/Under Second Half <figure afterward>
    PRECONDITIONS: - Over/Under Total Goals <Home/Away Team>: Over/Under <Home/Away Team> Total Goals <figure afterward>, Over/Under First Half <Home/Away Team> Total Goals <figure afterward>, Over/Under Second Half <Home/Away Team> Total Goals <figure afterward>
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

    def test_003_go_to_overunder_total_goals_section(self):
        """
        DESCRIPTION: Go to 'Over/Under Total Goals' section
        EXPECTED: *   Section is expanded and shown correctly
        EXPECTED: *   '90 mins' button is selected by default
        EXPECTED: *   First four markets are shown by default within section
        """
        pass

    def test_004_clicktap_show_all_button(self):
        """
        DESCRIPTION: Click/Tap 'Show all' button
        EXPECTED: *   All available markets for selected button (option) are shown
        EXPECTED: *   Button is changed to 'Show less'
        """
        pass

    def test_005_verify_markets_order_within_section(self):
        """
        DESCRIPTION: Verify Markets order within section
        EXPECTED: Markets are ordered from lowest to highest &lt;figure afterward&gt; value of verified markets (e.g. 0.5, 1.5, 2.5 etc)
        """
        pass

    def test_006_repeat_steps_4_5_when_1st_half_button_is_selected(self):
        """
        DESCRIPTION: Repeat steps №4-5 when '1st Half' button is selected
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_4_5_when_2nd_half_button_is_selected(self):
        """
        DESCRIPTION: Repeat steps №4-5 when '2nd Half' button is selected
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_4_7_for_overunder_total_goals_lthome_teamgt_section(self):
        """
        DESCRIPTION: Repeat steps №4-7 for 'Over/Under Total Goals &lt;Home team&gt; section
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_4_7_for_overunder_total_goals_ltaway_teamgt_section(self):
        """
        DESCRIPTION: Repeat steps №4-7 for 'Over/Under Total Goals &lt;Away team&gt; section
        EXPECTED: 
        """
        pass
