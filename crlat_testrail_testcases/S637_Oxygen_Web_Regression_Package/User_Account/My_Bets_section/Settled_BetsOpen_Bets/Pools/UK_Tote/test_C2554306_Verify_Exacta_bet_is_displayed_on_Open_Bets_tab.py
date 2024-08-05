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
class Test_C2554306_Verify_Exacta_bet_is_displayed_on_Open_Bets_tab(Common):
    """
    TR_ID: C2554306
    NAME: Verify Exacta bet is displayed on Open Bets tab
    DESCRIPTION: Format of date, 'Estimated Returns' need to be changed
    DESCRIPTION: This test case verifies the displayed contents of an Exacta tote bet in the Open Bets
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed tote Exacta Bet(s) on UK Tote events
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tabtap_on_the_pools_sub_section(self):
        """
        DESCRIPTION: Navigate to Open Bets tab
        DESCRIPTION: Tap on the Pools sub-section
        EXPECTED: Exacta tote bet information corresponds to placed bet:
        EXPECTED: *  Selection Name(s) and places
        EXPECTED: *  "Tote Exacta Pool" text
        EXPECTED: *  Race number (e.g. Race 3)
        EXPECTED: *  Race Name (e.g 15:25 Wincanton (WI))
        EXPECTED: *  Date of bet placement in a format MM/DD/YYYY (e.g. 10/19/2018)
        EXPECTED: *  Bet Receipt id (e.g. P/0156602/0000117)
        EXPECTED: *  Stake value (e.g. £2.00)
        EXPECTED: *  Estimated returns value is N/A (exact value in case bet is settled as Won)
        """
        pass
