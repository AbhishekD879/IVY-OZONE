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
class Test_C12834306_Verify_Exacta_bet_is_displayed_on_Settled_Bets_tab(Common):
    """
    TR_ID: C12834306
    NAME: Verify Exacta bet is displayed on Settled Bets tab
    DESCRIPTION: This test case verifies the displayed contents of an Exacta tote bet on the Settled Bets tab
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed tote Exacta Bet(s) on UK Tote events
    PRECONDITIONS: User has placed tote Exacta Bet(s) on UK Tote events and the bet is already settled
    """
    keep_browser_open = True

    def test_001_navigate_to_settled_bets_tabtap_on_the_pools_sub_section(self):
        """
        DESCRIPTION: Navigate to Settled Bets tab
        DESCRIPTION: Tap on the Pools sub-section
        EXPECTED: Exacta tote bet information corresponds to settled bet:
        EXPECTED: *  Selection Name(s) and places
        EXPECTED: *  "Tote Exacta Pool" text
        EXPECTED: *  Race number (e.g. Race 3)
        EXPECTED: *  Race Name (e.g 15:25 Wincanton (WI))
        EXPECTED: *  Date of bet placement in a format
        EXPECTED: -Coral - MM/DD/YYYY (e.g. 10/19/2018)
        EXPECTED: -Ladbrokes - HH:MM - Date Month (e.g. 14:40 - 09 Aug)
        EXPECTED: *  Bet Receipt id (e.g. P/0156602/0000117)
        EXPECTED: *  Stake value (e.g. £2.00)
        EXPECTED: *  Estimated returns value(exact value in case bet is settled as Won , Lose or Void)
        """
        pass
