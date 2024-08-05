import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C1501895_Verify_navigation_arrows_for_Sport_Tabs_within_In_Play_and_Live_Stream_section_on_Home_page_for_Desktop(Common):
    """
    TR_ID: C1501895
    NAME: Verify navigation arrows for Sport Tabs within 'In-Play and Live Stream' section on Home page for Desktop
    DESCRIPTION: This test case verifies navigation arrows for Sport Tabs within 'In-Play and Live Stream' section on Home page for Desktop in case not all tabs fit in Sport Menu Ribbon
    PRECONDITIONS: * More than 6 different Sport Tabs should be present in Sport Menu Ribbon within 'In-Play and Live Stream' section on Home page for Desktop
    PRECONDITIONS: * To get Sport Tabs appear in Sport Menu Ribbon, at least one class for the corresponding category should have the following attributes:
    PRECONDITIONS: - Class's attribute 'siteChannels' contains 'M'
    PRECONDITIONS: - Class's attribute hasLiveNowEvent="true"
    PRECONDITIONS: - At least one event in the class has attribute 'siteChannels' that contains 'M'
    PRECONDITIONS: - At least one event in the class contains attribute drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS: - At least one event in the class contains attribute isLiveNowEvent="true"
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen app on Desktop
        EXPECTED: Home page is opened
        """
        pass

    def test_002_scroll_the_page_down_to_view_in_play_and_live_stream_section(self):
        """
        DESCRIPTION: Scroll the page down to view 'In-play and Live Stream' section
        EXPECTED: 'In-play and Live Stream' section is displayed below 'Enhances Multiples' carousel
        """
        pass

    def test_003_resize_screen_so_that_not_all_sport_tabs_fit_in_ribbon_and_hover_mouse_over(self):
        """
        DESCRIPTION: Resize screen so that NOT all Sport Tabs fit in ribbon and hover mouse over
        EXPECTED: Right arrow appears on the right side of Sport Menu Ribbon
        """
        pass

    def test_004_click_on_the_right_arrow(self):
        """
        DESCRIPTION: Click on the right arrow
        EXPECTED: Content (sport tabs) scrolls right
        """
        pass

    def test_005_hover_over_sport_menu_ribbon_again(self):
        """
        DESCRIPTION: Hover over Sport Menu Ribbon again
        EXPECTED: Right and left arrows appear on the sides of ribbon
        """
        pass

    def test_006_click_on_the_left_arrow(self):
        """
        DESCRIPTION: Click on the left arrow
        EXPECTED: Content (sport tabs) scrolls left
        """
        pass

    def test_007_click_on_right_arrow_till_the_end_of_ribbon(self):
        """
        DESCRIPTION: Click on right arrow till the end of ribbon
        EXPECTED: * Right arrow is not displayed at the end of ribbon
        EXPECTED: * Left arrow is displayed
        """
        pass

    def test_008_resize_screen_so_that_all_sport_tabs_fit_in_ribbon_and_hover_mouse_over(self):
        """
        DESCRIPTION: Resize screen so that ALL Sport Tabs fit in ribbon and hover mouse over
        EXPECTED: No arrows are shown
        """
        pass
