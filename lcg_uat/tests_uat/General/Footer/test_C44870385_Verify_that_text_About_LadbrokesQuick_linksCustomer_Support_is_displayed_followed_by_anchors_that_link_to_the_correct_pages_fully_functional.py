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
class Test_C44870385_Verify_that_text_About_LadbrokesQuick_linksCustomer_Support_is_displayed_followed_by_anchors_that_link_to_the_correct_pages_fully_functional_and_aligned_as_follows(Common):
    """
    TR_ID: C44870385
    NAME: Verify that text About Ladbrokes,Quick links,Customer Support. is displayed followed by anchors that link to the correct pages, fully functional and aligned as follows:
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_open_application(self):
        """
        DESCRIPTION: Open application
        EXPECTED: Application is opened.
        """
        pass

    def test_002_navigate_to_footerverify_that_text_about_ladbrokesquick_linkscustomer_support_is_displayed_followed_by_anchors_that_link_to_the_correct_pages_fully_functional_and_aligned_as_follows(self):
        """
        DESCRIPTION: Navigate to footer
        DESCRIPTION: Verify that text About Ladbrokes,Quick links,Customer Support. is displayed followed by anchors that link to the correct pages, fully functional and aligned as follows:
        EXPECTED: When clicked on
        EXPECTED: Visit Our Help Centre or Tweet Us@LadbrokesCare
        EXPECTED: User is navigated to appropriate pages.
        """
        pass
