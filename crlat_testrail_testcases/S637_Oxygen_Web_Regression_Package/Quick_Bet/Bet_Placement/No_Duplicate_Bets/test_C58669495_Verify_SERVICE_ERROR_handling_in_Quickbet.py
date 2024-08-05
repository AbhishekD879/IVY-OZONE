import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C58669495_Verify_SERVICE_ERROR_handling_in_Quickbet(Common):
    """
    TR_ID: C58669495
    NAME: Verify SERVICE_ERROR handling in Quickbet
    DESCRIPTION: This test case verifies SERVICE_ERROR handling within Quickbet
    PRECONDITIONS: - [Burp Suite](https://confluence.egalacoral.com/display/SPI/WebSockets+interception+with+Burp+Suite) (or any other proxy tool with ability to intercept websocket messages) should be installed and running to intercept server-to-client messages
    PRECONDITIONS: OR
    PRECONDITIONS: Dev support is needed to mock remotebetslip response
    PRECONDITIONS: - User is logged in with positive balance
    PRECONDITIONS: - Selection(s) added to Quickbet, stake field is populated
    PRECONDITIONS: - In devtools 'Network' tab WebSockets (wss://remotebetslip) is open
    """
    keep_browser_open = True

    def test_001_mobile__click_on_place_bet_4230011_ws_message_sent__in_burp_suite_intercept_server_to_client_4230013_message_and_paste4231012dataerrorcodeservice_errordescriptionconnection_timeoutindexphpattachmentsget106145986(self):
        """
        DESCRIPTION: *Mobile*
        DESCRIPTION: - Click on Place Bet 42["30011"..] ws message sent
        DESCRIPTION: - In Burp suite intercept server-to-client 42["30013"..] message and paste:
        DESCRIPTION: 42["31012",{"data":{"error":{"code":"SERVICE_ERROR","description":"Connection timeout"}}}]
        DESCRIPTION: ![](index.php?/attachments/get/106145986)
        EXPECTED: - Error displayed: "Sorry, there may have been a problem placing your bet. To confirm if your bet was placed please check your Open bets"
        EXPECTED: - OPEN BETS displayed as LINK
        EXPECTED: ![](index.php?/attachments/get/106145987)
        """
        pass

    def test_002_click_on_open_bets_link_within_error_message(self):
        """
        DESCRIPTION: Click on Open Bets link within error message
        EXPECTED: User is redirected to Open Bets page
        """
        pass

    def test_003_mobile_plus_desktopnavigate_to_event_with_bybbet_builder_banach_market_and_repeat_step_1_using_error_message4251102dataerrorcodeerrordescriptionconnection_timeoutsuberrorcodeservice_error(self):
        """
        DESCRIPTION: *Mobile + Desktop*
        DESCRIPTION: Navigate to event with BYB/Bet Builder (Banach) market and repeat step 1 using error message:
        DESCRIPTION: 42["51102",{"data":{"error":{"code":"ERROR","description":"Connection timeout","subErrorCode":"SERVICE_ERROR"}}}]
        EXPECTED: - Error displayed: "Sorry, there may have been a problem placing your bet. To confirm if your bet was placed please check your Open bets"
        EXPECTED: - OPEN BETS displayed as LINK clicking on which redirects to Open Bets page
        EXPECTED: ![](index.php?/attachments/get/106147528)
        """
        pass

    def test_004_mobile_plus_desktopnavigate_to_event_with_five_a_side_banach_market_and_repeat_step_1_using_error_message4251102dataerrorcodeerrordescriptionconnection_timeoutsuberrorcodeservice_error(self):
        """
        DESCRIPTION: *Mobile + Desktop*
        DESCRIPTION: Navigate to event with Five-A-Side (Banach) market and repeat step 1 using error message:
        DESCRIPTION: 42["51102",{"data":{"error":{"code":"ERROR","description":"Connection timeout","subErrorCode":"SERVICE_ERROR"}}}]
        EXPECTED: - Error displayed: "Sorry, there may have been a problem placing your bet. To confirm if your bet was placed please check your Open bets"
        EXPECTED: - OPEN BETS displayed as LINK clicking on which redirects to Open Bets page
        EXPECTED: ![](index.php?/attachments/get/106147528)
        """
        pass
