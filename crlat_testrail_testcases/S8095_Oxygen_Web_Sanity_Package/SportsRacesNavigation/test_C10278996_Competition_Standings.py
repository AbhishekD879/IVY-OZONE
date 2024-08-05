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
class Test_C10278996_Competition_Standings(Common):
    """
    TR_ID: C10278996
    NAME: Competition Standings
    DESCRIPTION: Test case verifies Standings tab on Competitions (which substituted 'Leagues' page in OX 98)
    PRECONDITIONS: **User is on Football > Competitions tab**
    PRECONDITIONS: Link to check league table results: http://www.espnfc.com/english-league-championship/24/table
    """
    keep_browser_open = True

    def test_001_select_competitionverify_standings_tab(self):
        """
        DESCRIPTION: Select competition
        DESCRIPTION: Verify Standings tab
        EXPECTED: Standings tab is present on Competition page if data is returned from 'resultstables' query
        """
        pass

    def test_002_verify_table(self):
        """
        DESCRIPTION: Verify Table
        EXPECTED: - League Table is given for the current season of selected Competition
        EXPECTED: - Table contains the following columns:
        EXPECTED: POS (position in table)
        EXPECTED: Team name (Text truncates for long names)
        EXPECTED: P (stands for 'Plays/Matches total')
        EXPECTED: W (stands for 'Won total')
        EXPECTED: D (stands for 'Draw total')
        EXPECTED: L (stands for 'Lost total')
        EXPECTED: GD (stands for 'Goal Difference total')
        EXPECTED: PTS (stands for 'Points total')
        """
        pass

    def test_003_verify_user_can_navigate_between_available_seasons(self):
        """
        DESCRIPTION: Verify user can navigate between available seasons
        EXPECTED: User can navigate using arrow in the Table header
        EXPECTED: for ex. from UEFA Champions League 18/19 to UEFA Champions League 17/18 and back
        """
        pass
