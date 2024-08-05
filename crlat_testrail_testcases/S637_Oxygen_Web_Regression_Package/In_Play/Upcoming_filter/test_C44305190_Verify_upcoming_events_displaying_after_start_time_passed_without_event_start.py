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
class Test_C44305190_Verify_upcoming_events_displaying_after_start_time_passed_without_event_start(Common):
    """
    TR_ID: C44305190
    NAME: Verify upcoming events displaying after start time passed without event start
    DESCRIPTION: This test case verifies upcoming events displaying after start time passed without event start
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Make sure that Upcoming events are present in 'Upcoming' section of 'In-Play' page (for mobile/tablet) or when 'Upcoming' switcher is selected (for Desktop)
    PRECONDITIONS: 3. Make sure there is the event with the following settings:
    PRECONDITIONS: * startTime of less than or equal current time in UTC plus 24 hours
    PRECONDITIONS: * 'drilldownTagNames' with 'EVFLAG_BL'
    PRECONDITIONS: * at least one market with attribute 'isMarketBetInRun' = 'true'
    PRECONDITIONS: * WITHOUT attribute is_off='Y' and without attribute 'isStarted'
    PRECONDITIONS: Note:
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::UPCOMING_EVENT::XXX"
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    """
    keep_browser_open = True

    def test_001_verify_upcoming_events_within_the_page(self):
        """
        DESCRIPTION: Verify upcoming events within the page
        EXPECTED: Event from the preconditions is present within the 'Upcoming' section
        """
        pass

    def test_002_verify_event_attributes(self):
        """
        DESCRIPTION: Verify event attributes
        EXPECTED: Upcoming events do not include attributes:
        EXPECTED: * 'isNext24HourEvent'
        EXPECTED: Upcoming events include attributes:
        EXPECTED: * eventStatusCode: "A"
        EXPECTED: * isLiveNowOrFutureEvent: "true"
        """
        pass

    def test_003_modify_event_to_be_defined_by_attributes_is_off__y_and_event_attribute_isstarted(self):
        """
        DESCRIPTION: Modify event to be defined by attributes is_off = 'Y' and event attribute isStarted
        EXPECTED: * Event disappears from 'Upcoming' section
        EXPECTED: * Event is displayed in 'In-Play' section
        """
        pass
