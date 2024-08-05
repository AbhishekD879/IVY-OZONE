import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C2554304_Verify_Placepot_bet_is_displayed_on_Open_Bets_tab(Common):
    """
    TR_ID: C2554304
    NAME: Verify Placepot bet is displayed on Open Bets tab
    DESCRIPTION: Format of date, 'Estimated Returns' need to be changed
    DESCRIPTION: This test case verifies the displayed contents of a Placepot tote bet in the Settled Bets/Open Bets
    DESCRIPTION: AUTOTEST: [C2604131]
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed tote Placepot Bet(s) on UK Tote events
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tabtap_on_the_pools_sub_section(self):
        """
        DESCRIPTION: Navigate to Open Bets tab
        DESCRIPTION: Tap on the Pools sub-section
        EXPECTED: Placepot tote bet information corresponds to placed bet:
        EXPECTED: * Placepot title
        EXPECTED: * Leg number with Time and Name of the meeting
        EXPECTED: * Selection Name/s for each Leg
        EXPECTED: * Date of bet placement in a format MM/DD/YYYY (e.g. 10/19/2018)
        EXPECTED: * Bet Receipt id (e.g. P/0156602/0000117)
        EXPECTED: * Stake value (e.g. £2.00)
        EXPECTED: * Estimated returns value is N/A
        """
        pass
