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
class Test_C62764781_Verify_Remove_surface_bet_with_Segmentwith_single_inclusion_and_verify_in_FE(Common):
    """
    TR_ID: C62764781
    NAME: Verify Remove surface bet with Segment(with single inclusion) and verify in FE
    DESCRIPTION: This test case verifies removal Segment(with single inclusion)
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> surface bet
    PRECONDITIONS: 2) Create a Segment(with single inclusion) surface bet
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_precondition(self):
        """
        DESCRIPTION: Navigate to module from precondition
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_surface_bet_link(self):
        """
        DESCRIPTION: Click on surface bet link.
        EXPECTED: User should be able to view existing surface bets should be displayed.
        """
        pass

    def test_004_click_on_existing_surface_bet_with_segmentwith_single_inclusion(self):
        """
        DESCRIPTION: Click on existing surface bet with Segment(with single inclusion)
        EXPECTED: surface bet detail page should be opened  with Universal (with single exclusion)
        """
        pass

    def test_005_click_on_remove_button(self):
        """
        DESCRIPTION: Click on Remove button
        EXPECTED: surface bet should be removed successfully
        """
        pass

    def test_006_load_oxygen_and_verify_surface_bet(self):
        """
        DESCRIPTION: Load oxygen and verify surface bet
        EXPECTED: Removed surface bet should not be shown in application, surface bet should be removed from specific segment
        """
        pass
