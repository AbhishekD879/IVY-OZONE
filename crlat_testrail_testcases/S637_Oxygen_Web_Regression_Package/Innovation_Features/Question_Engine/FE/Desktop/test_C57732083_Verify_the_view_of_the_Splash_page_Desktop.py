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
class Test_C57732083_Verify_the_view_of_the_Splash_page_Desktop(Common):
    """
    TR_ID: C57732083
    NAME: Verify the view of the Splash page [Desktop]
    DESCRIPTION: This test case verifies the view of the Splash page on the Desktop.
    PRECONDITIONS: 1. The game is configured in the CMS.
    PRECONDITIONS: 2. The User is logged in.
    PRECONDITIONS: 3. The User has not played the game yet.
    PRECONDITIONS: 4. Click on the 'Correct4' link.
    PRECONDITIONS: 5. Login with valid credentials.
    """
    keep_browser_open = True

    def test_001_click_on_the_correct4_link(self):
        """
        DESCRIPTION: Click on the 'Correct4' link.
        EXPECTED: 1. The Splash page is opened.
        EXPECTED: 2. The content is centered within the middle column.
        EXPECTED: 3. The Game Header is displayed as per design
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d888c43cae74a026e8eedd0
        EXPECTED: 4. The breadcrumbs in the sub-menu are not displayed.
        EXPECTED: 5. The 'X' icon is not displayed.
        """
        pass

    def test_002_click_on_the_back_arrow_icon(self):
        """
        DESCRIPTION: Click on the Back arrow icon.
        EXPECTED: 1. The User is redirected to the Home page.
        EXPECTED: 2. The Exit pop-up is not displayed.
        EXPECTED: 3. The sub-header with breadcrumbs is not displayed.
        """
        pass
