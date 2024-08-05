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
class Test_C29483_Tracking_of_clientUserAgent_value_in_data_base_on_OpenBet_side(Common):
    """
    TR_ID: C29483
    NAME: Tracking of clientUserAgent value in data base on OpenBet side
    DESCRIPTION: This test case verifies tracking of **clientUserAgent **values in data base on **OpenBet **side.
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   BMA-8963 Tracking bet placement for Native
    DESCRIPTION: *   BMA-9212 Tracking bet placement for Web HTML5
    PRECONDITIONS: *   Use is logged in
    PRECONDITIONS: *   User is able to place a bet (user is not suspended and has a positive balance)
    PRECONDITIONS: *   List of all supported devices should be covered
    PRECONDITIONS: *   Guide "[How to debug emulator, real iOS and Android devices][1]"
    PRECONDITIONS: *   UAT assistance is needed
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/MOB/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is added
        """
        pass

    def test_002_open_betslip__my_bets_page(self):
        """
        DESCRIPTION: Open 'Betslip / My Bets' page
        EXPECTED: 'Bet Slip' tab is opened
        EXPECTED: **Note**: It's recommended to clear history in Developer tools before next step. It would be easier to find request needed.
        """
        pass

    def test_003_enter_stake_value_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter "Stake" value and tap 'Bet Now' button
        EXPECTED: The Bet is successfully placed
        """
        pass

    def test_004_send_to_uat_team_the_following_bet_info___username___bet_time___bet_receipt_number___clientuseragent_value(self):
        """
        DESCRIPTION: Send to UAT team the following bet info:
        DESCRIPTION: *   Username
        DESCRIPTION: *   Bet time
        DESCRIPTION: *   Bet Receipt number
        DESCRIPTION: *   **clientUserAgent **value
        EXPECTED: 
        """
        pass

    def test_005_ask_to_send_you_info_related_to_verified_bet_from_ob_system(self):
        """
        DESCRIPTION: Ask to send you info related to verified bet from OB system
        EXPECTED: Received data contains:
        EXPECTED: *   Receipt
        EXPECTED: *   client_name
        """
        pass

    def test_006_verify_datacorrectness(self):
        """
        DESCRIPTION: Verify data correctness
        EXPECTED: *   OB 'Receipt' value matches with sent on step №5 Bet Receipt number
        EXPECTED: *   OB '**client_name**' value matches with sent on step №5 **clientUserAgent **value
        """
        pass
