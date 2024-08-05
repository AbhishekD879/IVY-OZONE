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
class Test_C29228_Launching_Perform_Stream_when_User_is_logged_out(Common):
    """
    TR_ID: C29228
    NAME: Launching Perform Stream when User is logged out
    DESCRIPTION: User is trying to launch stream in logged out state.
    DESCRIPTION: Applies to <Race>/<Sport> events.
    PRECONDITIONS: 1. SiteServer event should be configured to support Perform streaming (**'typeFlagCodes'**='PVA , ... ' AND **'drilldownTagNames'**='EVFLAG_PVM' flags should be set)
    PRECONDITIONS: 2. Load Oxygen application as logged out user
    PRECONDITIONS: 3. The event should have the following attributes:
    PRECONDITIONS: for 'Sport' events: isStarted = "true";
    PRECONDITIONS: for 'Race' events: isStarted = "true", but stream has not run for more than 1 minute after the 'start time'
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
        EXPECTED: * Warning message with following text is shown above the market tabs lane: "In order to watch this stream, you must be logged in."
        EXPECTED: * No request is sent to OptIn MS
        EXPECTED: * User is not able to watch the stream
        """
        pass

    def test_003_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: * No request is sent to OptIn MS
        EXPECTED: * [ **Coral** desktop/ **Ladbrokes** desktop]: Message is displayed: "In order to watch this stream, you must be logged in."
        EXPECTED: * [ **Ladbrokes** and **Coral** tablet/mobile]: Pop up opens with message "In order to watch this stream, you must be logged in."
        EXPECTED: * User is not able to watch the stream
        """
        pass

    def test_004_log_in_to_the_apptapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: Log in to the app.
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: * Stream is launched
        EXPECTED: * Request to OptIn MS is sent (see preconditions) to identify stream provider
        EXPECTED: * **listingUrl** attribute is received from OptIn MS to consume streaming
        EXPECTED: * The next provider info is received from Optin MS:
        EXPECTED: {
        EXPECTED: priorityProviderCode: "PERFORM"
        EXPECTED: priorityProviderName: "Perform"
        EXPECTED: }
        """
        pass

    def test_005_open_event_details_page_of_any_race_event_that_satisfies_preconditions_and_with_log_out_user(self):
        """
        DESCRIPTION: Open Event Details Page of any <Race> event that satisfies Preconditions and with log out user
        EXPECTED: * Desktop:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050952) (Coral) / 'Watch' ![](index.php?/attachments/get/3050953) (Ladbrokes) button is shown below the event name line
        EXPECTED: * Mobile/Tablet:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050954) (Coral) / 'Watch' ![](index.php?/attachments/get/3050955) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_006_all_devicestapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch'/'Live Stream' button
        EXPECTED: Expected Results match those, described in step 3
        """
        pass

    def test_007_log_in_to_the_app_with_user_who_placed_bet_for_more_than_1_pound_for_the_eventtapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: Log in to the app with user, who placed bet for more than 1 pound for the event.
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: * Stream is launched
        EXPECTED: * Request to OptIn MS is sent (see preconditions) to identify stream provider
        EXPECTED: * **listingUrl** attribute is received from OptIn MS to consume streaming
        EXPECTED: * The next provider info is received from Optin MS:
        EXPECTED: {
        EXPECTED: priorityProviderCode: "PERFORM"
        EXPECTED: priorityProviderName: "Perform"
        EXPECTED: }
        """
        pass
