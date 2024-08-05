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
class Test_C1274038_Verify_Media_Area_Displaying(Common):
    """
    TR_ID: C1274038
    NAME: Verify Media Area Displaying
    DESCRIPTION: Verify Media Area displaying on races event details page
    DESCRIPTION: Test case is applicable for 'Horse racing' and 'Greyhounds' details events page
    DESCRIPTION: 'LIVESIM' is not available for 'Greyhounds'
    DESCRIPTION: 'Live Commentary' is not available on mobile and tablet, only on desktop
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: [BMA-6585 - Racecard Layout Update - Media Area] [1].
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-6585
    DESCRIPTION: [BMA-17781 - Live Sim/Watch Free Display Change for Special Open Collapse Button] [2].
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-17979
    DESCRIPTION: [BMA-39820 - Desktop HR+ GH Redesign : Race Page - Streaming redesign] [3].
    DESCRIPTION: [3]: https://jira.egalacoral.com/browse/BMA-39820
    DESCRIPTION: Note: cannot automate as mapped stream is required
    PRECONDITIONS: *   Event has started (scheduled race-off time is not reached)
    PRECONDITIONS: *   Make sure there is mapped race visualization and streaming to tested event
    PRECONDITIONS: *   SiteServer event should be configured to support streaming
    PRECONDITIONS: *   Quantum Leap/Live Sim product is displayed only when it's available based on CMS configs (Log in to CMS and navigate to 'System-configuration' -> 'Config'/'Structure' tab (Coral and Ladbrokes) -> 'QuantumLeapTimeRange')
    PRECONDITIONS: *   Register a valid user account
    PRECONDITIONS: *   The user is logged out
    PRECONDITIONS: URL to **Test/Demo** visualization:  https://www.racemodlr.com/coral-demo/visualiser/{event id} (implemented on DEV, TST2, STG2 environments)
    PRECONDITIONS: URL to **Real **visualization: https://www.racemodlr.com/coral/visualiser/{event id} (implemented on PROD environment)
    PRECONDITIONS: **NOTE**: It event attribute **'typeFlagCodes' **contains 'UK' or 'IE' parameter, this event is included in the group 'UK & IRE'.
    PRECONDITIONS: * URLs for 'Live Commentary' should be set in CMS:
    PRECONDITIONS: GH= https://sport.mediaondemand.net/player/ladbrokes?sport=greyhounds&showmenu=false
    PRECONDITIONS: HR= https://sport.mediaondemand.net/player/ladbrokes?sport=horses&showmenu=false
    PRECONDITIONS: To set links do the following steps:
    PRECONDITIONS: 1) Go to CMS -> System Configuration -> Structure
    PRECONDITIONS: 2) Type in Search field 'LiveCommentary'
    PRECONDITIONS: 3) Paste links in 'Field Value' per each 'Field Name'
    PRECONDITIONS: 4) Click on 'Save changes'
    """
    keep_browser_open = True

    def test_001_go_to_the_event_details_page_of_a_race_from_uk__ire_group_more_than_5_minutes_left_before_the_race_off_time(self):
        """
        DESCRIPTION: Go to the event details page of a race (from 'UK & IRE' group) **more than 5 minutes** left before the race off time
        EXPECTED: Event details page is opened
        """
        pass

    def test_002_verify_the_media_area(self):
        """
        DESCRIPTION: Verify the media area
        EXPECTED: *   The 'PRE-PARADE' and 'LIVE STREAM' buttons are available and inactive
        EXPECTED: *   Relevant icons are shown next to the 'PRE-PARADE' and 'LIVE STREAM' labels (MOBILE)
        EXPECTED: *   Relevant icons are NOT shown next to the 'PRE-PARADE' and 'LIVE STREAM' labels (DESKTOP)
        EXPECTED: *   'Live Commentary' link is displayed (DESKTOP LADBROKES)
        EXPECTED: *   Microphone icon is shown next to the 'Live Commentary' link (DESKTOP LADBROKES)
        """
        pass

    def test_003_tap_on_the_live_stream_for_coral_watch_for_ladbrokes_button_event_has_not_started(self):
        """
        DESCRIPTION: Tap on the 'LIVE STREAM' (for Coral)/ 'WATCH' (for Ladbrokes) button (event has not started)
        EXPECTED: * 'LIVE STREAM'/'WATCH' button becomes active
        EXPECTED: * The area below 'LIVE STREAM'/'WATCH' buttons is expanded
        EXPECTED: * Error Message with 'i' icon is displayed: "In order to watch this stream, you must be logged in."
        EXPECTED: * 'WATCH' label on button is changed to 'DONE' (LADBROKES)
        """
        pass

    def test_004_tap_active_live_streamfor_coraldone_for_ladbrokes_button_one_more_time(self):
        """
        DESCRIPTION: Tap active 'LIVE STREAM'(for Coral)/'DONE' (for Ladbrokes) button one more time
        EXPECTED: * The area below 'LIVE STREAM'/'DONE' button is hidden
        """
        pass

    def test_005_login_to_the_app_with_the_user_from_preconditions_and_verify_the_media_area(self):
        """
        DESCRIPTION: Login to the app with the user from preconditions and verify the media area
        EXPECTED: * 'LIVE STREAM ' button becomes inactive
        EXPECTED: * The area below 'LIVE STREAM' buttons is collapsed
        """
        pass

    def test_006_tap_on_the_live_stream_for_coral_watch_for_ladbrokes_button_event_has_not_started(self):
        """
        DESCRIPTION: Tap on the 'LIVE STREAM' (for Coral)/ 'WATCH' (for Ladbrokes) button (event has not started)
        EXPECTED: * The area below 'LIVE STREAM'/'WATCH' button is expanded
        EXPECTED: * Error Message with 'i' icon is displayed: "This stream has not yet started. Please try again soon."
        EXPECTED: * 'WATCH' label on button is changed to 'DONE' (LADBROKES)
        """
        pass

    def test_007_tap_active_live_streamfor_coraldone_for_ladbrokes_button_one_more_time(self):
        """
        DESCRIPTION: Tap active 'LIVE STREAM'(for Coral)/'DONE' (for Ladbrokes) button one more time
        EXPECTED: * The area below 'LIVE STREAM'/'DONE' button is hidden
        """
        pass

    def test_008_tap_on__live_stream_for__coralwatch_for_ladbrokes_button_event_has_started(self):
        """
        DESCRIPTION: Tap on  'LIVE STREAM' (for  Coral)/'WATCH' (for Ladbrokes) button (event has started)
        EXPECTED: * The area below 'LIVE STREAM'/'WATCH' buttons is expanded
        EXPECTED: * Error Message with 'i' icon is displayed:"In order to view this event you should place a bet greater than or Equal to <currency><value>"(amount should be equal to 1pound and currency depends on user currency selected)
        EXPECTED: * 'WATCH' label on button is changed to 'DONE' (LADBROKES)
        """
        pass

    def test_009_tap_active_live_streamfor_coraldone_for_ladbrokes_button_one_more_time(self):
        """
        DESCRIPTION: Tap active 'LIVE STREAM'(for Coral)/'DONE' (for Ladbrokes) button one more time
        EXPECTED: * The area below 'LIVE STREAM'/'DONE' button is hidden
        """
        pass

    def test_010_place_a_1_bet_on_one_or_many_selections(self):
        """
        DESCRIPTION: Place a £1 bet on one or many Selections
        EXPECTED: 
        """
        pass

    def test_011_tap_on__live_stream_for__coralwatch_for_ladbrokes_button_event_has_started(self):
        """
        DESCRIPTION: Tap on  'LIVE STREAM' (for  Coral)/'WATCH' (for Ladbrokes) button (event has started)
        EXPECTED: * The area below 'LIVE STREAM'/'WATCH' button is expanded
        EXPECTED: * The stream is shown for the user
        """
        pass

    def test_012_tap_active_live_streamfor_coraldone_for_ladbrokes_button_one_more_time(self):
        """
        DESCRIPTION: Tap active 'LIVE STREAM'(for Coral)/'DONE' (for Ladbrokes) button one more time
        EXPECTED: * The area below 'LIVE STREAM'/'DONE' button is hidden
        """
        pass

    def test_013_tap_on_the_pre_parade_button(self):
        """
        DESCRIPTION: Tap on the 'PRE-PARADE' button
        EXPECTED: * 'PRE-PARADE' button becomes active
        EXPECTED: * The area below 'PRE-PARADE' button is expanded
        EXPECTED: * Visualization video object is shown
        EXPECTED: * An information link labeled "Find out more about Watch Free here" with '?' mark appears under Media Area on the page
        EXPECTED: * 'PRE-PARADE' label on button changes to 'DONE' (LADBROKES)
        """
        pass

    def test_014_tap_active_pre_parade_for_coral_done_for_ladbrokes_button(self):
        """
        DESCRIPTION: Tap active 'PRE-PARADE' (for Coral)/ 'DONE' (for Ladbrokes) button
        EXPECTED: * The area below 'PRE-PARADE' button is collapsed
        EXPECTED: * The information link is no longer displayed
        EXPECTED: * The area below 'DONE' button is collapsed (LADBROKES)
        EXPECTED: * 'DONE' label on button changes to 'PRE-PARADE'(LADBROKES)
        """
        pass
