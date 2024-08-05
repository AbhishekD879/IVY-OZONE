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
class Test_C29262_Launching_Stream_when_Event_is_not_started(Common):
    """
    TR_ID: C29262
    NAME: Launching Stream when Event is not started
    DESCRIPTION: User is trying to launch stream when it is more than 5 minutes left to its start time.
    DESCRIPTION: Applies to <Race> events
    PRECONDITIONS: 1. SiteServer event should be configured to support RUK/Perform streaming (**'typeFlagCodes'**='RVA , ... ' AND **'drilldownTagNames'**='EVFLAG_RVA' flags should be set) and should be mapped to RUK/Perform stream event
    PRECONDITIONS: 2. More than 5 min left to event start time. The event should not be started
    PRECONDITIONS: 3. This is free to watch for all 'Active' users. (Active user = Logged In user with a positive balance or placed a bet in last 24 Hours).
    PRECONDITIONS: 4. Endpoints of Optin MS:
    PRECONDITIONS: * https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Coral
    PRECONDITIONS: * https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Ladbrokes
    PRECONDITIONS: * https://optin-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - tst2 Coral
    PRECONDITIONS: * https://optin-tst0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - tst2 Ladbrokes
    PRECONDITIONS: * https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - prod Coral
    PRECONDITIONS: * https://optin-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - prod Ladbrokes
    PRECONDITIONS: * https://optin-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - beta Coral
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

    def test_002_all_devicestapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch'/'Live Stream' button
        EXPECTED: Perform Iframe is loaded:
        EXPECTED: ![](index.php?/attachments/get/121101486)
        EXPECTED: Request to OptIn MS is sent (see preconditions) to identify stream provider
        EXPECTED: The next provider info is received from Optin MS:
        EXPECTED: {
        EXPECTED: priorityProviderCode: "PERFORM"
        EXPECTED: priorityProviderName: "Perform"
        EXPECTED: }
        """
        pass
