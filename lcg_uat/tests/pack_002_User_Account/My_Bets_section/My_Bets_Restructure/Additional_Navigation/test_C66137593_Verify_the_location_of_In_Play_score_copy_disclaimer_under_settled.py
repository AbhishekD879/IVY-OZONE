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
class Test_C66137593_Verify_the_location_of_In_Play_score_copy_disclaimer_under_settled(Common):
    """
    TR_ID: C66137593
    NAME: Verify the location of In-Play score copy disclaimer under settled
    DESCRIPTION: This test case is to Verify the location of In-Play score copy disclaimer under settled
    PRECONDITIONS: User should have bets for sports/races/lottos/pools under all tabs (open/cashout/settled)
    """
    keep_browser_open = True

    def test_000_launch_application(self):
        """
        DESCRIPTION: Launch Application
        EXPECTED: Application shold be launched succesfully
        """
        pass

    def test_000_login_to_applicaiton_with_valid_credentials(self):
        """
        DESCRIPTION: Login to applicaiton with valid credentials
        EXPECTED: User should be able to login without any issues
        """
        pass

    def test_000_navigate_to_mybets(self):
        """
        DESCRIPTION: Navigate to Mybets
        EXPECTED: Should be able to see recently placed bets under open
        EXPECTED: Note: Open bets willl be selected by default
        """
        pass

    def test_000_verify_in_play_score_copy_disclaimer_under_cashout_by_scrolling_the_bets_after_navigating_to_settled_from_open(self):
        """
        DESCRIPTION: Verify In-Play score copy disclaimer under cashout by scrolling the bets after navigating to settled from open
        EXPECTED: In-Play score copy disclaimer should be displayed at the bottom of settled bets page
        """
        pass

    def test_000_verify_the_location_of__in_play_score_copy_disclaimer_under_settled(self):
        """
        DESCRIPTION: verify the location of  In-Play score copy disclaimer under settled
        EXPECTED: Location of  In-Play score copy disclaimer should be left justified below the Cash Out T&amp;Cs and Edit My Acca T&amp;Cs quick links
        EXPECTED: ![](index.php?/attachments/get/f27fa1e9-fe15-4e94-a3c1-5bc452453dbf)
        """
        pass

    def test_000_repeat_step_3_to_step_6_for_all_lottos_pools_under_settled_along_with_sportsraces(self):
        """
        DESCRIPTION: Repeat step 3 to step 6 for all lottos, pools under settled along with sports/races
        EXPECTED: Result should be same as above
        """
        pass
