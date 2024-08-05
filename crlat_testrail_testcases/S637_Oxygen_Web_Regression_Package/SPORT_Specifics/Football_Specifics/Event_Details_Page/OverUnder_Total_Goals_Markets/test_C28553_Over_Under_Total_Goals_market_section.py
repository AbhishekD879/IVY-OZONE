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
class Test_C28553_Over_Under_Total_Goals_market_section(Common):
    """
    TR_ID: C28553
    NAME: Over/Under Total Goals market section
    DESCRIPTION: This test case verifies 'Over/Under Total Goals' market section on Event Details Page.
    PRECONDITIONS: Football events with over/under markets (Total Goals Over/Under <figure afterward>, Over/Under First Half <figure afterward>, Over/Under Second Half <figure afterward>)
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Total Goals Over/Under x.x"
    PRECONDITIONS: *   PROD: name="Over/Under Total Goals x.x"
    """
    keep_browser_open = True

    def test_001_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        pass

    def test_002_go_to_overunder_total_goals_market_section(self):
        """
        DESCRIPTION: Go to 'Over/Under Total Goals' market section
        EXPECTED: *   Section is present on Event Details Page and titled ‘Over/Under Total Goals’
        EXPECTED: *   It is possible to collapse/expand section
        """
        pass

    def test_003_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If one of markets (Total Goals Over/Under <figure afterward>, Over/Under First Half <figure afterward>, Over/Under Second Half <figure afterward>) has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        pass

    def test_004_expand_overunder_total_goals_market_section(self):
        """
        DESCRIPTION: Expand 'Over/Under Total Goals' market section
        EXPECTED: Section consists of:
        EXPECTED: *   Three buttons: '90 mins' (selected by default), '1st Half', '2nd Half'
        EXPECTED: *   'Total Goals' column with market names
        EXPECTED: *   'Over' and 'Under' columns with price/odds buttons
        EXPECTED: *   First four markets shown by default
        EXPECTED: *   'Show All' button (if more than 4 markets are available)
        """
        pass

    def test_005_verify_overunder_markets_shown_for_90_mins(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '90 mins'
        EXPECTED: *  Only markets with attribute **name="Total Goals Over/Under <figure afterward>"** are present
        EXPECTED: *  Selection names and their Price/Odds values are correct
        """
        pass

    def test_006_verify_overunder_markets_shown_for_1st_half(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '1st Half'
        EXPECTED: *  Only markets with attribute **name="Over/Under First Half <figure afterward>"** are present
        EXPECTED: *  Selection names and their Price/Odds values are correct
        """
        pass

    def test_007_verify_overunder_markets_shown_for_2nd_half(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '2nd Half'
        EXPECTED: *  Only markets with attribute **name="Over/Under Second Half <figure afterward>"** are present
        EXPECTED: *  Selection names and their Price/Odds values are correct
        """
        pass
