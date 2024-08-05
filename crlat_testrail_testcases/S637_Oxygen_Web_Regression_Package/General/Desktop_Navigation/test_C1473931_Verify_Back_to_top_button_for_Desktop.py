import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C1473931_Verify_Back_to_top_button_for_Desktop(Common):
    """
    TR_ID: C1473931
    NAME: Verify 'Back to top' button for Desktop
    DESCRIPTION: This test case verifies 'Back to top' button for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Oxygen app is loaded
    """
    keep_browser_open = True

    def test_001_scroll_the_page_down(self):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: * 'Back to top' button appears when full Main Header is hidden
        EXPECTED: * 'Back to top' button is located in the bottom right corner of the page
        EXPECTED: * 'Back to top' button became sticky
        EXPECTED: * 'Up' arrow and 'Back to top' inscription are displayed at the button
        """
        pass

    def test_002_resize_the_page_to_more_than_1920px(self):
        """
        DESCRIPTION: Resize the page to more than 1920px
        EXPECTED: 'Back to top' button is located in the bottom right corner of the window
        """
        pass

    def test_003_resize_the_page_to_less_than_970px(self):
        """
        DESCRIPTION: Resize the page to less than 970px
        EXPECTED: 'Back to top' button is located in the bottom right corner of the window
        """
        pass

    def test_004_hover_the_mouse_over_the_back_to_top_button(self):
        """
        DESCRIPTION: Hover the mouse over the 'Back to top' button
        EXPECTED: * Hover state is activated
        EXPECTED: * Pointer changed the view from 'Normal select' to 'Link select' for realizing the possibility to click on the particular area
        """
        pass

    def test_005_click_on_the_back_to_top_button(self):
        """
        DESCRIPTION: Click on the 'Back to top' button
        EXPECTED: * User is redirected to the top of the page
        EXPECTED: * 'Back to top' button disappears
        """
        pass

    def test_006_navigate_to_different_pages_across_application_and_repeat_steps__1_5(self):
        """
        DESCRIPTION: Navigate to different pages across application and repeat steps  1-5
        EXPECTED: 
        """
        pass
