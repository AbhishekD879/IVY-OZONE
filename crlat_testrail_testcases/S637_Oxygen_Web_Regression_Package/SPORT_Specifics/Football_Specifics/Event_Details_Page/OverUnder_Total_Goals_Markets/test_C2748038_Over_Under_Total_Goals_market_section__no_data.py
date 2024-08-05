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
class Test_C2748038_Over_Under_Total_Goals_market_section__no_data(Common):
    """
    TR_ID: C2748038
    NAME: Over/Under Total Goals market section - no data
    DESCRIPTION: This test case verifies 'Over/Under Total Goals' market section on Event Details Page in case there is not enough data
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
        """
        pass

    def test_003_verify_overunder_markets_shown_for_90_mins(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '90 mins'
        EXPECTED: If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        pass

    def test_004_verify_overunder_markets_shown_for_1st_half(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '1st Half'
        EXPECTED: If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        pass

    def test_005_verify_overunder_markets_shown_for_2nd_half(self):
        """
        DESCRIPTION: Verify Over/Under markets shown for '2nd Half'
        EXPECTED: If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        pass

    def test_006_verify_overunder_total_goals_section_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify 'Over/Under Total Goals' section in case of data absence
        EXPECTED: 'Over/Under Total Goals' section is not shown if:
        EXPECTED: all markets that section consists of are absent
        EXPECTED: all markets that section consists of do not have any outcomes
        """
        pass
