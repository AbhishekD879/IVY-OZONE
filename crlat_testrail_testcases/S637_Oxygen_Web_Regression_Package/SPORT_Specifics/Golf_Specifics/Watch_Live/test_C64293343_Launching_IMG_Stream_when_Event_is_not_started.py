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
class Test_C64293343_Launching_IMG_Stream_when_Event_is_not_started(Common):
    """
    TR_ID: C64293343
    NAME: Launching IMG Stream when Event is not started
    DESCRIPTION: User is trying to launch stream when it is more than 15 minutes left to its start time. Applies to Golf events
    PRECONDITIONS: SiteServer event should be configured to support IMG streaming (**'typeFlagCodes'**='IVA , ... ' AND 'drilldownTagNames'='EVFLAG_IVM' flags should be set) and should be mapped to IMG stream event
    PRECONDITIONS: More than 15 min left to event start time. Event should not be started
    PRECONDITIONS: User is logged into the Oxygen app and has a positive balance
    PRECONDITIONS: Endpoints of Optin MS:
    PRECONDITIONS: https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Coral
    PRECONDITIONS: https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Ladbrokes
    PRECONDITIONS: https://optin-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - tst2 Coral
    PRECONDITIONS: https://optin-tst0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - tst2 Ladbrokes
    PRECONDITIONS: https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - prod Coral
    PRECONDITIONS: https://optin-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - prod Ladbrokes
    PRECONDITIONS: https://optin-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - beta Coral
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
        EXPECTED: Warning message with following text is shown above the market tabs lane: "This stream has not yet started. Please try again soon"
        EXPECTED: Request to OptIn MS is sent (see preconditions) to indetify stream provider
        EXPECTED: User is not able to watch the stream
        """
        pass

    def test_003_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: All Devices
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: [ Coral desktop / Ladbrokes desktop]: Message is displayed: "This stream has not yet started. Please try again soon"
        EXPECTED: [ Ladbrokes and Coral tablet/mobile]: Pop up opens with message "This stream has not yet started. Please try again soon". There's an 'Event countdown' to event start time under the message.
        EXPECTED: User is not able to watch the stream
        EXPECTED: Request to OptIn MS is sent (see preconditions) to indetify stream provider
        EXPECTED: The next provider info is received from Optin MS:
        EXPECTED: {
        EXPECTED: priorityProviderCode: "IMG"
        EXPECTED: priorityProviderName: "IMG Video Streaming"
        EXPECTED: }
        """
        pass
