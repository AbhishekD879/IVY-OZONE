import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C57732122_Verify_error_handling_of_submit_button(Common):
    """
    TR_ID: C57732122
    NAME: Verify error handling of submit button
    DESCRIPTION: This test case verifies error handling of submit button
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: for Qubit version (deprecated) https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: for Oxygen version: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. User Do not have prediction yet
    """
    keep_browser_open = True

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: 'Submit' button **displayed**
        """
        pass

    def test_002_tap_on_submit_button_with_network_delays(self):
        """
        DESCRIPTION: Tap on 'Submit' button with network delays
        EXPECTED: 'Submit' button changes to **'Processing'**
        """
        pass

    def test_003_tap_on_submit_button_with_fail_for_any_reason_or_error_from_msturn_off_wi_fi_replace_ip_to_be_in_hosts_file(self):
        """
        DESCRIPTION: Tap on 'Submit' button with Fail for any reason or error from MS
        DESCRIPTION: (Turn Off Wi-Fi, Replace IP to BE in hosts file)
        EXPECTED: - 'Submit' button changes to **'Please try again'**
        EXPECTED: - User should have ability to Tap on 'Submit' button once again and make a prediction
        """
        pass
