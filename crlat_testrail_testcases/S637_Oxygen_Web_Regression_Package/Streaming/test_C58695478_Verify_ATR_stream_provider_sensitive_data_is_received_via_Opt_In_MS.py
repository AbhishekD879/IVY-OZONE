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
class Test_C58695478_Verify_ATR_stream_provider_sensitive_data_is_received_via_Opt_In_MS(Common):
    """
    TR_ID: C58695478
    NAME: Verify ATR stream provider sensitive data is received via Opt-In MS
    DESCRIPTION: This test case verifies that AtTheRaces stream provider sensitive data is received via Opt-In MS
    PRECONDITIONS: At least one ATR stream is available within testing environment
    PRECONDITIONS: ATR stream provider data is configured in CMS > Secrets
    PRECONDITIONS: ATR secrets config for TST Coral:
    PRECONDITIONS: ![](index.php?/attachments/get/115428078)
    PRECONDITIONS: ATR secrets config for TST Ladbrokes:
    PRECONDITIONS: ![](index.php?/attachments/get/115428079)
    PRECONDITIONS: How to map streams to existing events:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: To check information about video stream:
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * DevTools should be opened
    PRECONDITIONS: * In Network tab search field **opt** should be entered in order to find requests to Opt-In MS
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_of_the_event_with_mapped_atr_stream(self):
        """
        DESCRIPTION: Navigate to EDP of the event with mapped ATR stream
        EXPECTED: EDP of the event is loaded
        """
        pass

    def test_002_start_the_stream_of_the_event_and_check_requests_to_opt_in_ms(self):
        """
        DESCRIPTION: Start the stream of the event and check requests to Opt-In MS
        EXPECTED: * Request to Opt-In MS is present (request name is equal to event ID)
        EXPECTED: * Device type is displayed as a parameter in the request link (e.g. https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame/10232859?device=XXXXXX )
        EXPECTED: where **device** is **mobile** for mobile or tablet devices and **desktop** for desktop view
        """
        pass

    def test_003_observe_data_within_opt_in_ms_request(self):
        """
        DESCRIPTION: Observe data within Opt-In MS request
        EXPECTED: * Data with sensitive information is present in response from Opt-In under **meta** tag
        EXPECTED: * Data corresponds to values set in CMS
        EXPECTED: * Data for a stream is displayed with data structure:
        EXPECTED: meta: {
        EXPECTED: AtTheRaces: {
        EXPECTED: partnerCode: '',
        EXPECTED: password: '',
        EXPECTED: secret: ''
        EXPECTED: }
        EXPECTED: }
        """
        pass
