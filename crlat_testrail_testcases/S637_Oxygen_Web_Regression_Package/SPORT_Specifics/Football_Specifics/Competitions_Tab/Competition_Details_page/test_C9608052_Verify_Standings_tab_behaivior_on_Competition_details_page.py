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
class Test_C9608052_Verify_Standings_tab_behaivior_on_Competition_details_page(Common):
    """
    TR_ID: C9608052
    NAME: Verify 'Standings' tab behaivior on Competition details page
    DESCRIPTION: This test case verifies 'Standings' tab displayed on Football competition details page depends on league table availability
    PRECONDITIONS: 1. Navigate to Football landing page > Competitions tab
    PRECONDITIONS: 2. Expand any class accordion and click on any type (e.g. Premier League)
    PRECONDITIONS: NOTE:
    PRECONDITIONS: 'Standings' tab is displayed if a league table is available for that league on the competition page(received from Bet Radar)
    PRECONDITIONS: **Requests:**
    PRECONDITIONS: Request to get Spark id for competition user is viewing (see value in “competitionId”):
    PRECONDITIONS: **/brcompetitionseason/XX/YY/ZZZ,**
    PRECONDITIONS: where
    PRECONDITIONS: * XX - OB category id (e.g. Football - id=16)
    PRECONDITIONS: * YY - OB class id (e.g. Football England - id=97)
    PRECONDITIONS: * ZZZ - OB type id (e.g. Premier League - id=442)
    PRECONDITIONS: Request to get league table for competition user is viewing (see value in “competitionId”):
    PRECONDITIONS: **/resultstables/X/YY/HH/ZZZZ,**
    PRECONDITIONS: where
    PRECONDITIONS: * X - OB area Id (e.g England id=1)
    PRECONDITIONS: * YY - OB competition Id (e.g Premier League id=1)
    PRECONDITIONS: * HH - OB sport Id (e.g Soccer id=1)
    PRECONDITIONS: * ZZZZ - OB season Id(e.g. id = 38738)
    """
    keep_browser_open = True

    def test_001_tap_standings_tab(self):
        """
        DESCRIPTION: Tap 'Standings' tab
        EXPECTED: * User navigates to the appropriate competition page (e.g. Premier League)
        EXPECTED: * The league table for that competition for current season is displayed
        """
        pass

    def test_002_navigate_to_previous_league_tableif_one_is_available(self):
        """
        DESCRIPTION: Navigate to previous League Table(if one is available)
        EXPECTED: User is navigated to page with the previous league table for that competition when multiple league tables are received
        """
        pass

    def test_003_navigate_to_current_league_table_if_viewing_a_previous_one(self):
        """
        DESCRIPTION: Navigate to current League Table (if viewing a previous one)
        EXPECTED: User is navigated to the current League Table
        """
        pass
