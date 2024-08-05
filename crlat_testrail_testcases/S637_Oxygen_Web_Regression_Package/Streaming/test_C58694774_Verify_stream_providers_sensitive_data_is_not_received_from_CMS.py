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
class Test_C58694774_Verify_stream_providers_sensitive_data_is_not_received_from_CMS(Common):
    """
    TR_ID: C58694774
    NAME: Verify stream providers sensitive data is not received from CMS
    DESCRIPTION: This test case verifies if stream providers sensitive data is not received from CMS system config
    PRECONDITIONS: List of CMS Endpoints:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
    """
    keep_browser_open = True

    def test_001_in_application_find_initial_data_response_from_cms_in_devtools_mobile_for_mobile_and_tablets_desktop_for_desktop_view(self):
        """
        DESCRIPTION: In application, find initial data response from CMS in devtools
        DESCRIPTION: ( **mobile** for mobile and tablets, **desktop** for desktop view)
        EXPECTED: * Initial data response is received
        EXPECTED: * **systemConfiguration** part of response does not include streaming providers data ( **AtTheRaces**, **IMGStreaming**; **performGroup** only includes csbIframeEnabled and csbIframeSportIds parameters)
        """
        pass

    def test_002__open_cms_related_to_environment_under_the_test_check_system_configuration_parameters(self):
        """
        DESCRIPTION: * Open CMS related to environment under the test
        DESCRIPTION: * Check System Configuration parameters
        EXPECTED: System Configuration does not include streaming providers parameters ( **AtTheRaces**, **IMGStreaming**; **performGroup** only includes csbIframeEnabled and csbIframeSportIds parameters))
        """
        pass
