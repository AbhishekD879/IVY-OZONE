import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C852914_Verify_Hero_Header_displaying_on_Virtuals_page_for_Desktop(Common):
    """
    TR_ID: C852914
    NAME: Verify Hero Header displaying on Virtuals page for Desktop
    DESCRIPTION: This test case verifies Hero Header displaying on Virtuals page.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Virtuals page is opened
    PRECONDITIONS: 3. The first tab is opened by default
    """
    keep_browser_open = True

    def test_001_verify_hero_header_content_on_the_virtuals_page(self):
        """
        DESCRIPTION: Verify Hero Header content on the Virtuals page
        EXPECTED: Main View 1 and Main View 2 columns are merged and contain the following element:
        EXPECTED: * Virtuals header and 'Back' button
        EXPECTED: * Breadcrumbs trail
        """
        pass

    def test_002_verify_back_button(self):
        """
        DESCRIPTION: Verify 'Back' button
        EXPECTED: 'Back' button is displayed on the Virtuals header
        """
        pass

    def test_003_verify_breadcrumbs_trail_displaying(self):
        """
        DESCRIPTION: Verify Breadcrumbs trail displaying
        EXPECTED: * Breadcrumbs trail is displayed below Virtuals header
        EXPECTED: * Breadcrumbs trail is displayed in the next format: 'Home' > 'Virtuals'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass
