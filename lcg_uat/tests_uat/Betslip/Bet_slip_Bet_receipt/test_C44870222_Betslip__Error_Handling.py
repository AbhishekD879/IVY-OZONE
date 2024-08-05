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
class Test_C44870222_Betslip__Error_Handling(Common):
    """
    TR_ID: C44870222
    NAME: Betslip - Error Handling
    DESCRIPTION: "Verify User sees following errors on betslip
    DESCRIPTION: - ""There was an error when attempting to place your bet, please try again."" when there is Boosted Odds mismatch
    DESCRIPTION: -  ""Your Odds Boost has been expired/redeemed.' when token has already been used
    DESCRIPTION: -  ""Sorry, there may have been a problem placing your bet. To confirm if your bet was placed please check your Open bets.""when Openbet TimeOut
    DESCRIPTION: -   ""Your bet has not been accepted. Please try again."" when bet is rejected
    DESCRIPTION: -   ""Sorry, one of the selections cannot be boosted, please remove the selection and try again."" when  Odds Boost not allowed for selection
    PRECONDITIONS: 
    """
    keep_browser_open = True
