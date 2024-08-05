import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C9240788_HR_Inspired_Virtual_Carousel_not_shown_if_NO_races_available(Common):
    """
    TR_ID: C9240788
    NAME: HR Inspired Virtual Carousel not shown if NO races available
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

    def test_002_navigate_to_the_inspired_virtual_race_module(self):
        """
        DESCRIPTION: Navigate to the 'Inspired Virtual race' module
        EXPECTED: 'Inspired Virtual race' module is shown as Carousel
        """
        pass

    def test_003_verify_carousel_if_therere_no_available_races_for_the_next_7_hours(self):
        """
        DESCRIPTION: Verify carousel if there're no available races for the next 7 hours
        EXPECTED: 'Carousel module' is not shown at all
        """
        pass
