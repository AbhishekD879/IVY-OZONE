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
class Test_C62764603_Verify_Highlights_Carousel_module_ordering_among_other_modules(Common):
    """
    TR_ID: C62764603
    NAME: Verify Highlights Carousel module ordering among other modules
    DESCRIPTION: Test case verifies possibility to order Highlights Carousel module among other modules
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> Highlights Carousel
    PRECONDITIONS: 2) There is at least one Highlights Carousel added to the SLP/Homepage in CMS.
    PRECONDITIONS: 3)There are other modules active and configured in CMS for this homepage/SLP
    PRECONDITIONS: 4)Open this SLP/Homepage in Oxygen application.
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
        EXPECTED: User should be navigated successfully
        """
        pass

    def test_003_verify_the_order_of_the_highlights_carousel_module_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the Highlights Carousel module is as per order in the CMS.
        EXPECTED: The order is as defined in CMS.
        """
        pass

    def test_004_change_the_order_in_the_cms_in_the_application_refresh_the_page_and_verify_the_order_is_updated(self):
        """
        DESCRIPTION: Change the order in the CMS. In the application refresh the page and verify the order is updated.
        EXPECTED: The order is updated and is as defined in the CMS
        """
        pass
