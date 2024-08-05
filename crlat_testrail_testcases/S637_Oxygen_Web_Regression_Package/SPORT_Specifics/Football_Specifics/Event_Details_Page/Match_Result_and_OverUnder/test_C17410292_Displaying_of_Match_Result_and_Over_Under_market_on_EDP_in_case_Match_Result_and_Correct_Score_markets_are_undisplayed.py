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
class Test_C17410292_Displaying_of_Match_Result_and_Over_Under_market_on_EDP_in_case_Match_Result_and_Correct_Score_markets_are_undisplayed(Common):
    """
    TR_ID: C17410292
    NAME: Displaying of 'Match Result and Over/Under' market on EDP  in case 'Match Result' and 'Correct Score' markets are undisplayed
    DESCRIPTION: This test case verifies displaying of 'Match Result and Over/Under' market on EDP  in case 'Match Result' and 'Correct Score' markets are undisplayed since 'Match Result and Over/Under' market takes names of teams from 'Match result' and 'Correct Score' markets.
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Event Details page
    PRECONDITIONS: 3. Make sure that 'Match Result', 'Correct Score' and 'Match Result and Over/Under' are created for a particular event. That event should NOT have other markets with dispSortName="MR"/"MH"/"CS"
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Note:
    PRECONDITIONS: Create a team with specials symbols in the team name to see if is shown correctly ex. M. B. Heid'enheim and long names such as Bayer Leverkusen, Borussia Dormund or Borussia Monchengladbach
    """
    keep_browser_open = True

    def test_001_verify_markets_displaying_on_edp(self):
        """
        DESCRIPTION: Verify markets displaying on EDP
        EXPECTED: The following markets are displayed on EDP:
        EXPECTED: - 'Match Result'
        EXPECTED: - 'Correct Score'
        EXPECTED: - 'Match Result and Over/Under'
        """
        pass

    def test_002_undisplay_the_match_result_market_using_ob_system(self):
        """
        DESCRIPTION: Undisplay the 'Match Result' market using OB system
        EXPECTED: The changes are saved successfully
        """
        pass

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: All available markets are loaded successfully on EDP
        """
        pass

    def test_004_verify_displaying_of_match_result_and_overunder_markets(self):
        """
        DESCRIPTION: Verify displaying of 'Match Result and Over/Under' markets
        EXPECTED: 'Match Result and Over/Under' markets are displayed on EDP
        """
        pass

    def test_005_undisplay_the_correct_score_market_using_ob_system(self):
        """
        DESCRIPTION: Undisplay the 'Correct Score' market using OB system
        EXPECTED: The changes are saved successfully
        """
        pass

    def test_006_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: All available markets are loaded successfully on EDP
        """
        pass

    def test_007_verify_displaying_of_match_result_and_overunder_markets(self):
        """
        DESCRIPTION: Verify displaying of 'Match Result and Over/Under' markets
        EXPECTED: 'Match Result and Over/Under' markets are displayed on EDP
        """
        pass

    def test_008_undisplay_the_following_markets_using_ob_system__match_result__correct_score(self):
        """
        DESCRIPTION: Undisplay the following markets using OB system:
        DESCRIPTION: - 'Match Result'
        DESCRIPTION: - 'Correct Score'
        EXPECTED: The changes are saved successfully
        """
        pass

    def test_009_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: All available markets are loaded successfully on EDP
        """
        pass

    def test_010_verify_displaying_of_match_result_and_overunder_markets(self):
        """
        DESCRIPTION: Verify displaying of 'Match Result and Over/Under' markets
        EXPECTED: 'Match Result and Over/Under' markets are NOT displayed on EDP
        """
        pass
