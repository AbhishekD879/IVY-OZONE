import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.streaming
@vtest
class Test_C29237_Watching_a_Perform_Stream_with_incorrect_configuration(Common):
    """
    TR_ID: C29237
    NAME: Watching a Perform Stream with incorrect configuration
    DESCRIPTION: User is  trying to watch a Stream when CMS configuration for that specific stream provider is incorrect.
    PRECONDITIONS: 1. SiteServer event should be configured to support Perform streaming (**'typeFlagCodes'**='PVA , ... ' AND **'drilldownTagNames'**='EVFLAG_PVM' flags should be set) and should be mapped to Perform stream event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: *   isStarted = "true"
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: 3. User is logged in and has a positive balance
    PRECONDITIONS: 4. Ukraine should be whitelisted by Perform
    PRECONDITIONS: 5. Change CMS configurations for Perform stream to incorrect values here:
    PRECONDITIONS: Before OX103: CMS -> System Configuration -> Structure -> 'performGroup'
    PRECONDITIONS: After OX103: CMS -> Secrets -> 'PerformGroup'
    PRECONDITIONS: **Postconditions**
    PRECONDITIONS: All configurations should be set to DEFAULT again:
    PRECONDITIONS: *   **desktopPartnerId **= 905
    PRECONDITIONS: *   **desktopUserId **= test
    PRECONDITIONS: *   **mobilePartnerId **= 2864
    PRECONDITIONS: *   **mobileUserId **= test
    PRECONDITIONS: *   **desktopSeed=**3GVJr687Z2KSTu2r3J7D
    PRECONDITIONS: *   **mobileSeed**=2fhghg46565kjlkill56
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_sport_for_the_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Sport> for the event which satisfies Preconditions
        EXPECTED: Event details page is opened
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: 'Watch Live' button is shown when scoreboard is present(for both brands);
        EXPECTED: 'Watch' ![](index.php?/attachments/get/3050950) (Coral) / ![](index.php?/attachments/get/3050951) (Ladbrokes) button is shown when scoreboard is absent.
        EXPECTED: -
        EXPECTED: **For Desktop:**
        EXPECTED: 'Watch Live' ![](index.php?/attachments/get/3050948) (Coral) / ![](index.php?/attachments/get/3050949) (Ladbrokes) button is shown in case of scoreboard/visualization being present.
        EXPECTED: * No stream buttons are shown if Stream is available WITHOUT mapped Visualization/Scoreboard
        """
        pass

    def test_002_for_desktop_onlyverify_that_warning_message_is_shown_on_edp_if_no_stream_buttons_are_shown(self):
        """
        DESCRIPTION: **For Desktop only:**
        DESCRIPTION: Verify that warning message is shown on EDP (if no stream buttons are shown)
        EXPECTED: * Warning message with following text is shown above the market tabs lane: "The Stream for this event is currently not available."
        EXPECTED: * User is not able to watch the stream
        """
        pass

    def test_003_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: * [ **Coral** desktop / **Ladbrokes** desktop]: Message is displayed: "The Stream for this event is currently not available."
        EXPECTED: * [ **Ladbrokes** and **Coral** tablet/mobile]: Pop up opens with message "The Stream for this event is currently not available."
        EXPECTED: * User is not able to watch the stream
        EXPECTED: * Application has not crashed
        """
        pass

    def test_004_for_desktop_onlynavigate_to_in_play_and_live_stream_section_on_homepage_and_switch_to_live_stream(self):
        """
        DESCRIPTION: **For Desktop only:**
        DESCRIPTION: Navigate to 'IN-PLAY AND LIVE STREAM ' section on Homepage and switch to 'LIVE STREAM'
        EXPECTED: Stream of 1st event on a list is launched automatically
        EXPECTED: Stream is shown in the player frame below 'In-Play' and 'Live Stream' tabs
        """
        pass

    def test_005_for_desktop_onlymake_the_event_from_step_3_appear_at_the_topas_first_one_of_the_live_stream_events_list_and_refresh_the_page(self):
        """
        DESCRIPTION: **For Desktop only:**
        DESCRIPTION: Make the event from step 3 appear at the top(as first one) of the Live Stream events list and refresh the page
        EXPECTED: Message is displayed: 'The Stream for this event is currently not available'.
        EXPECTED: User is not able to watch the stream
        """
        pass
