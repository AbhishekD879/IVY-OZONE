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
class Test_C66111710_Verify_the_chevron_displayed_at_the_right_of_each_selection_for_the_bets_displayed_in_My_Bets_area(Common):
    """
    TR_ID: C66111710
    NAME: Verify the chevron displayed at the right of each selection for the bets displayed in My Bets area
    DESCRIPTION: This testcase verifies the chevron displayed at the right of each selection for the bets displayed in My Bets area
    PRECONDITIONS: Sports,Lottos,Pools bets should be available in Open ,cash out settled tab
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_verify_the_chevron_displayed_at_the_right_of_each_selection_for_the_bets_displayed_in_open_tab(self):
        """
        DESCRIPTION: Verify the chevron displayed at the right of each selection for the bets displayed in open tab
        EXPECTED: Chevron should no longer appears to the right of each selection
        EXPECTED: ![](index.php?/attachments/get/2a3bc65a-93c5-4668-b963-5ac705a78258)
        """
        pass

    def test_004_repeat_step_4_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat step 4 in cash out tab
        EXPECTED: Chevron should no longer appears to the right of each selection
        """
        pass

    def test_005_repeat_step_4_in_settled_tab(self):
        """
        DESCRIPTION: Repeat step 4 in Settled tab
        EXPECTED: Chevron should no longer appears to the right of each selection
        """
        pass
