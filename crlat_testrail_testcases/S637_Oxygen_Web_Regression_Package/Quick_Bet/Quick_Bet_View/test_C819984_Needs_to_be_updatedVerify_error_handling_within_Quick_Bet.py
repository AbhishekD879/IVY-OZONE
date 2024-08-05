import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.quick_bet
@vtest
class Test_C819984_Needs_to_be_updatedVerify_error_handling_within_Quick_Bet(Common):
    """
    TR_ID: C819984
    NAME: [Needs to be updated]Verify error handling within Quick Bet
    DESCRIPTION: This test case verifies error handling within Quick Bet
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User is logged out
    PRECONDITIONS: * [How to trigger error from SS][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+simulate+the+situation+when+Site+Serve+is+down
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_one_sportrace_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: * Selected price/odds are highlighted in green
        EXPECTED: * Betslip counter does NOT increase by 1
        """
        pass

    def test_003_trigger_situation_when_ss_is_down_or_invalid_outcome_id_is_sent_to_remote_betslip_microservice(self):
        """
        DESCRIPTION: Trigger situation when SS is down or invalid outcome ID is sent to Remote Betslip microservice
        EXPECTED: The next error is received in response of 30001 request in WS:
        EXPECTED: ["31002",{"data":{"error":{"code":"EVENT_NOT_FOUND","description":"Error reading outcome data. Data not found. OutcomeIds - [outcome_id]"}}}]
        """
        pass

    def test_004_verify_quick_bet(self):
        """
        DESCRIPTION: Verify Quick Bet
        EXPECTED: The next information is displayed in Quick Bet:
        EXPECTED: * 'Server is unavailable at the moment, please try again later. If problem persists, contact our Customer Service Department'
        EXPECTED: where 'Customer Service Department' part is a hyperlink
        EXPECTED: * 'Reload' button
        EXPECTED: * 'ADD TO BETSLIP' and 'PLACE BET' buttons are displayed below message
        EXPECTED: * 'PLACE BET' button is disabled
        """
        pass

    def test_005_verify_customer_service_department_hyperlink(self):
        """
        DESCRIPTION: Verify 'Customer Service Department' hyperlink
        EXPECTED: User is navigated to 'Contact Us' page within Oxygen app after tapping hyperlink
        """
        pass

    def test_006_verify_reload_button(self):
        """
        DESCRIPTION: Verify 'Reload' button
        EXPECTED: Quick bet is reloaded after tapping 'Reload' button
        """
        pass

    def test_007_trigger_situation_when_connection_with_remote_betslip_microservice_is_expired_or_invalid_session_id_is_set_up(self):
        """
        DESCRIPTION: Trigger situation when connection with Remote Betslip microservice is expired or invalid session id is set up
        EXPECTED: The next error is received in response of 30001 request in WS:
        EXPECTED: ["ERROR",{"code":2,"message":"Session not found"}]
        """
        pass

    def test_008_repeat_steps_4_6(self):
        """
        DESCRIPTION: Repeat steps #4-6
        EXPECTED: 
        """
        pass

    def test_009_log_in_and_repeat_steps_2_8(self):
        """
        DESCRIPTION: Log in and repeat steps #2-8
        EXPECTED: 
        """
        pass
