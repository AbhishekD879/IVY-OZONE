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
class Test_C10959707_Verify_Overask_Bets_with_status_Pending_NOT_displaying_on_Settled_Bets_tab(Common):
    """
    TR_ID: C10959707
    NAME: Verify Overask Bets with status 'Pending' NOT displaying on 'Settled Bets' tab
    DESCRIPTION: This test case verifies that Overask Bets with status 'Pending' are NOT displayed on 'Settled Bets' tab
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

    def test_001_while_review_is_pending_navigate_tomy_bets__settled_bets_tabormy_account__bet_history__settled_bets_tab(self):
        """
        DESCRIPTION: While review is pending navigate to:
        DESCRIPTION: 'My bets' > 'Settled bets' tab
        DESCRIPTION: OR
        DESCRIPTION: 'My account' > 'Bet history' > 'Settled bets' tab
        EXPECTED: Pending overask bet is NOT displayed
        """
        pass

    def test_002_navigate_to_kibana__check_status_for_pending_overask_bet(self):
        """
        DESCRIPTION: Navigate to Kibana > check 'status' for pending overask bet
        EXPECTED: Pending overask bet has the following data:
        EXPECTED: * status:P
        EXPECTED: ![](index.php?/attachments/get/29413)
        """
        pass
