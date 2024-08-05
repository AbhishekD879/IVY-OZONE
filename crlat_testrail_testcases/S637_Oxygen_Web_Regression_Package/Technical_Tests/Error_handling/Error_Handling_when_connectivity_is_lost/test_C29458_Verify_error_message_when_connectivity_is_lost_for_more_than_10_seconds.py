import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C29458_Verify_error_message_when_connectivity_is_lost_for_more_than_10_seconds(Common):
    """
    TR_ID: C29458
    NAME: Verify error message when connectivity is lost for more than 10 seconds
    DESCRIPTION: This test case verifies error message when connectivity is lost for more than 10 seconds
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-7647 Display Message To Users When Connectivity Is Lost
    DESCRIPTION: *   BMA-7698 As a PO I want the app to retry to connect to a failed HTTP or Websocket request once before displaying an information message.
    DESCRIPTION: *   BMA-7891 Connection issue during under maintenance
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_any_pagetab_within_the_application(self):
        """
        DESCRIPTION: Go to any page/tab within the application
        EXPECTED: User is redirected to the selected area
        """
        pass

    def test_003_turn_off_the_internet_connection(self):
        """
        DESCRIPTION: Turn off the Internet connection
        EXPECTED: *   Connection to the internet is lost
        EXPECTED: *   Application is opened
        """
        pass

    def test_004_wait_approx_10_seconds_after_connection_request_failed_there_is_10_seconds_delay_beforeretry__if_second_request_failed___message_is_shown(self):
        """
        DESCRIPTION: Wait approx. 10 seconds (after connection request failed there is 10 seconds delay before **retry**-> if second request failed - message is shown)
        EXPECTED: Message about lost connection is shown with option to retry
        """
        pass

    def test_005_verify_reflection_on_navigating_to_other_pagetab_where_https_requests_are_expected(self):
        """
        DESCRIPTION: Verify reflection on navigating to other page/tab (where http(s) requests are expected)
        EXPECTED: *   User is navigated to selected page/tab
        EXPECTED: *   Message about lost connection is shown **with delay in approx. 10 seconds**(after connection request failed there is 10 seconds delay before **retry**-> if second request failed - message is shown)
        """
        pass

    def test_006_tap_retry_button_within_message_about_lost_connection(self):
        """
        DESCRIPTION: Tap 'Retry' button within message about lost connection
        EXPECTED: Default browser handling is performed after app reload when connection is absent
        """
        pass

    def test_007_repeat_steps_1_4(self):
        """
        DESCRIPTION: Repeat steps 1-4
        EXPECTED: 
        """
        pass

    def test_008_turn_on_connection_to_the_internet(self):
        """
        DESCRIPTION: Turn on connection to the internet
        EXPECTED: Connection is active
        """
        pass

    def test_009_tap_on_retry_button_within_message_about_lost_connection(self):
        """
        DESCRIPTION: Tap on 'Retry' button within message about lost connection
        EXPECTED: *   Application is fully reloaded
        EXPECTED: *   Homepage is shown with all content if connection is active
        """
        pass
