import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870397_Verify_the_Bet_placement_Settlement_for_available_selections_in_the_markets_Markets_type_Yourcall_Yourcall_Home_team_Yourcall_Both_team_(Common):
    """
    TR_ID: C44870397
    NAME: """Verify the Bet placement & Settlement  for available selections in the markets ( Markets type #Yourcall) #Yourcall Home team , #Yourcall Both team "
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_open_httpsmsportsladbrokescom(self):
        """
        DESCRIPTION: Open https://msports.ladbrokes.com
        EXPECTED: Ladbrokes application launched
        """
        pass

    def test_002_navigate_to_football_lp(self):
        """
        DESCRIPTION: Navigate to Football LP
        EXPECTED: Football LP displayed
        """
        pass

    def test_003_find_football_event_with__markets_type_yourcall_yourcall_home_team__yourcall_both_team_etc(self):
        """
        DESCRIPTION: Find football event with ( Markets type #Yourcall) #Yourcall Home team , #Yourcall Both team etc"
        EXPECTED: ( Markets type #Yourcall) #Yourcall Home team , #Yourcall Both team etc displayed
        """
        pass

    def test_004_place_bets_on_these_selections(self):
        """
        DESCRIPTION: Place bets on these selections
        EXPECTED: Bets placed successfully
        """
        pass

    def test_005_verify_correct_settlement_of_these_markets(self):
        """
        DESCRIPTION: Verify correct settlement of these markets
        EXPECTED: Selections settled successfully
        """
        pass
