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
class Test_C29261_Launching_Stream_when_User_is_logged_out(Common):
    """
    TR_ID: C29261
    NAME: Launching Stream when User is logged out
    DESCRIPTION: User is trying to launch stream in logged out state.
    DESCRIPTION: Applies to <Race> events.
    PRECONDITIONS: 1. SiteServer event should be configured to support RUK/Perform streaming (**'typeFlagCodes'**='RVA , ... ' AND **'drilldownTagNames'**='EVFLAG_RVA' flags should be set)
    PRECONDITIONS: 2. User is logged out
    PRECONDITIONS: 3. The event should have the following attributes:
    PRECONDITIONS: isStarted = "true", but stream has not run for more than 1 minute after the 'start time'
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_race_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> event which satisfies Preconditions
        EXPECTED: * Desktop:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050952) (Coral) / 'Watch' ![](index.php?/attachments/get/3050953) (Ladbrokes) button is shown below the event name line
        EXPECTED: * Mobile/Tablet:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050954) (Coral) / 'Watch' ![](index.php?/attachments/get/3050955) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_002_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: * No request is sent to OptIn MS
        EXPECTED: * [ **Coral** desktop / **Ladbrokes** desktop]: Message is displayed: "In order to watch this stream, you must be logged in."
        EXPECTED: * [ **Ladbrokes** and **Coral** tablet/mobile]: Pop up opens with message "In order to watch this stream, you must be logged in."
        EXPECTED: * User is not able to watch the stream
        """
        pass

    def test_003_log_in_to_the_apptapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: Log in to the app.
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: * Stream is launched
        EXPECTED: * Request to OptIn MS is sent (see preconditions) to indetify stream provider
        EXPECTED: * **listingUrl** attribute is received from OptIn MS to consume streaming
        EXPECTED: * The next provider info is received from Optin MS:
        EXPECTED: {
        EXPECTED: priorityProviderCode: "PERFORM"
        EXPECTED: priorityProviderName: "Perform"
        EXPECTED: }
        """
        pass
