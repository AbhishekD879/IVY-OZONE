import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66114120_Verify_whether_share_icon_displayed_under_my_bets_in_collapsed_state(Common):
    """
    TR_ID: C66114120
    NAME: Verify whether share icon displayed under my bets in collapsed state
    DESCRIPTION: This test case is to verify whether share icon displayed under my bets in collapsed state
    PRECONDITIONS: User should be logged in and Placed single and multiple bets data should be available.
    """
    keep_browser_open = True

    def test_000_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched without any issues
        """
        pass

    def test_001_go_to_my_bets_and_verify_recently_placed_bets_under_open(self):
        """
        DESCRIPTION: Go to my bets and verify recently placed bets under open
        EXPECTED: Should be match the bet details under open with recently placed single/multiple bets  Note: Bets will be in expanded state by default
        """
        pass

    def test_002_verify_share_icon_displaying_under_open(self):
        """
        DESCRIPTION: Verify share icon displaying under open
        EXPECTED: Share icon should be displayed in Open and to be in line with the Bet Details information  Note: Potential returns should be in the above line of share icon
        """
        pass

    def test_003_click_on_anywhere_on_bet_header_area_and_verify_collapsed_functionality(self):
        """
        DESCRIPTION: Click on anywhere on bet header area and verify collapsed functionality
        EXPECTED: Should be able to collapse bets in open
        """
        pass

    def test_004_verify_share_icon_after_collapsing_bets_under_open(self):
        """
        DESCRIPTION: verify share icon after collapsing bets under open
        EXPECTED: share icon should not display once bets are collapsed
        EXPECTED: ![](index.php?/attachments/get/75c756b9-80ec-44af-9183-c82c9cb7d24b)  ![](index.php?/attachments/get/a15138f5-9b0e-408e-8176-22c89bff7323)
        """
        pass

    def test_005_navigate_to_cashout_tab_and_perform_collapse_the_bets_then_verify_share_icon(self):
        """
        DESCRIPTION: Navigate to cashout tab and perform collapse the bets then verify share icon
        EXPECTED: share icon should not display once bets are collapsed
        """
        pass

    def test_006_navigate_to_settled_and_perform_collapse_the_bets_then_verify_share_icon(self):
        """
        DESCRIPTION: Navigate to settled and perform collapse the bets then verify share icon
        EXPECTED: share icon should not display once bets are collapsed
        """
        pass

    def test_007_repeat_the_step_2_to_step_7__by_placing_bets_for_lottos_and_pools_along_with_races(self):
        """
        DESCRIPTION: Repeat the step 2 to step 7  by placing bets for lottos and pools along with races
        EXPECTED: Result will be the same as above
        """
        pass
