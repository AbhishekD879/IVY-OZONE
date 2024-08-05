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
class Test_C64881025_Verify_CMS_filter_by_category_or_show_all_in_surface_bets(Common):
    """
    TR_ID: C64881025
    NAME: Verify CMS filter by category or show all in surface bets
    DESCRIPTION: This test cases verifies filter by category or show all
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: 2)CMS configuration:
    PRECONDITIONS: CMS > Sports pages >home page>Surface bet
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        pass

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be able to see the surface bet module page with existing Universal Surfacebet records by selecting filter by category (default)
        """
        pass

    def test_003_verify_show_all_in_surface_bet_module_page(self):
        """
        DESCRIPTION: Verify show all in surface bet module page
        EXPECTED: All Surfacebet records shoud display without CSP implementaion
        """
        pass

    def test_004_(self):
        """
        DESCRIPTION: 
        EXPECTED: 1.There should not be drag and drop functionality
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: 2.Segment drop down should be disabled
        """
        pass
