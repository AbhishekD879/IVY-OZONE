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
class Test_C661121_Verify_Horizontal_slider_for_Desktop(Common):
    """
    TR_ID: C661121
    NAME: Verify Horizontal slider for Desktop
    DESCRIPTION: This test case verifies Horizontal slider.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Oxygen app is loaded
    """
    keep_browser_open = True

    def test_001_verify_if_horizontal_slider_is_not_displayed_in_desktop_body_view_for_screen_width_more_than_970px_or_equal_to_970px(self):
        """
        DESCRIPTION: Verify if Horizontal slider is NOT displayed in Desktop Body View for screen width more than 970px or equal to 970px
        EXPECTED: * Desktop View is displayed with Left navigation menu and 2 columns
        EXPECTED: * Horizontal slider is NOT displayed at the bottom of page
        """
        pass

    def test_002_verify_if_horizontal_slider_is_displayed_in_desktop_body_view_for_screen_width_less_than_970px_when_actual_size_of_page_is_970px(self):
        """
        DESCRIPTION: Verify if Horizontal slider is displayed in Desktop Body View for screen width less than 970px when actual size of page is 970px
        EXPECTED: * Desktop View is displayed with Left navigation menu and 2 columns
        EXPECTED: * Horizontal slider is displayed at the bottom of page
        """
        pass

    def test_003_verify_if_possible_to_scroll_page_using_horizontal_slider(self):
        """
        DESCRIPTION: Verify if possible to scroll page using Horizontal slider
        EXPECTED: The page is scrolling to right/left side
        """
        pass

    def test_004_verify_if_possible_to_see_the_whole_page_content_using_horizontal_slider(self):
        """
        DESCRIPTION: Verify if possible to see the whole page content using Horizontal slider
        EXPECTED: Possible to see whole content of the page when scrolling Horizontal slider to left/right
        """
        pass

    def test_005_navigate_to_different_pages_across_the_application_and_repeat_steps_1_4(self):
        """
        DESCRIPTION: Navigate to different pages across the application and repeat steps 1-4
        EXPECTED: 
        """
        pass
