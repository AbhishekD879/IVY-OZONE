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
class Test_C57732044_Verify_the_view_and_navigation_to_the_Quick_link_pages(Common):
    """
    TR_ID: C57732044
    NAME: Verify the view and navigation to the Quick link pages
    DESCRIPTION: This test case verifies the view and navigation to the Quick link pages:
    DESCRIPTION: - 'Prizes'
    DESCRIPTION: - 'Frequently Asked Questions'
    DESCRIPTION: - 'Terms & Conditions'
    PRECONDITIONS: 1. The Quick link pages are successfully created and linked to the Splash page in the CMS.
    """
    keep_browser_open = True

    def test_001_tap_on_the_prizes_quick_link_in_the_footer(self):
        """
        DESCRIPTION: Tap on the 'Prizes' quick link in the footer.
        EXPECTED: The User is navigated to the 'Prizes' content page.
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a6765b59ba27451b0
        """
        pass

    def test_002_tap_on_the_back_arrow_icon(self):
        """
        DESCRIPTION: Tap on the 'Back' arrow icon.
        EXPECTED: The User is returned to the previous page.
        """
        pass

    def test_003_tap_on_the_frequently_asked_questions_quick_link_in_the_footer(self):
        """
        DESCRIPTION: Tap on the 'Frequently Asked Questions' quick link in the footer.
        EXPECTED: The User is navigated to the 'Frequently Asked Questions' content page.
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a96fd105217526bf6
        """
        pass

    def test_004_tap_on_the_back_arrow_icon(self):
        """
        DESCRIPTION: Tap on the 'Back' arrow icon.
        EXPECTED: The User is returned to the previous page.
        """
        pass

    def test_005_tap_on_the_terms__conditions_quick_link_in_the_footer(self):
        """
        DESCRIPTION: Tap on the 'Terms & Conditions' quick link in the footer.
        EXPECTED: The User is navigated to the 'Terms & Conditions' content page.
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a96fd105217526bf6
        """
        pass

    def test_006_tap_on_the_back_arrow_icon(self):
        """
        DESCRIPTION: Tap on the 'Back' arrow icon.
        EXPECTED: The User is returned to the previous page.
        """
        pass
