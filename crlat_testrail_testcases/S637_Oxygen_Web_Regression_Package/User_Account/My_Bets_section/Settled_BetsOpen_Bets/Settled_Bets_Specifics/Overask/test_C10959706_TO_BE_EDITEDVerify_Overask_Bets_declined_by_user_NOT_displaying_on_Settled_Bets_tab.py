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
class Test_C10959706_TO_BE_EDITEDVerify_Overask_Bets_declined_by_user_NOT_displaying_on_Settled_Bets_tab(Common):
    """
    TR_ID: C10959706
    NAME: [TO BE EDITED]Verify Overask Bets, declined by user, NOT displaying on 'Settled Bets' tab
    DESCRIPTION: This test case verifies that Overask Bets, declined by user, are NOT displayed on 'Settled Bets' tab
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

    def test_001_in_ti_trigger_offer_with_the_max_bet_by_a_trader(self):
        """
        DESCRIPTION: In TI: Trigger offer with the max bet by a trader
        EXPECTED: Confirmation is sent and received in Oxygen app
        """
        pass

    def test_002_in_application_tap_cancel_button(self):
        """
        DESCRIPTION: In application tap 'Cancel' button
        EXPECTED: Bet is NOT placed
        """
        pass

    def test_003_navigate_to_my_bets__settled_bets_tabormy_account__bet_history__settled_bets_tab(self):
        """
        DESCRIPTION: Navigate to 'My bets' > 'Settled bets' tab
        DESCRIPTION: OR
        DESCRIPTION: 'My account' > 'Bet history' > 'Settled bets' tab
        EXPECTED: Overask bet, declined by user, is NOT displayed
        """
        pass

    def test_004_navigate_to_kibana__check_status_and_asyncstatus_for_declined_overask_bet(self):
        """
        DESCRIPTION: Navigate to Kibana > check 'status' and 'asyncStatus' for declined overask bet
        EXPECTED: Declined by user overask bet has the following data:
        EXPECTED: * 'status:X'
        EXPECTED: * 'asyncStatus:S'
        EXPECTED: ![](index.php?/attachments/get/29412)
        """
        pass
