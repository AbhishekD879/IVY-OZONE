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
class Test_C883825_To_Be_Archived_Launching_stream_for_an_event_with_several_mapped_streaming_providers(Common):
    """
    TR_ID: C883825
    NAME: (To Be Archived) Launching stream for an event with several mapped streaming providers
    DESCRIPTION: This test case verifies successfully launching a streaming when several streaming providers are mapped to the same event
    DESCRIPTION: ***Jira ticket:***
    DESCRIPTION: BMA-22601: Integrate with Igame media
    PRECONDITIONS: 1. SiteServer event should be configured to support Perform, IMG, RUK, RPGTV streaming (**'typeFlagCodes'**='PVA , IVA, RVA, RPG... ' AND **'drilldownTagNames'**='EVFLAG_PVM, EVFLAG_IVM, EVFLAG_AVA, EVFLAG_RVA, EVFLAG_RPM' flags should be set) and should be mapped to the same <Sport> event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: isStarted = "true"
    PRECONDITIONS: isMarketBetInRun = "true"
    PRECONDITIONS: 3. - For Perform: User has positive balance
    PRECONDITIONS: - For ATR, RUK, RPGTV: User placed a minimum sum of £1 on one or many Selections within tested event
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User is logged in successfully
        """
        pass

    def test_003_open_event_details_page_of_any_sportrace_for_the_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Sport>/<Race> for the event which satisfies Preconditions
        EXPECTED: 'Video Stream' button is displayed
        """
        pass

    def test_004_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: Stream is launched
        """
        pass

    def test_005_verify_eventid_response_in_network(self):
        """
        DESCRIPTION: Verify <eventID> response in Network
        EXPECTED: - <eventID> response is available
        EXPECTED: - List of mapped providers are available in <eventID> response
        EXPECTED: - Providers are prioritized
        """
        pass

    def test_006_verify_topprioritizedprovider_response_in_network(self):
        """
        DESCRIPTION: Verify <TopPrioritizedProvider> response in Network
        EXPECTED: - <TopPrioritizedProvider> response is available
        EXPECTED: - Video iframe is received from <TopPrioritizedProvider>
        """
        pass
