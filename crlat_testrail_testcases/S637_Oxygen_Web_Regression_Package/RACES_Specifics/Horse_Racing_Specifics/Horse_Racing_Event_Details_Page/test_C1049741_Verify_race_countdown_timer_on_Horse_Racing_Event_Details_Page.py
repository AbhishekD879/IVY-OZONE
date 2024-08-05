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
class Test_C1049741_Verify_race_countdown_timer_on_Horse_Racing_Event_Details_Page(Common):
    """
    TR_ID: C1049741
    NAME: Verify race countdown timer on Horse Racing Event Details Page
    DESCRIPTION: This test case verifies the new race start countdown timer module introduced as part of HR Landing page redesign.
    DESCRIPTION: The timer module will be used across Next 4, racing grids, on EDP
    DESCRIPTION: AUTOTEST: [C1501504]
    PRECONDITIONS: * To verify specific event attributes (in this case: startTime, raceStage ), use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: * XXX - the event ID
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: * The countdown timer should use the start time as specified in Openbet TI
    """
    keep_browser_open = True

    def test_001_select_an_event_where_the_race_start_time_is_more_than_45_minutes(self):
        """
        DESCRIPTION: Select an event where the Race start time is more than 45 minutes
        EXPECTED: Event Details Page is opened
        EXPECTED: A countdown timer is not displayed
        """
        pass

    def test_002_select_an_event_where_the_race_start_time_is_less_than_or_equal_to_45_minutes(self):
        """
        DESCRIPTION: Select an event where the Race start time is less than or equal to 45 minutes
        EXPECTED: Event Details Page is opened
        EXPECTED: Countdown timer displays corresponding time left
        """
        pass

    def test_003_select_an_event_where_the_race_start_time_is_more_than_45_minutes_eg_50_min__wait_till_45_minutes_is_left_to_start(self):
        """
        DESCRIPTION: Select an event where the Race start time is more than 45 minutes (e.g. 50 min),  wait till 45 minutes is left to start
        EXPECTED: Event Details Page is opened
        EXPECTED: A timer module counting down from 45 minutes is displayed
        """
        pass

    def test_004_refresh_event_details_page(self):
        """
        DESCRIPTION: Refresh event details page
        EXPECTED: Countdown timer displays corresponding time left
        """
        pass

    def test_005_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to Horse Racing Landing Page
        EXPECTED: Countdown timer is not displayed for any event in the Race Grid
        """
        pass
