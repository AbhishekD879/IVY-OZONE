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
class Test_C66114125_Verify_Denoting_Free_bet_journey_in_my_bets_by_placing_a_bet_with_free_bet(Common):
    """
    TR_ID: C66114125
    NAME: Verify Denoting Free bet journey in my bets by placing a bet with free bet
    DESCRIPTION: This test case is to verify Denoting Free bet journey in my bets by placing a bet with free bet
    PRECONDITIONS: 
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

    def test_002_navigate_to_any_sport_from_sports_ribbona_z_menu(self):
        """
        DESCRIPTION: Navigate to any sport from Sports ribbon/A-Z menu
        EXPECTED: Should be able to navigate to sports landing page
        """
        pass

    def test_003_place_a_single_bet_by_using_free_bet_without_entering_any_stake_amount_and_verify(self):
        """
        DESCRIPTION: place a single bet by using free bet without entering any stake amount and verify
        EXPECTED: should be able to place single bet successfully with free bet
        """
        pass

    def test_004_go_to_my_bets_and_verify(self):
        """
        DESCRIPTION: Go to my bets and verify
        EXPECTED: Recently placed bets should display under open and bets will be display in expanded state by default
        """
        pass

    def test_005_verify_free_bet_sign_posting_under_open(self):
        """
        DESCRIPTION: Verify free bet sign posting under open
        EXPECTED: Free bet signposting with text of its worth should be displayed beside stake
        EXPECTED: ![](index.php?/attachments/get/9be783a4-4187-4bc5-b46e-999ea82e2da8)
        """
        pass

    def test_006_collapse_the_bet_by_clicking_anywhere_on_the_bet_header_and_verify(self):
        """
        DESCRIPTION: collapse the bet by clicking anywhere on the bet header and verify
        EXPECTED: Should be able to collapse bets
        """
        pass

    def test_007_verify_free_bet_sign_posting_under_open_after_collapsing_bet(self):
        """
        DESCRIPTION: Verify free bet sign posting under open after collapsing bet
        EXPECTED: Free bet signposting with text of its worth should be displayed beside stake
        """
        pass

    def test_008_repeat_the_step_4_to_step_8_for_cashout_and_settled_tabs(self):
        """
        DESCRIPTION: Repeat the step 4 to step 8 for cashout and settled tabs
        EXPECTED: Result should be same as above
        """
        pass

    def test_009_repeat_the_step_3_to_step_9_by_placing_bets_in_lottos_and_pools_along_with_races(self):
        """
        DESCRIPTION: Repeat the step 3 to step 9 by placing bets in lottos and pools along with races
        EXPECTED: Result should be same as above
        """
        pass
