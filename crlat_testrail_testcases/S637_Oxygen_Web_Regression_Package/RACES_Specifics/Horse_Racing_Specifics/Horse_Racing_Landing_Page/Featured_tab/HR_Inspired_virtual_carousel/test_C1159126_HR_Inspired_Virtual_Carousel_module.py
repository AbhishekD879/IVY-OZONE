import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1159126_HR_Inspired_Virtual_Carousel_module(Common):
    """
    TR_ID: C1159126
    NAME: HR Inspired Virtual Carousel module
    DESCRIPTION: This test case verifies Carousel module on the Horse Racing Landing page with count down timer for the video
    PRECONDITIONS: - Ordering of HR Inspired Virtual Carousel module is configured in CMS
    PRECONDITIONS: - Video starts on 1min20 sec earlier than event starts (Video starts = eventStartTime + 1min20 sec. )
    PRECONDITIONS: - "eventIsOff" time = 45 seconds after stream for an event is finished.
    PRECONDITIONS: - To get the Inspired Virtual events check modules ('Virtual Race Carousel' module, the name can be changed in CMS) in 'FEATURED_STRUCTURE_CHANGED' request from websocket (wss://featured-sports)
    PRECONDITIONS: Example of Virtual event structure:
    PRECONDITIONS: {
    PRECONDITIONS: id: "230549330",
    PRECONDITIONS: name: "Derby Downs",
    PRECONDITIONS: startTime: "2020-06-19T17:26:00Z",
    PRECONDITIONS: classId: "285"
    PRECONDITIONS: }
    PRECONDITIONS: - Amount of events in Inspired Virtual carousel can be set in CMS: Sports Pages-> Sport Categories -> Horse Racing/Greyhounds -> **'limit'** field
    PRECONDITIONS: Default value is 5, min is 1, max is 12 events.
    PRECONDITIONS: - Types and classes for Inspired Virtuals can be changed in CMS: Sports Pages-> Sport Categories -> Horse Racing/Greyhounds -> **'excludeTypeIDs'** and **'classId'** fields
    PRECONDITIONS: **'excludeTypeIDs' default values for different profiles are**:
    PRECONDITIONS: tst: ['3048', '3049', '3123'],
    PRECONDITIONS: stg: ['16576', '16575', '16602'],
    PRECONDITIONS: prod: ['28977', '28975', '29346']
    PRECONDITIONS: **'classId'** default value is **285** (for Horse Racing) and **286** (for Greyhounds)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Oxygen application is loaded
        """
        pass

    def test_002_on_homepage_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: On homepage tap 'Horse Racing' icon from the Sports Menu Ribbon
        EXPECTED: Horse Racing landing page is opened
        """
        pass

    def test_003_navigate_to_the_inspired_virtual_race_module(self):
        """
        DESCRIPTION: Navigate to the 'Inspired Virtual race' module
        EXPECTED: 'Inspired Virtual race' module is shown as Carousel
        """
        pass

    def test_004_verify_hr_virtual_carousel_module(self):
        """
        DESCRIPTION: Verify 'HR Virtual Carousel' module
        EXPECTED: 'HR Virtual Carousel' module is expanded by default and may be collapsed/expanded once tapped
        """
        pass

    def test_005_verify_the_meetings_within_inspired_virtual_carousel(self):
        """
        DESCRIPTION: Verify the meetings within 'Inspired Virtual' carousel
        EXPECTED: - Header with name of meeting
        EXPECTED: - Start time of the race
        EXPECTED: - Count down timer for the video to start (for events that are not yet started)
        EXPECTED: - 'LIVE' badge instead of countdown timer (appears when eventStartTime + 1min20 sec.)
        EXPECTED: - 'BET NOW' clickable link for the events that are not yet started
        EXPECTED: - For events with 'Live' badge > the whole meeting area is clickable
        EXPECTED: - Only 5 next races are available within the carousel
        EXPECTED: - The last one is card with 'View all virtual events' clickable link
        EXPECTED: - Meetings may be swiped left/right within the carousel
        EXPECTED: **For tablet/desktop:**
        EXPECTED: - Meetings may be swiped left/right within the carousel using hover over arrows
        EXPECTED: - When first/last card is shown left/right hover over arrow is not shown
        """
        pass
