import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.
@vtest
class Test_C60034678_Verify_Time_Service_MS(Common):
    """
    TR_ID: C60034678
    NAME: Verify Time Service MS
    DESCRIPTION: This test case verifies that time and user IP is sent through new service
    PRECONDITIONS: For phoenix env:
    PRECONDITIONS: https://s6b1xo4ww9.execute-api.eu-west-1.amazonaws.com/v1/session
    """
    keep_browser_open = True

    def test_001_load_url_from_preconditions_and_verify_response(self):
        """
        DESCRIPTION: Load URL from preconditions and verify response
        EXPECTED: - user IP is present
        EXPECTED: - timestamp in UTC - server time
        """
        pass

    def test_002_verify_that_user_ip_is_correct(self):
        """
        DESCRIPTION: Verify that User IP is correct
        EXPECTED: - https://whatismyipaddress.com/ - check your IP address here
        EXPECTED: - compare with Timeservice IP address
        """
        pass

    def test_003_verify_timestamp(self):
        """
        DESCRIPTION: Verify timestamp
        EXPECTED: - https://www.epochconverter.com/ - translate time stamp to human date
        EXPECTED: - compare with the current time
        """
        pass

    def test_004_verify_that_bpp_call_is_removed(self):
        """
        DESCRIPTION: Verify that BPP call is removed
        EXPECTED: - make call https://coral-bpp-dev-phoenix.symphony-solutions.eu/Proxy/v2/user/session/info
        EXPECTED: - 404 status should be in the response code
        """
        pass
