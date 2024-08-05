import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C1049075_Carousel_functionality_on_In_play_widget_for_Desktop(Common):
    """
    TR_ID: C1049075
    NAME: Carousel functionality on In-play widget for Desktop
    DESCRIPTION: This test case verifies carousel functionality on In-play widget for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Oxygen app is loaded
    """
    keep_browser_open = True

    def test_001_navigate_to_any_sports_landing_page_that_contains_several_live_events(self):
        """
        DESCRIPTION: Navigate to any Sports Landing page that contains several Live events
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * In-Play widget is displayed in 3-rd column
        EXPECTED: * In-Play widget is expanded by default
        EXPECTED: * Live events are displayed in the carousel
        """
        pass

    def test_002_hover_over_the_carousel(self):
        """
        DESCRIPTION: Hover over the carousel
        EXPECTED: The right arrow appears on the right side of carousel
        """
        pass

    def test_003_click_on_the_right_arrow(self):
        """
        DESCRIPTION: Click on the right arrow
        EXPECTED: * Content scrolls right
        EXPECTED: * Current set of event cards are replaced by the same number of the next cards
        """
        pass

    def test_004_hover_over_the_carousel_again(self):
        """
        DESCRIPTION: Hover over the carousel again
        EXPECTED: Right and left arrows appear on the sides of carousel respectively
        """
        pass

    def test_005_click_on_the_left_arrow(self):
        """
        DESCRIPTION: Click on the left arrow
        EXPECTED: * Content scrolls left
        EXPECTED: * Current set of event cards are replaced by the same number of the next cards
        """
        pass

    def test_006_click_on_right_arrow_till_the_end_of_carousel(self):
        """
        DESCRIPTION: Click on right arrow till the end of carousel
        EXPECTED: * Carousel is not a loop, user is able to get to last Live event card
        EXPECTED: * Right arrow is not displayed at the end of carousel
        EXPECTED: * The last Live event card is displayed at the end of carousel
        """
        pass

    def test_007_navigate_to_any_sports_landing_page_that_contains_only_one_live_event(self):
        """
        DESCRIPTION: Navigate to any Sports Landing page that contains only one Live event
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * In-Play widget is displayed in 3-rd column
        EXPECTED: * In-Play widget is expanded by default
        EXPECTED: * Only one card is displayed within carousel on the whole width of the In-Play widget
        EXPECTED: * Right/left arrows are NOT shown on the sides of carousel
        """
        pass

    def test_008_navigate_to_any_sports_landing_page_that_doesnt_contain_any_live_events(self):
        """
        DESCRIPTION: Navigate to any Sports Landing page that doesn't contain any Live events
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * In-Play widget is NOT displayed in 3-rd column
        """
        pass
