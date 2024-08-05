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
class Test_C29000_Verify_Media_Area(Common):
    """
    TR_ID: C29000
    NAME: Verify Media Area
    DESCRIPTION: Verify Media Area on races event details page: Live Stream button for **mobile&tablet** / Live Stream switcher for **desktop**
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: BMA-6585 - Racecard Layout Update - Media Area
    DESCRIPTION: BMA-17781 - Live Sim/Watch Free Display Change for Special Open Collapse Button
    PRECONDITIONS: SiteServer event should be configured to support streaming
    """
    keep_browser_open = True

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_greyhounds_landing_page(self):
        """
        DESCRIPTION: Go to Greyhounds landing page
        EXPECTED: Greyhounds landing page is opened
        """
        pass

    def test_003_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_verify_media_area(self):
        """
        DESCRIPTION: Verify media area
        EXPECTED: *   Media area consists of 'LIVE STREAM' button
        EXPECTED: *   'LIVE STREAM' button is in state inActive
        EXPECTED: *   'LIVE STREAM' media button is displayed filling all available width
        EXPECTED: *   Relevant icon is shown next to the 'LIVE STREAM' label
        """
        pass

    def test_005_tap_inactive_live_stream_button(self):
        """
        DESCRIPTION: Tap inActive 'LIVE STREAM' button
        EXPECTED: *   'LIVE STREAM ' button becomes Active
        EXPECTED: *   The area below 'LIVE STREAM' buttons is expanded
        EXPECTED: *   Error Message with 'i' icon is displayed for mobile&tablet: "In order to watch this stream, you must be logged in."
        EXPECTED: *   Error Message with NO icon is displayed in the middle of media area
        """
        pass

    def test_006_login(self):
        """
        DESCRIPTION: Login
        EXPECTED: *   'LIVE STREAM ' button becomes inActive
        EXPECTED: *   The area below 'Live STREAM' buttons is collapsed
        """
        pass

    def test_007_tap_inactive_live_stream_button_event_has_not_started(self):
        """
        DESCRIPTION: Tap inActive 'LIVE STREAM' button (event has not started)
        EXPECTED: *   'LIVE STREAM ' button becomes Active
        EXPECTED: *   The area below 'LIVE STREAM' buttons is expanded
        EXPECTED: *   Error Message with 'i' icon is displayed for mobile&tablet: "This stream has not yet started. Please try again soon."
        EXPECTED: *   Error Message with NO icon is displayed in the middle of media area
        """
        pass

    def test_008_wait_till_event_starts(self):
        """
        DESCRIPTION: Wait till event starts
        EXPECTED: * Error disappears
        EXPECTED: *  'LIVE STREAM ' button becomes inActive
        """
        pass

    def test_009_tap_inactive_live_stream_button_event_has_started(self):
        """
        DESCRIPTION: Tap inActive 'LIVE STREAM' button (event has started)
        EXPECTED: *   'LIVE STREAM ' button becomens Active
        EXPECTED: *   The area below 'LIVE STREAM' buttons is expanded
        EXPECTED: *   Error Message with 'i' icon is displayed for mobile&tablet:"In order to view this event you should place a bet greater then or Equal to <currency><value>"(amount  should be equal to 1pound and currency depends on user currency selected)
        EXPECTED: *   Error Message with NO icon is displayed in the middle of media area
        """
        pass

    def test_010_user_placed_a_minimum_sum_of_1_on_one_or_many_selections_within_tested_event(self):
        """
        DESCRIPTION: User placed a minimum sum of £1 on one or many Selections within tested event
        EXPECTED: 
        """
        pass

    def test_011_tap_active_live_stream_button_event_has_started(self):
        """
        DESCRIPTION: Tap Active 'LIVE STREAM' button (event has started)
        EXPECTED: *   'LIVE STREAM ' button remains Active
        EXPECTED: *   The area below 'LIVE STREAM' buttons is expanded to show the Video Stream
        EXPECTED: *   The 'Possible delay: 10 seconds' text message is appeared above the video object before video streaming translation
        """
        pass

    def test_012_tap_active_live_stream_button_one_more_time(self):
        """
        DESCRIPTION: Tap Active 'LIVE STREAM' button one more time
        EXPECTED: *   The area below 'LIVE STREAM' button is hidden
        EXPECTED: *   'LIVE STREAM' button becomes inActive
        """
        pass
