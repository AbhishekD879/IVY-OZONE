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
class Test_C59551034_Verify_Betradar_Scoreboard_slides_navigation(Common):
    """
    TR_ID: C59551034
    NAME: Verify Betradar Scoreboard-slides navigation
    DESCRIPTION: This test case verifies navigation of slides in betradar visualization
    PRECONDITIONS: Make sure you have Table Tennis upcoming event which is subscribed to Betradar Scoreboards
    PRECONDITIONS: Navigate to Inplay-> Table Tennis -> Tap on event (which is subscribed to betradar)
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_upcoming_event_as_per_the_pre_conditions(self):
        """
        DESCRIPTION: Navigate to Event Details Page of upcoming event as per the pre-conditions
        EXPECTED: Event Details Page should be opened with event visualization and scoreboards
        """
        pass

    def test_002_verify_display_of_slides_in_table_tennis_court(self):
        """
        DESCRIPTION: Verify display of slides in table tennis court
        EXPECTED: Application should display slides and small rectangles at bottom of the slides
        EXPECTED: + By default The first rectangle is highlighted with blue color corresponding to first selected slide (the rest rectangles are white)
        """
        pass

    def test_003_click_on_next_rectangle_button(self):
        """
        DESCRIPTION: Click on next rectangle button
        EXPECTED: + Next slide should be shown
        EXPECTED: + The second rectangle should be highlighted with blue color
        """
        pass

    def test_004_navigate_till_last_slide_and_click_on_first_rectangle_button(self):
        """
        DESCRIPTION: Navigate till last slide and click on first rectangle button
        EXPECTED: + Again the first slide should be shown
        EXPECTED: + The first rectangle is highlighted with blue color
        """
        pass

    def test_005_on_mobiletablet_repeat_steps_2_4(self):
        """
        DESCRIPTION: On mobile/tablet repeat steps #2-4
        EXPECTED: 
        """
        pass

    def test_006_from_table_tennis_court_widgetswipe_to_the_left(self):
        """
        DESCRIPTION: From Table Tennis court widget
        DESCRIPTION: swipe to the left
        EXPECTED: + Next slide should be shown
        EXPECTED: + The second rectangle should be highlighted with blue color
        """
        pass

    def test_007_swipe_to_the_right(self):
        """
        DESCRIPTION: Swipe to the right
        EXPECTED: + Previous slide should be shown
        EXPECTED: + The first rectangle should be highlighted with blue color
        """
        pass

    def test_008_navigate_to_the_last_slide_and_swipe_to_the_left(self):
        """
        DESCRIPTION: Navigate to the last slide and swipe to the left
        EXPECTED: + Again the first slide should be shown
        EXPECTED: + The first rectangle should be highlighted with blue color
        """
        pass

    def test_009_swipe_to_the_right(self):
        """
        DESCRIPTION: Swipe to the right
        EXPECTED: + Last slide should be shown
        EXPECTED: + The last rectangle should be highlighted with blue color
        """
        pass
