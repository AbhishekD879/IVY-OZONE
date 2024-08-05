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
class Test_C57732035_Verify_the_application_performance_on_Slow_3G(Common):
    """
    TR_ID: C57732035
    NAME: Verify the application performance on Slow 3G
    DESCRIPTION: This test case verifies application performance on Slow 3G
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on Homepage or Football landing page
    """
    keep_browser_open = True

    def test_001___turn_on_slow_3g_using_the_browser_device_emulator__turn_on_edge_on_the_real_device(self):
        """
        DESCRIPTION: - Turn ON Slow 3G using the browser device emulator
        DESCRIPTION: - Turn ON 'EDGE' on the real device
        EXPECTED: Configuration applied successfully
        """
        pass

    def test_002_check_application_performance_using_a_slow_internet_connection(self):
        """
        DESCRIPTION: Check application performance using a slow internet connection
        EXPECTED: - All application pages and elements should be displayed correctly
        EXPECTED: - All data should be correctly retrieved and displayed
        EXPECTED: - Any error should not appear during using a slow connection
        """
        pass
