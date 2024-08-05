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
class Test_C57732045_TO_UPDATE_Verify_the_view_and_navigation_to_the_Quick_link_pages_when_the_content_is_incomplete(Common):
    """
    TR_ID: C57732045
    NAME: [TO UPDATE] Verify the view and navigation to the Quick link pages when the content is incomplete
    DESCRIPTION: This test case verifies the the view and navigation to the Quick link pages when the content is incomplete:
    DESCRIPTION: - The Header is populated, but the description is empty.
    DESCRIPTION: - the Header is empty, but the the description is populated.
    PRECONDITIONS: 1. The CMS User has successfully created a Quick link page with
    PRECONDITIONS: - Link 1 with Title "Prizes", URL "prizes" and empty description.
    PRECONDITIONS: - Link 2 with empty Title, empty URL and some description. - NOT VALID
    PRECONDITIONS: - Link 3 with empty Title, URL "terms" and empty description. - NOT VALID
    PRECONDITIONS: 2. The CMS User has successfully linked a previously created Quick link page to an active quiz.
    """
    keep_browser_open = True

    def test_001_open_httpsphoenix_invictuscoralcoukcorrect4splash(self):
        """
        DESCRIPTION: Open https://phoenix-invictus.coral.co.uk/correct4/splash
        EXPECTED: The Splash page is opened.
        EXPECTED: Only 'Prizes' Quick link is displayed.
        EXPECTED: ![](index.php?/attachments/get/59102)
        """
        pass

    def test_002_click_on_the_prizes_quick_link(self):
        """
        DESCRIPTION: Click on the 'Prizes' Quick link.
        EXPECTED: The error message with 'GO Back' button is displayed.
        EXPECTED: ![](index.php?/attachments/get/59103)
        """
        pass

    def test_003_click_on_the_go_back_button(self):
        """
        DESCRIPTION: Click on the 'GO Back' button.
        EXPECTED: The User is redirected to the Splash page.
        """
        pass

    def test_004_click_on_the_prizes_quick_link(self):
        """
        DESCRIPTION: Click on the 'Prizes' Quick link.
        EXPECTED: The error message with 'GO Back' button is displayed.
        EXPECTED: ![](index.php?/attachments/get/59103)
        """
        pass

    def test_005_click_on_the_back_arrow_icon(self):
        """
        DESCRIPTION: Click on the Back arrow icon.
        EXPECTED: The User is redirected to the Splash page.
        """
        pass
