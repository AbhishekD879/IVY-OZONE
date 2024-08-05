import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870412_Back_To_Top_arrow_functionality(Common):
    """
    TR_ID: C44870412
    NAME: Back To Top arrow functionality
    DESCRIPTION: When user start scrolling down the page and click on Back to Top arrow, is navigated to top of the page
    PRECONDITIONS: User loads the Ladbrokes desktop web page and log in
    """
    keep_browser_open = True

    def test_001_verify_that_back_to_top_arrow_is_available_in_all_the_pagesverify_that_when_user_start_scrolling_down_the_page_and_click_on_back_to_top_arrow_is_navigated_to_top_of_the_page(self):
        """
        DESCRIPTION: Verify that Back To Top arrow is available in all the pages
        DESCRIPTION: Verify that when user start scrolling down the page and click on Back to Top arrow, is navigated to top of the page
        EXPECTED: Back To Top arrow is available and functionality works fine
        """
        pass
