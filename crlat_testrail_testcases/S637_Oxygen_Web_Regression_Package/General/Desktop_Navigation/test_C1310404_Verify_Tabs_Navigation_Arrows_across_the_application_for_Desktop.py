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
class Test_C1310404_Verify_Tabs_Navigation_Arrows_across_the_application_for_Desktop(Common):
    """
    TR_ID: C1310404
    NAME: Verify Tabs Navigation Arrows across the application for Desktop
    DESCRIPTION: This test case verifies Tabs Navigation Arrows across the application for Desktop.
    DESCRIPTION: Need to check on Windows ( IE, Edge, Chrome, FireFox ) and Mac OS (Safari).
    PRECONDITIONS: Oxygen app is loaded
    """
    keep_browser_open = True

    def test_001_navigate_to_any_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to any Sports Landing page
        EXPECTED: * Sports Landing page is loaded successfully
        EXPECTED: * Sports Sub Tabs are displayed below banner area (or Enhanced multiples carousel if it's available)
        """
        pass

    def test_002_hover_the_mouse_over_the_tabs(self):
        """
        DESCRIPTION: Hover the mouse over the tabs
        EXPECTED: No arrows appear on both sides of tabs row
        """
        pass

    def test_003_minimize_the_page_to_smaller_size_and_make_sure_that_tabs_are_not_visible_fully(self):
        """
        DESCRIPTION: Minimize the page to smaller size and make sure that tabs are not visible fully
        EXPECTED: Some tabs are not fully visible
        """
        pass

    def test_004_hover_the_mouse_over_the_tabs(self):
        """
        DESCRIPTION: Hover the mouse over the tabs
        EXPECTED: Right navigation arrow appears on the tabs row
        """
        pass

    def test_005_click_on_the_right_navigation_arrow(self):
        """
        DESCRIPTION: Click on the right navigation arrow
        EXPECTED: * Content scrolls horizontally in the left direction
        EXPECTED: * The next tab becomes visible in the tabs row
        """
        pass

    def test_006_hover_the_mouse_over_the_tabs_again(self):
        """
        DESCRIPTION: Hover the mouse over the tabs again
        EXPECTED: Right and left navigation arrows appear on both sides of tabs row respectively
        """
        pass

    def test_007_click_on_the_left_navigation_arrow(self):
        """
        DESCRIPTION: Click on the left navigation arrow
        EXPECTED: * Content scrolls horizontally in the right direction
        EXPECTED: * The previous tab becomes visible in the tabs row
        """
        pass

    def test_008_click_on_the_right_navigation_arrow_to_rich_the_end_of_tabs_row_to_the_last_tab(self):
        """
        DESCRIPTION: Click on the right navigation arrow to rich the end of tabs row (to the last tab)
        EXPECTED: *  Content scrolls horizontally in the left direction and the last tab becomes visible in the tabs row
        EXPECTED: * It's not a loop, user is able to get to the last tab in the tabs row
        EXPECTED: * Right navigation arrow is not displayed at the end of the tabs row
        """
        pass

    def test_009_hover_the_mouse_over_the_tabs_again(self):
        """
        DESCRIPTION: Hover the mouse over the tabs again
        EXPECTED: Left navigation arrow appears on the tabs row
        """
        pass

    def test_010_click_on_the_left_navigation_arrow_to_rich_the_beginning_of_tabs_row_to_the_first_tab(self):
        """
        DESCRIPTION: Click on the left navigation arrow to rich the beginning of tabs row (to the first tab)
        EXPECTED: *  Content scrolls horizontally in the right direction and the first tab becomes visible in the tabs row
        EXPECTED: * It's not a loop, user is able to get to the first tab in the tabs row
        EXPECTED: * Left navigation arrow is not displayed at the beginning of the tabs row
        """
        pass

    def test_011_navigate_to_betslip_widget_and_repeat_steps_2_10(self):
        """
        DESCRIPTION: Navigate to 'Betslip' widget and repeat steps 2-10
        EXPECTED: 
        """
        pass

    def test_012_navigate_to_sports_event_details_page_and_repeat_steps_2_10(self):
        """
        DESCRIPTION: Navigate to Sports Event Details page and repeat steps 2-10
        EXPECTED: 
        """
        pass

    def test_013_navigate_to_virtuals_all_tabs_except_tournaments_and_repeat_steps_2_10(self):
        """
        DESCRIPTION: Navigate to Virtuals (All tabs except Tournaments) and repeat steps 2-10
        EXPECTED: 
        """
        pass

    def test_014_navigate_to_races_landing_page_and_repeat_steps_2_10(self):
        """
        DESCRIPTION: Navigate to Races Landing page and repeat steps 2-10
        EXPECTED: 
        """
        pass

    def test_015_navigate_to_races_details_page_and_repeat_steps_2_10(self):
        """
        DESCRIPTION: Navigate to Races Details page and repeat steps 2-10
        EXPECTED: 
        """
        pass

    def test_016_navigate_to_inplay__live_stream_section_and_repeat_steps_2_10(self):
        """
        DESCRIPTION: Navigate to 'InPlay & Live Stream' section and repeat steps 2-10
        EXPECTED: 
        """
        pass

    def test_017_navigate_to_inplay_page_and_repeat_steps_2_10(self):
        """
        DESCRIPTION: Navigate to 'InPlay' page and repeat steps 2-10
        EXPECTED: 
        """
        pass
