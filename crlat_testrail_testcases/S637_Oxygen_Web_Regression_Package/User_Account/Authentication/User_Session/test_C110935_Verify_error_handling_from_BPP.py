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
class Test_C110935_Verify_error_handling_from_BPP(Common):
    """
    TR_ID: C110935
    NAME: Verify error handling from BPP
    DESCRIPTION: This test case verifies that user stays logged in when BPP sends 'UNAUTHORIZED_ACCESS' error and Oxygen FE sends new OpenApi token to BPP
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Open Development tool ->Network ->'All'
    PRECONDITIONS: Note: BPP services that are used in the application:
    PRECONDITIONS: 1. buildComplexLegs
    PRECONDITIONS: 2. buildBet
    PRECONDITIONS: 3. buildBetLogged
    PRECONDITIONS: 4. placeBet
    PRECONDITIONS: 5. cashoutBet
    PRECONDITIONS: 6. readBet
    PRECONDITIONS: 7. offerBet
    PRECONDITIONS: 8. getBetHistory
    PRECONDITIONS: 9. getBetDetail
    PRECONDITIONS: 10. getBetDetails
    PRECONDITIONS: 11. getBetsPlaced
    PRECONDITIONS: 12. freeBetOffer
    PRECONDITIONS: 13. freebetTrigger
    PRECONDITIONS: 14. videoStream
    PRECONDITIONS: 15. accountFreebets
    PRECONDITIONS: 16. privateMarkets
    PRECONDITIONS: 17. netVerify
    PRECONDITIONS: 18. getPriceLadder
    PRECONDITIONS: 19. getPriceModifiers
    """
    keep_browser_open = True

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_selection_to_betslip_and_enter_stake(self):
        """
        DESCRIPTION: Add selection to betslip and enter stake
        EXPECTED: 
        """
        pass

    def test_003__tap_bet_now_trigger_error_unauthorized_access_sending_to_oxygen_developers_help_is_needed_after_betplacement_or_any_other_service_used_check_preconditions(self):
        """
        DESCRIPTION: * Tap 'Bet Now'
        DESCRIPTION: * Trigger error 'UNAUTHORIZED_ACCESS' sending to Oxygen (developers help is needed) after betplacement (or any other service used, check preconditions)
        EXPECTED: * Bet is placed and bet receipt is shown
        EXPECTED: * 3'placebet' requests are present in Development tool
        """
        pass

    def test_004_check_error_and_token_displaying_in_second__placebet_response_highlighted_in_red_in_network_or_any_other_service_used_check_preconditions(self):
        """
        DESCRIPTION: Check error and token displaying in second  'placebet' response (highlighted in red) in Network or any other service used, check preconditions
        EXPECTED: Error is received:
        EXPECTED: error: "Token expired or user does not exist"
        EXPECTED: message: "Service error"
        EXPECTED: status: 'UNAUTHORIZED_ACCESS'
        """
        pass

    def test_005__navigate_to_development_tool__network__ws_framescheck__30001_requests_is_sent(self):
        """
        DESCRIPTION: * Navigate to Development tool ->Network ->WS> Frames
        DESCRIPTION: *Check  30001 requests is sent
        EXPECTED: 30001 request is present
        """
        pass

    def test_006_check_30002_success_response_is_received_with_new_token(self):
        """
        DESCRIPTION: Check 30002 success response is received with new token
        EXPECTED: 30002 success response is received with token value
        """
        pass

    def test_007_open_last_user_request_in_network_and_check_token_in_header_request_payload_section(self):
        """
        DESCRIPTION: Open last 'user' request in Network and check token in header ('Request Payload' section)
        EXPECTED: 'token' value = 'token' value in 30002 response in WS
        """
        pass

    def test_008_navigate_to_application__local_storage_oxygen_url_and_check_two_tokens_in_oxuser(self):
        """
        DESCRIPTION: Navigate to Application ->Local Storage->Oxygen URL and check two tokens in OX.USER
        EXPECTED: 'Session token' and 'BBP token'
        """
        pass

    def test_009_open_last_placebet_response_in_network_or_any_other_service_used_check_preconditions_and_check_token_value_in_header(self):
        """
        DESCRIPTION: Open last 'placebet' response in Network (or any other service used, check preconditions) and check token value in Header
        EXPECTED: 'Token' value = BBP token in step 8
        """
        pass

    def test_010_repeat_steps_2_9_for_any_other_service_from_preconditions(self):
        """
        DESCRIPTION: Repeat steps #2-9 for any other service from preconditions
        EXPECTED: Oxygen FE should send request to Playtech IMS for new token and send it to BPP.
        EXPECTED: User should stay logged in and  able to use BPP services with new token.
        """
        pass
