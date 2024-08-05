import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C2490706_Banach_Format_of_Correct_score_selection_on_dashboard(Common):
    """
    TR_ID: C2490706
    NAME: Banach. Format of Correct score selection on dashboard
    DESCRIPTION: Test case verifies Correct Score selections format in dashboard
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > markets-grouped request
    PRECONDITIONS: Response of selections for specific markets is to be taken from selections request when the market is expanded
    PRECONDITIONS: Correct Score market should be available
    PRECONDITIONS: BYB **Coral**/Bet Builder **Ladbrokes** tab is opened
    """
    keep_browser_open = True

    def test_001_make_the_following_selection_in_the_correct_score_market_accordion90_mins_home_team_1___away_team_3_and_tap_add_to_bet(self):
        """
        DESCRIPTION: Make the following selection in the Correct Score market accordion:
        DESCRIPTION: 90 mins HOME team 1 - AWAY team 3 and tap ADD TO BET
        EXPECTED: Selection has the following name format in dashboard:
        EXPECTED: Correct Score 90 mins [AWAY team] 3-1 - Coral
        EXPECTED: ![](index.php?/attachments/get/114303314)
        EXPECTED: (!) Team which has higher score is displayed in Dashboard.
        """
        pass

    def test_002_make_the_following_selection_in_the_correct_score_market_accordion90_mins_home_team_3___away_team_1_and_tap_add_to_bet(self):
        """
        DESCRIPTION: Make the following selection in the Correct Score market accordion:
        DESCRIPTION: 90 mins HOME team 3 - AWAY team 1 and tap ADD TO BET
        EXPECTED: Selection has the following name format in dashboard:
        EXPECTED: Correct Score 90 mins [Home team] 3-1 - Ladbrokes
        EXPECTED: ![](index.php?/attachments/get/114303315)
        EXPECTED: (!) Team which has higher score is displayed in Dashboard.
        """
        pass
