import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870418__Verify_Display_of_betslip_header_it_should_have____Betslip____My_Bets__Cash_Out______________Open_Bets______________Settled_Bets(Common):
    """
    TR_ID: C44870418
    NAME: "-Verify Display of betslip header,  it should have        Betslip        My Bets --> Cash Out                           Open Bets                           Settled Bets"
    DESCRIPTION: 
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_verify_betslip_header_should_havebetslip________my_bets____cash_out___________________________open_bets___________________________settled_bets(self):
        """
        DESCRIPTION: Verify Betslip header should have
        DESCRIPTION: Betslip        My Bets --> Cash Out                           Open Bets                           Settled Bets"
        EXPECTED: User Sees Following Bet slip headers in Tab.
        EXPECTED: Betslip     My Bets (Sub Headers:  Cash Out, Open Bets, Settled Bets)
        """
        pass
