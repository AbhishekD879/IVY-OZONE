import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.build_your_bet
@vtest
class Test_C2461990_Banach_BYB_5_A_Side_Verify_bet_placement_error_when_event_goes_Live(Common):
    """
    TR_ID: C2461990
    NAME: Banach. BYB/5-A-Side. Verify bet placement error when event goes Live
    DESCRIPTION: Test case verifies error during Banach(BYB/5-A-Side) bet placement if event has started when user was placing bet
    DESCRIPTION: Cannot automate this test as assistance from Banach to make event live on their side
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Check the following WS for Adding selection to Quick bet and placing bet:
    PRECONDITIONS: wss://remotebetslip-dev1.coralsports.dev.cloud.ladbrokescoral.com/quickbet/?EIO=3&transport=websocket
    PRECONDITIONS: Pre-conditions:
    PRECONDITIONS: 1. Load EDP with BYB tab opened
    PRECONDITIONS: 2. Add any selections to quick bet
    PRECONDITIONS: 3. Following will need to be done after Place bet is clicked and before bet is placed:
    PRECONDITIONS: - Make event live in TI tool
    PRECONDITIONS: - Contact Banach to get assistance to make event live on their side (OR intercept response from server and change it to error response after placing bet)
    PRECONDITIONS: QB response with code 51102 and error message "EVENT_STARTED":
    PRECONDITIONS: 42["51102",{"data":{"error":{"code":"ERROR","description":"some message","subErrorCode":"EVENT_STARTED"}}}]
    """
    keep_browser_open = True

    def test_001_clicktap_place_bet_on_quick_bet(self):
        """
        DESCRIPTION: Click/tap 'Place bet' on quick bet
        EXPECTED: - In WS client sends message with code 50001 and receives message from quick bet with code 51102 subErrorCode: "EVENT_STARTED";
        EXPECTED: - UI error message **Event has started, please see Main Markets tab for all available bets** appears.
        EXPECTED: ![](index.php?/attachments/get/118215880)
        """
        pass

    def test_002_close_quickbet(self):
        """
        DESCRIPTION: Close Quickbet
        EXPECTED: - User is redirected to All Markets tab
        EXPECTED: - 5-A-Side/BYB tabs are not shown on EDP
        """
        pass
