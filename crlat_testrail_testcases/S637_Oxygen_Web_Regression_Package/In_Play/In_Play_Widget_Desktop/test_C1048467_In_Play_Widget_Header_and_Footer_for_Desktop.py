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
class Test_C1048467_In_Play_Widget_Header_and_Footer_for_Desktop(Common):
    """
    TR_ID: C1048467
    NAME: In-Play Widget Header and Footer for Desktop
    DESCRIPTION: This test case verifies In-Play Widget Header and Footer for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Navigate to Sports Landing page that contains Live events
    PRECONDITIONS: 3. Choose 'Matches' tab
    PRECONDITIONS: 4. Make sure that In-Play widget is displayed in 3-rd column and expanded by default
    PRECONDITIONS: 5. Live events are displayed in the carousel
    """
    keep_browser_open = True

    def test_001_verify_in_play_widget_header(self):
        """
        DESCRIPTION: Verify In-Play widget Header
        EXPECTED: In-Play widget Header contains:
        EXPECTED: * Capitalized text 'In-Play'
        EXPECTED: * 'Live' badge
        EXPECTED: * Capitalized Sport name e.g. 'Football'
        EXPECTED: * Up/down chevron
        """
        pass

    def test_002_verify_in_play_widget_footer_when_there_is_only_1_in_play_event(self):
        """
        DESCRIPTION: Verify In-Play widget Footer when there is only 1 In-Play event
        EXPECTED: * In-Play widget Footer contains 'View all in-play events' link
        EXPECTED: * Link takes the user to 'In-play' page with selected 'All Sports' tab in Sports Menu Ribbon
        """
        pass

    def test_003_verify_in_play_widget_footer_when_there_are_more_than_1_in_play_events(self):
        """
        DESCRIPTION: Verify In-Play widget Footer when there are more than 1 In-Play events
        EXPECTED: * In-Play widget Footer contains 'View all in-play events' link
        EXPECTED: * Link takes user to 'In-play' page with specific sport selected in Sports Menu Ribbon e.g. Football
        """
        pass

    def test_004_click_anywhere_in_the_header(self):
        """
        DESCRIPTION: Click anywhere in the header
        EXPECTED: * Widget gets collapsed together with footer
        EXPECTED: * Up chevron changes to down one
        """
        pass

    def test_005_click_again_anywhere_in_the_header(self):
        """
        DESCRIPTION: Click again anywhere in the header
        EXPECTED: * Widget gets expanded: in-play cards and footer are shown
        EXPECTED: * Down chevron changes to up one
        """
        pass
