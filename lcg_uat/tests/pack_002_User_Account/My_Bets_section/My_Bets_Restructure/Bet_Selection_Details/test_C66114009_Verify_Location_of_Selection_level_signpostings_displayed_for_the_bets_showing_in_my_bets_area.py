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
class Test_C66114009_Verify_Location_of_Selection_level_signpostings_displayed_for_the_bets_showing_in_my_bets_area(Common):
    """
    TR_ID: C66114009
    NAME: Verify Location of Selection level signpostings displayed for the bets showing in my bets area
    DESCRIPTION: This test case is to Verify Location of Selection level signpostings displayed for the bets showing in my bets area
    PRECONDITIONS: Placed single and multiple bets should be available under open/cashout/settled
    """
    keep_browser_open = True

    def test_000_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched successfully
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: user should be able to login succesfully
        """
        pass

    def test_002_go_to_my_bets_and_verify_bets_under_open(self):
        """
        DESCRIPTION: Go to my bets and verify bets under open
        EXPECTED: Recenlty placed bets should be display under open
        """
        pass

    def test_003_verify_the_sign_postings_for_single_and_multiple_bets_beside_selection(self):
        """
        DESCRIPTION: Verify the sign postings for single and multiple bets beside selection
        EXPECTED: Sign postings should be displayed next to the selection name and few signpostings should displayed with inlined to selection name
        """
        pass

    def test_004_verify_the_sign_postings_for_acca_bets(self):
        """
        DESCRIPTION: Verify the sign postings for ACCA bets
        EXPECTED: Sign postings should be displayed next to the selection name and few signpostings should displayed with inlined to selection name  (ex: Won tick mark, lost cross mark, Suspended, bet status icons-upward &amp; downward icons,
        """
        pass

    def test_005_repeat_step_4_and_5_under_cashout_tab(self):
        """
        DESCRIPTION: Repeat step 4 and 5 under cashout tab
        EXPECTED: Result should be same as above
        """
        pass

    def test_006_verify_the_icons_at_selection_level_under_setted_tab(self):
        """
        DESCRIPTION: Verify the icons at selection level under setted tab
        EXPECTED: Icons should be display properly next to the selection name for selection level icons
        """
        pass

    def test_007_repeat_step_3_to_step7_under_by_placing_bets_of_lottos_and_pools_and_verify(self):
        """
        DESCRIPTION: Repeat step 3 to step7 under by placing bets of lottos and pools and verify
        EXPECTED: Result should be same as above
        """
        pass
