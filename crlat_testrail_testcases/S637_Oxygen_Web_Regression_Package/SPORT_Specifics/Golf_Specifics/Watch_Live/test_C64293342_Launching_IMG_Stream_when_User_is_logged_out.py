import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64293342_Launching_IMG_Stream_when_User_is_logged_out(Common):
    """
    TR_ID: C64293342
    NAME: Launching IMG Stream when User is logged out
    DESCRIPTION: User is trying to launch stream in logged out state. Applies to Golf events.
    PRECONDITIONS: SiteServer event should be configured to support IMG streaming (**'typeFlagCodes'**='IVA , ... ' AND 'drilldownTagNames'='EVFLAG_IVM' flags should be set)
    PRECONDITIONS: Load Oxygen application as logged out user
    PRECONDITIONS: The event should have the following attributes:
    PRECONDITIONS: isStarted = "true"
    """
    keep_browser_open = True

    def test_001_open_event_details_page_for_the_golf_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page for the golf event which satisfies Preconditions
        EXPECTED: Event details page is opened
        EXPECTED: For Mobile/Tablet:
        EXPECTED: 'Watch Live' button is shown when scoreboard is present(for both brands);
        EXPECTED: 'Watch'  (Coral) /  (Ladbrokes) button is shown when scoreboard is absent.
        EXPECTED: -
        EXPECTED: For Desktop:
        EXPECTED: 'Watch Live'  (Coral) /  (Ladbrokes) button is shown in case of scoreboard/visualization being present.
        EXPECTED: No stream buttons are shown if Stream is available WITHOUT mapped Visualization/Scoreboard
        """
        pass

    def test_002_for_desktop_onlyverify_that_warning_message_is_shown_on_edp_if_no_stream_buttons_are_shown(self):
        """
        DESCRIPTION: For Desktop only:
        DESCRIPTION: Verify that warning message is shown on EDP (if no stream buttons are shown)
        EXPECTED: Warning message with following text is shown above the market tabs lane: "In order to watch this stream, you must be logged in."
        EXPECTED: No request is sent to OptIn MS
        EXPECTED: User is not able to watch the stream
        """
        pass

    def test_003_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: All Devices
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: No request is sent to OptIn MS
        EXPECTED: [ Coral desktop / Ladbrokes desktop]: Message is displayed: "In order to watch this stream, you must be logged in."
        EXPECTED: [ Ladbrokes and Coral tablet/mobile]: Pop up opens with message "In order to watch this stream, you must be logged in."
        EXPECTED: User is not able to watch the stream
        """
        pass

    def test_004_log_in_to_the_apptapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: Log in to the app.
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: Request to OptIn MS is sent to indetify stream provider
        EXPECTED: listingUrl attribute is received from https://dge.imggaming.com/api/v2/streaming/events/{eventID}/stream?operatorId=26&auth=de68cd07dd16983b6f6a7eadf0313b85&timestamp=1571814531496&page.page=2&page.size=1 to consume stream [eventID is needed to be inserted in order to view data]
        EXPECTED: The next provider info is received from Optin MS:
        EXPECTED: {
        EXPECTED: priorityProviderCode: "IMG"
        EXPECTED: priorityProviderName: "IMG Video Streaming"
        EXPECTED: }
        EXPECTED: Stream is launched
        """
        pass
