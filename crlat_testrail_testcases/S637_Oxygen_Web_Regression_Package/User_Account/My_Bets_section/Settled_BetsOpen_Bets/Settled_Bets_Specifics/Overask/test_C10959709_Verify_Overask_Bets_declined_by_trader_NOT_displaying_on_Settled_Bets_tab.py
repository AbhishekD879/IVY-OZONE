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
class Test_C10959709_Verify_Overask_Bets_declined_by_trader_NOT_displaying_on_Settled_Bets_tab(Common):
    """
    TR_ID: C10959709
    NAME: Verify Overask Bets, declined by trader, NOT displaying on 'Settled Bets' tab
    DESCRIPTION: This test case verifies that Overask Bets, declined by trader, are NOT displayed on 'Settled Bets' tab
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

    def test_001_trigger_rejecting_the_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger rejecting the bet by a trader in OpenBet system
        EXPECTED: The bet is rejected
        """
        pass

    def test_002_navigate_to_my_bets__settled_bets_tabormy_account__bet_history__settled_bets_tab(self):
        """
        DESCRIPTION: Navigate to 'My bets' > 'Settled bets' tab
        DESCRIPTION: OR
        DESCRIPTION: 'My account' > 'Bet history' > 'Settled bets' tab
        EXPECTED: Overask bet, declined by trader, is NOT displayed
        """
        pass

    def test_003_navigate_to_kibana__check_status_and_asyncstatus_for_declined_overask_bet(self):
        """
        DESCRIPTION: Navigate to Kibana > check 'status' and 'asyncStatus' for declined overask bet
        EXPECTED: Declined by trader overask bet has the following data:
        EXPECTED: * 'status:X'
        EXPECTED: * 'asyncStatus:D'
        EXPECTED: ![](index.php?/attachments/get/29411)
        """
        pass
