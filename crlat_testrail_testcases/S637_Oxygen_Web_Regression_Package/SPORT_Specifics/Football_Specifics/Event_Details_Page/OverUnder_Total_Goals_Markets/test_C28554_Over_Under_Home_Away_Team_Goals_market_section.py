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
class Test_C28554_Over_Under_Home_Away_Team_Goals_market_section(Common):
    """
    TR_ID: C28554
    NAME: Over/Under <Home/Away Team> Goals market section
    DESCRIPTION: This test case verifies 'Over/Under <Home/Away Team> Goals' market section on Event Details Page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with 'Over/Under <Home/Away Team> Total Goals' markets (Over/Under <Home/Away Team> Total Goals <figure afterward>, Over/Under First Half <Home/Away Team> Total Goals <figure afterward>, Over/Under Second Half <Home/Away Team> Total Goals <figure afterward>)
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
    PRECONDITIONS: **Jira ticket: **BMA-3902
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

    def test_003_go_to_overunder_lthome_teamgt_goals_market_section(self):
        """
        DESCRIPTION: Go to 'Over/Under &lt;Home Team&gt; Goals' market section
        EXPECTED: *   Section is present on Event Details Page and titled ‘Over/Under &lt;Home Team&gt; Goals’
        EXPECTED: *   It is possible to collapse/expand section
        """
        pass

    def test_004_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If one of markets (Over/Under &lt;Home/Away Team&gt; Total Goals &lt;figure afterward&gt;, Over/Under First Half &lt;Home/Away Team&gt; Total Goals &lt;figure afterward&gt;, Over/Under Second Half &lt;Home/Away Team&gt; Total Goals &lt;figure afterward&gt;) has cashoutAvail="Y" then label 'Cash Out' should be displayed next to market section name
        """
        pass

    def test_005_expand_overunder_lthome_teamgt_goals_market_section(self):
        """
        DESCRIPTION: Expand 'Over/Under &lt;Home Team&gt; Goals' market section
        EXPECTED: Section consists of:
        EXPECTED: *   Three buttons: '90 mins' (selected by default), '1st Half', '2nd Half'
        EXPECTED: *   'Total Goals' column with market names
        EXPECTED: *   'Over' and 'Under' columns with price/odds buttons
        EXPECTED: *   First four markets shown by default
        EXPECTED: *   'Show All' button (if more than 4 markets are available)
        """
        pass

    def test_006_verify_overunder_markets_shown_for_90_mins(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '90 mins'
        EXPECTED: *   Only markets with attribute **name="Over/Under &lt;Home Team&gt; Total Goals &lt;figure afterward&gt;" **are present
        EXPECTED: *   If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        pass

    def test_007_verify_overunder_markets_shown_for_1st_half(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '1st Half'
        EXPECTED: *   Only markets with attribute **name="Over/Under First Half &lt;Home Team&gt; Total Goals &lt;figure afterward&gt;" **are present
        EXPECTED: *   If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        pass

    def test_008_verify_overunder_markets_shown_for_2nd_half(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '2nd Half'
        EXPECTED: *   Only markets with attribute **name="Over/Under Second Half &lt;HomeTeam&gt; Total Goals &lt;figure afterward&gt;" **are present
        EXPECTED: *   If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        pass

    def test_009_verify_overunder_lthome_teamgt_goals_section_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify 'Over/Under &lt;Home Team&gt; goals' section in case of data absence
        EXPECTED: 'Over/Under &lt;Home Team&gt; goals' section is not shown if:
        EXPECTED: *   all markets that section consists of are absent
        EXPECTED: *   all markets that section consists of do not have any outcomes
        """
        pass

    def test_010_repeat_steps__4_9_for_overunderltaway_teamgtgoals_market_section(self):
        """
        DESCRIPTION: Repeat steps № 4-9 for 'Over/Under **&lt;Away Team&gt; **Goals' market section
        EXPECTED: 
        """
        pass
