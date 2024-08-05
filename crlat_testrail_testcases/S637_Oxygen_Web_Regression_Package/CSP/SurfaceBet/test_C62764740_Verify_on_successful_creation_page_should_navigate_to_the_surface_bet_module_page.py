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
class Test_C62764740_Verify_on_successful_creation_page_should_navigate_to_the_surface_bet_module_page(Common):
    """
    TR_ID: C62764740
    NAME: Verify on successful creation, page should navigate to the surface bet module page
    DESCRIPTION: This test case verifies page navigation after successful creation to the surface bet Module page
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> surface bet
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

    def test_003_click_on_surface_bet_link_and_configure_one_surface_bet(self):
        """
        DESCRIPTION: click on surface bet link and configure one surface bet.
        EXPECTED: On successful creation, page should navigate to the surface bet Module page.
        """
        pass
