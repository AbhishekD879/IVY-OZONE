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
class Test_C62764599_Verify_the_CMS_navigation_and_default_view_of_Highlights_Carousel_module(Common):
    """
    TR_ID: C62764599
    NAME: Verify the CMS navigation and default view of Highlights Carousel module
    DESCRIPTION: This test case verifies CMS navigation and default view  of Highlights Carousel
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> Highlights Carousel
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
        EXPECTED: User should be able to see the Highlights Carousel module page and
        """
        pass

    def test_003_(self):
        """
        DESCRIPTION: 
        EXPECTED: with existing Universal Highlights Carousel records.
        """
        pass
