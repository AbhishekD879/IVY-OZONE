import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C16268995_Vanilla_Verify_opt_in_button_during_multiple_log_in(Common):
    """
    TR_ID: C16268995
    NAME: [Vanilla] Verify opt in button during multiple log in
    DESCRIPTION: This test case verifies opt in button during multiple log in
    PRECONDITIONS: User should be logged in the same account from multiple devices
    """
    keep_browser_open = True

    def test_001_make_multiple_login_the_same_account_which_is_not_already_opted_in(self):
        """
        DESCRIPTION: Make multiple login the same account which is not already opted in
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_promotion_with_opt_in_button_from_device_1(self):
        """
        DESCRIPTION: Navigate to Promotion with Opt In button from Device 1
        EXPECTED: - Opt In button is enabled
        EXPECTED: - Request ID with username and token is sent in the devtool-> Network
        EXPECTED: - 'fired': 'false' in sent in the Request ID response
        """
        pass

    def test_003_tap_on_opt_in_button_from_device_1(self):
        """
        DESCRIPTION: Tap on Opt In button from Device 1
        EXPECTED: Opt In option was successful
        """
        pass

    def test_004_navigate_to_the_same_promotion_with_opt_in_button_from_device_2(self):
        """
        DESCRIPTION: Navigate to the same Promotion with Opt In button from Device 2
        EXPECTED: - Already opted in message is displayed on Opt In button
        EXPECTED: - Request ID with username and token is sent in the devtool-> Network
        EXPECTED: - 'fired': 'true' in sent in the Request ID response
        """
        pass

    def test_005_make_multiple_login_the_same_account_which_is_not_already_opted_in(self):
        """
        DESCRIPTION: Make multiple login the same account which is not already opted in
        EXPECTED: User is logged out
        """
        pass

    def test_006_navigate_to_promotion_with_opt_in_button_on_both_devices(self):
        """
        DESCRIPTION: Navigate to Promotion with Opt In button on both devices
        EXPECTED: - Opt In button is enabled
        EXPECTED: - Request ID with username and token is sent in the devtool-> Network
        EXPECTED: - 'fired': 'false' in sent in the Request ID response
        """
        pass

    def test_007_tap_on_opt_in_button_on_one_of_devices(self):
        """
        DESCRIPTION: Tap on Opt In button on one of devices
        EXPECTED: - Opt In option was successful
        EXPECTED: - Success message appears
        """
        pass

    def test_008_verify_opt_in_button_on_device_2(self):
        """
        DESCRIPTION: Verify Opt In button on Device 2
        EXPECTED: Opt In button is enabled
        """
        pass

    def test_009_refresh_the_page_within_browser_refresh_button(self):
        """
        DESCRIPTION: Refresh the page within browser refresh button
        EXPECTED: - Already opted in message is displayed on Opt In button
        EXPECTED: - Request ID with username and token is sent in the devtool-> Network
        EXPECTED: - 'fired': 'true' in sent in the Request ID response
        """
        pass
