import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C38219423_Verify_blocking_a_request_to_BPP_when_2_same_requests_are_sent_at_the_same_time(Common):
    """
    TR_ID: C38219423
    NAME: Verify blocking a request to BPP when 2 same requests are sent at the same time
    DESCRIPTION: This test case verifies blocking of duplicate requests to BPP made at the same time
    DESCRIPTION: **NOTE:** Valid for Coral version >=101.1 and Ladbrokes version >=100.3
    PRECONDITIONS: - User is logged in to application with positive balance
    PRECONDITIONS: - devTools is opened in browser
    """
    keep_browser_open = True

    def test_001_add_selection_to_betslip_and_place_bet(self):
        """
        DESCRIPTION: Add selection to Betslip and place bet.
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet receipt is shown to user
        EXPECTED: * 'placeBet' request is present in devTools
        """
        pass

    def test_002_copy_placebet_response_as_curlindexphpattachmentsget59204749(self):
        """
        DESCRIPTION: Copy placeBet response as cURL![](index.php?/attachments/get/59204749)
        EXPECTED: 
        """
        pass

    def test_003_paste_this_curl_into_two_instances_of_terminal_on_same_or_different_computers(self):
        """
        DESCRIPTION: Paste this cURL into two instances of terminal (on same or different computers)
        EXPECTED: cURL data is displayed in terminals and ready to be triggered
        EXPECTED: **Example:**
        EXPECTED: ![](index.php?/attachments/get/59204750)
        """
        pass

    def test_004_trigger_response_execution_in_terminal_for_both_instances_at_the_same_time_and_verify_result_of_this_execution(self):
        """
        DESCRIPTION: Trigger response execution in terminal for both instances at the same time and verify result of this execution
        EXPECTED: * {"betError":[{"subErrorCode":"DUPLICATED_BET","code":"IGNORE_BET","betRef":[{"documentId":"1"}
        EXPECTED: is displayed in one of the terminal instances
        EXPECTED: * Bet placement info is displayed in another instance
        EXPECTED: **Example:**
        EXPECTED: ![](index.php?/attachments/get/59204751)
        """
        pass

    def test_005_verify_bets_displaying_in_open_bets_section_in_application(self):
        """
        DESCRIPTION: Verify bets displaying in Open Bets section in application
        EXPECTED: Only one of placed via terminal bets is displayed in application
        """
        pass
