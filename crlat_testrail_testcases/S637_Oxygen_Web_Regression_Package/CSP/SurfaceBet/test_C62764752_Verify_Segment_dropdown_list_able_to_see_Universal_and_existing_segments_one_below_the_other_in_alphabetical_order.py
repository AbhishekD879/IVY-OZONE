import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C62764752_Verify_Segment_dropdown_list_able_to_see_Universal_and_existing_segments_one_below_the_other_in_alphabetical_order(Common):
    """
    TR_ID: C62764752
    NAME: Verify Segment dropdown list, able to see Universal and existing segments one below the other in alphabetical order.
    DESCRIPTION: This test case verifies order of in the segment dropdown list
    PRECONDITIONS: 1) "User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> surface bet
    PRECONDITIONS: 2) Should have some surface bet for Universal and segments
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_surface_bet_link(self):
        """
        DESCRIPTION: click on surface bet link.
        EXPECTED: User should be able to view existing surface bets should be displayed.
        """
        pass

    def test_004_click_on_segment_dropdown_and_verify_universal_segments_order(self):
        """
        DESCRIPTION: Click on segment dropdown and verify universal ,segments order
        EXPECTED: a) segment dropdown list should show Universal first and other segments should be in alphabetical order.
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: B) if user select any segment from drop down list the surface bets in that segment should display in alphabetical order.
        """
        pass

    def test_006_(self):
        """
        DESCRIPTION: 
        EXPECTED: C) If we remove all surface bets of any segment it should not display in drop down
        """
        pass
