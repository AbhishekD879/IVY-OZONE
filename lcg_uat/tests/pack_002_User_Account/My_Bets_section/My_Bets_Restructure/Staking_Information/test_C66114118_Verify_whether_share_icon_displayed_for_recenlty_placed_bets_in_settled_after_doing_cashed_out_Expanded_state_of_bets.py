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
class Test_C66114118_Verify_whether_share_icon_displayed_for_recenlty_placed_bets_in_settled_after_doing_cashed_out_Expanded_state_of_bets(Common):
    """
    TR_ID: C66114118
    NAME: Verify whether share icon displayed for recenlty placed bets in settled after doing cashed out- Expanded state of bets
    DESCRIPTION: This test case is to verify whether share icon displayed after placing bet in settled after doing cashed out
    PRECONDITIONS: cashout available events data should be available
    """
    keep_browser_open = True

    def test_000_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched without any issues
        """
        pass

    def test_001_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User should be able to login without any issues
        """
        pass

    def test_002_navigate_to_any_sport_landing_page_from_sports_ribbon_a_z_menu(self):
        """
        DESCRIPTION: Navigate to any sport landing page from sports ribbon /A-Z menu
        EXPECTED: User should be able to navigate to SLP
        """
        pass

    def test_003_place_single_and_mutiple_bets_from_different_events_which_events_have_cashout_availability(self):
        """
        DESCRIPTION: Place single and mutiple bets from different events which events have cashout availability
        EXPECTED: Single and multiple bets should be placed successfully
        """
        pass

    def test_004_go_to_my_bets_and_verify_recently_placed_bets_under_open(self):
        """
        DESCRIPTION: Go to my bets and verify recently placed bets under open
        EXPECTED: Should be match the bet details under open with recently placed single/multiple bets Note: Bets will be in expanded state by default
        """
        pass

    def test_005_navigate_to_cashout_tab_and_verify_recently_placed_bets(self):
        """
        DESCRIPTION: Navigate to cashout tab and verify recently placed bets
        EXPECTED: Recently placed bets which have cashout under open should be display under cashout
        """
        pass

    def test_006_perform_cashout_for_single__multiple_bets__under_cashout_tab_and_verify(self):
        """
        DESCRIPTION: Perform cashout for single / Multiple bets  under cashout tab and verify
        EXPECTED: User should be able to do cashout successfully
        """
        pass

    def test_007_navigate_to_settled_and_verify_share_icon_displaying_under_settled_for_recently_cashed_out_bets(self):
        """
        DESCRIPTION: Navigate to settled and verify share icon displaying under settled for recently cashed out bets
        EXPECTED: Share icon should be displayed in settled and to be in line with the Bet Details information  Note: Potential returns should be in the above line of share icon
        EXPECTED: ![](index.php?/attachments/get/f29836d1-03b8-4238-ab64-1f3358a819af)
        """
        pass

    def test_008_repeat_the_step_7_and_8_from_open_bet_and_verify(self):
        """
        DESCRIPTION: Repeat the step 7 and 8 from open bet and verify
        EXPECTED: Result will be the same as above
        """
        pass

    def test_009_repeat_the_step_3_to_step_9__by_placing_bets_for_lottos_and_pools_along_with_races(self):
        """
        DESCRIPTION: Repeat the step 3 to step 9  by placing bets for lottos and pools along with races
        EXPECTED: Result will be the same as above
        """
        pass
