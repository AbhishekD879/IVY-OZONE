import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C10959708_TO_BE_EDITEDVerify_Expired_Overask_Bets_NOT_displaying_on_Settled_Bets_tab(Common):
    """
    TR_ID: C10959708
    NAME: [TO BE EDITED]Verify Expired Overask Bets NOT displaying on 'Settled Bets' tab
    DESCRIPTION: This test case verifies that Expired Overask Bets with 'status:X' and 'asyncStatus:T' are NOT displayed on 'Settled Bets' tab
    PRECONDITIONS: * How to disable/enable Overask functionality for User or Event Type: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: * How to accept/decline/make an Offer with Overask functionality: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    PRECONDITIONS: * The same value in ‘MaxBet’ should be set on event/market/selection levels for event under test in TI
    PRECONDITIONS: * Kibana credentials: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Symphony+Infrastructure+creds
    PRECONDITIONS: In Kibana:
    PRECONDITIONS: 1) select respective bpp e.g. bpp-dev0
    PRECONDITIONS: 2) filter by username and receipt id (bet receipt ID could be taken from 'readbet' response)
    PRECONDITIONS: 3) check 'Account History' log
    PRECONDITIONS: ![](index.php?/attachments/get/29408)
    PRECONDITIONS: Steps:
    PRECONDITIONS: 1. Log in as user with enabled Overask
    PRECONDITIONS: 2. Add selection to betslip and open it
    PRECONDITIONS: 3. Enter any stake amount that exceeds maximum allowed bet limit
    PRECONDITIONS: 4. Tap 'Bet now' > Overask should be triggered
    """
    keep_browser_open = True

    def test_001_wait_till_request_expires_without_traders_actions(self):
        """
        DESCRIPTION: Wait till request expires without Trader's actions
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_my_bets__settled_bets_tabormy_account__bet_history__settled_bets_tab(self):
        """
        DESCRIPTION: Navigate to 'My bets' > 'Settled bets' tab
        DESCRIPTION: OR
        DESCRIPTION: 'My account' > 'Bet history' > 'Settled bets' tab
        EXPECTED: Expired overask bet is NOT displayed
        """
        pass

    def test_003_navigate_to_kibana__check_status_and_asyncstat_for_expired_overask_bet(self):
        """
        DESCRIPTION: Navigate to Kibana > check 'status' and 'asyncStat' for expired overask bet
        EXPECTED: Expired overask bet has the following data:
        EXPECTED: * 'status:X'
        EXPECTED: * 'asyncStatus:T'
        EXPECTED: ![](index.php?/attachments/get/29409)
        """
        pass
