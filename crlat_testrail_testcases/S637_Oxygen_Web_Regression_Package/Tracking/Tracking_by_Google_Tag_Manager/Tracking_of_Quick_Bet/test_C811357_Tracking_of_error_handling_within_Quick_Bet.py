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
class Test_C811357_Tracking_of_error_handling_within_Quick_Bet(Common):
    """
    TR_ID: C811357
    NAME: Tracking of error handling within Quick Bet
    DESCRIPTION: This test case verifies tracking of error handling within Quick Bet
    PRECONDITIONS: * Test case should be run on Mobile Only
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * To view response open Dev tools -> Network -> WS -> choose the last request
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * User is logged out
    PRECONDITIONS: * [How to trigger error from SS][1]
    PRECONDITIONS: * Attribute <<CUSTOMER BUILT>> show Yes/No,
    PRECONDITIONS: if bet type = "Build Your Bet shows 'Yes'
    PRECONDITIONS: **New Quickbet tracking parameters:** https://confluence.egalacoral.com/pages/viewpage.action?pageId=91470520
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+simulate+the+situation+when+Site+Serve+is+down
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sportrace_selection(self):
        """
        DESCRIPTION: Tap <Sport>/<Race> selection
        EXPECTED: Selected price/odds are highlighted in green
        """
        pass

    def test_003_trigger_situation_when_ss_is_down_or_invalid_outcome_id_is_sent_to_remote_betslip_microservice(self):
        """
        DESCRIPTION: Trigger situation when SS is down or invalid outcome ID is sent to Remote Betslip microservice
        EXPECTED: * Quick Bet section is displayed with next error message:
        EXPECTED: 'Server is unavailable at the moment, please try again later. If problem persists, contact our Customer Service Department'
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
        EXPECTED: 'eventAction' : 'add to quickbet',
        EXPECTED: 'eventLabel' : 'failure',
        EXPECTED: 'errorMessage' : '<< ERROR MESSAGE >>',
        EXPECTED: 'errorCode' : '<< ERROR CODE >>'
        EXPECTED: 'location' : '<< LOCATION >>',
        EXPECTED: 'customerBuilt' : '<< CUSTOMER BUILT >>'
        EXPECTED: });
        """
        pass

    def test_005_verify_errormessage_parameter(self):
        """
        DESCRIPTION: Verify **'errorMessage'** parameter
        EXPECTED: * **'errorMessage'** parameter corresponds to message displayed to user
        """
        pass

    def test_006_verify_errorcode_parameter(self):
        """
        DESCRIPTION: Verify **'errorCode'** parameter
        EXPECTED: * **'errorCode'** parameter corresponds to **error.code** value recieved in response of 30001 request in WS
        """
        pass

    def test_007_trigger_situation_when_connection_with_remote_betslip_microservice_is_expired_or_invalid_session_id_is_set_up_and_repeat_steps_4_6(self):
        """
        DESCRIPTION: Trigger situation when connection with Remote Betslip microservice is expired or invalid session id is set up and repeat steps #4-6
        EXPECTED: 
        """
        pass

    def test_008_log_in_and_repeat_steps_2_7(self):
        """
        DESCRIPTION: Log in and repeat steps #2-7
        EXPECTED: 
        """
        pass
