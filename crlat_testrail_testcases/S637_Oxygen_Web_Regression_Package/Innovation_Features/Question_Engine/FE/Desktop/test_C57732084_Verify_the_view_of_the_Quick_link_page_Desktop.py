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
class Test_C57732084_Verify_the_view_of_the_Quick_link_page_Desktop(Common):
    """
    TR_ID: C57732084
    NAME: Verify the view of the Quick link page [Desktop]
    DESCRIPTION: This test case verifies the view of the Quick link page on the Desktop.
    PRECONDITIONS: 1. The game is configured in the CMS.
    PRECONDITIONS: 2. The User is logged in.
    PRECONDITIONS: 3. The User has not played the game yet.
    PRECONDITIONS: 4. Click on the 'Correct4' link.
    PRECONDITIONS: 5. Login with valid credentials.
    """
    keep_browser_open = True

    def test_001_click_on_any_quick_link(self):
        """
        DESCRIPTION: Click on any Quick link.
        EXPECTED: The Quick links content page is displayed with the CMS content.
        EXPECTED: The Back arrow navigation is displayed in the top left corner.
        EXPECTED: The Page header is displayed underneath the back arrow (as on Mobile).
        EXPECTED: The sub-header with breadcrumbs is not displayed.
        """
        pass

    def test_002_click_on_the_back_arrow_icon(self):
        """
        DESCRIPTION: Click on the Back arrow icon.
        EXPECTED: The Splash page is opened.
        EXPECTED: The sub-header with breadcrumbs is not displayed.
        """
        pass
