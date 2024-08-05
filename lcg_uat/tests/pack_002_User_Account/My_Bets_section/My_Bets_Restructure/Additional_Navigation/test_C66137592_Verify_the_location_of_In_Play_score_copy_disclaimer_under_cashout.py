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
class Test_C66137592_Verify_the_location_of_In_Play_score_copy_disclaimer_under_cashout(Common):
    """
    TR_ID: C66137592
    NAME: Verify the location of In-Play score copy disclaimer under cashout
    DESCRIPTION: This test case is to Verify the location of In-Play score copy disclaimer under cashout
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

    def test_000_verify_in_play_score_copy_disclaimer_under_cashout_by_scrolling_the_bets_after_navigating_to_cashout_from_open(self):
        """
        DESCRIPTION: Verify In-Play score copy disclaimer under cashout by scrolling the bets after navigating to cashout from open
        EXPECTED: In-Play score copy disclaimer should be displayed at the bottom of cashout bets page
        """
        pass

    def test_000_verify_the_location_of__in_play_score_copy_disclaimer_under_cashout(self):
        """
        DESCRIPTION: verify the location of  In-Play score copy disclaimer under cashout
        EXPECTED: Location of  In-Play score copy disclaimer should be left justified below the Cash Out T&amp;Cs and Edit My Acca T&amp;Cs quick links
        EXPECTED: ![](index.php?/attachments/get/a11aa9f6-9d15-40db-99aa-45d0066b4146)
        """
        pass

    def test_000_repeat_step_3_to_step_5_for_all_lottos_pools_under_open_along_with_sportsraces(self):
        """
        DESCRIPTION: Repeat step 3 to step 5 for all lottos, pools under open along with sports/races
        EXPECTED: Result should be same as above
        """
        pass
