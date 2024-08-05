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
class Test_C66137594_Verify_Whether_Cash_Out_TCs_and_Edit_My_Acca_TCs_quick_links_displayed_under_open(Common):
    """
    TR_ID: C66137594
    NAME: Verify Whether Cash Out T&Cs and Edit My Acca T&Cs quick links displayed under open
    DESCRIPTION: This test case is to Verify Whether Cash Out T&Cs and Edit My Acca T&Cs quick links displayed under open
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
        EXPECTED: Should be able to see recently placed bets under open  Note: Open bets willl be selected by default
        """
        pass

    def test_000_verify_the__cash_out_tampcs_and_edit_my_acca_tampcs_quick_links_by_scrolling_down_under_open(self):
        """
        DESCRIPTION: Verify the  Cash Out T&amp;Cs and Edit My Acca T&amp;Cs quick links by scrolling down under open
        EXPECTED: Should be able to see Quick links of Cash Out T&amp;Cs and Edit My Acca T&amp;Cs under under open
        EXPECTED: Note: Open bets will be selected by default
        """
        pass

    def test_000_verify_the_location_of__cash_out_tampcs_and_edit_my_acca_tampcs(self):
        """
        DESCRIPTION: Verify the location of  Cash Out T&amp;Cs and Edit My Acca T&amp;Cs
        EXPECTED: Quick links of Cash Out T&amp;Cs and Edit My Acca T&amp;Cs should be displayed utmost bottom to the bets and These both quick links should be displayed side be side
        EXPECTED: Note: Cash Out T&amp;Cs quick link should be left side to the Edit My Acca T&amp;Cs quick link
        EXPECTED: ![](index.php?/attachments/get/45122721-ceae-44e7-a131-ecb3ab14b79d)
        """
        pass

    def test_000_repeat_steps_3rd_to_step_6_for_raceslottospools_and_verify(self):
        """
        DESCRIPTION: Repeat steps 3rd to step 6 for races/lottos/pools and verify
        EXPECTED: Result should be sameas above for all sport/lotto/pools
        """
        pass
