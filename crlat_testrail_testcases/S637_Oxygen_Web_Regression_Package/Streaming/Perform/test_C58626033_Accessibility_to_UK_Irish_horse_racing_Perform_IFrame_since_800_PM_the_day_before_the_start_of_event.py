import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C58626033_Accessibility_to_UK_Irish_horse_racing_Perform_IFrame_since_800_PM_the_day_before_the_start_of_event(Common):
    """
    TR_ID: C58626033
    NAME: Accessibility to UK/Irish horse racing Perform IFrame since 8:00 PM the day before the start of event
    DESCRIPTION: This test case verifies accessibility to iFrame for Perform stream  with pre-stream info for the active user since 8:00 PM the day before the start of event
    PRECONDITIONS: **Preconditions for UK/Irish horse racing events:**
    PRECONDITIONS: * The PERFORM streams are mapped
    PRECONDITIONS: * In CMS (https://cms-api-ui-dev0.coralsports.dev.cloud.ladbrokescoral.com/system-configuration/structure) in section **performGroup** **CSBIframeEnabled** is enabled and sport ID 21 is present
    PRECONDITIONS: * App is loaded
    PRECONDITIONS: * Active User is logged in
    PRECONDITIONS: * User is navigated to Race EDP with a stream
    """
    keep_browser_open = True

    def test_001_user_clicks_on_the_live_streamwatch_button_at_any_time_from_the_range_12_am___759_pm_the_day_before_the_start_of_event(self):
        """
        DESCRIPTION: User clicks on the LIVE STREAM/WATCH button at any time from the range: 12 AM - 7:59 PM the day before the start of event.
        EXPECTED: iFrame is unavailable
        EXPECTED: The message appears: **The Stream for this event is currently not available.**
        """
        pass

    def test_002_user_clicks_on_the_live_streamwatch_button_at_any_time_from_the_range_800_pm_the_day_before_the_start_of_event___5_min_before_the_stream_started(self):
        """
        DESCRIPTION: User clicks on the LIVE STREAM/WATCH button at any time from the range: 8:00 PM the day before the start of event - 5 min before the stream started
        EXPECTED: iFrame is available with pre-stream information
        EXPECTED: ![](index.php?/attachments/get/104594961)
        EXPECTED: * Paddock tab - Default loading tab before live video is available
        EXPECTED: Content to be available from 20:00 the day before the race
        EXPECTED: * Predictor tab - Animated video prediction of race outcome
        EXPECTED: Content to be available from 20:00 the day before the race
        EXPECTED: * Stats tab - Highlights key statistical data for each rate i.e. strike rates Content to be available from 20:00 the day before the race
        EXPECTED: * Analysis tab - Highlighting potential draw basis and pace
        EXPECTED: Content to be available from 20:00 the day before the race
        EXPECTED: * Video form tab - Automated real life video archive for key runners in each race Video focuses on key runners in each race
        EXPECTED: Content to be available from 20:00 the day before the race
        """
        pass
