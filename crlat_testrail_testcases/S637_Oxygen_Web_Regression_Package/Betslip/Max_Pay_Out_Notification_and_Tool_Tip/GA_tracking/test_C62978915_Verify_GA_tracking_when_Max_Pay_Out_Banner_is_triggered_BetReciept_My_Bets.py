import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C62978915_Verify_GA_tracking_when_Max_Pay_Out_Banner_is_triggered_BetReciept_My_Bets(Common):
    """
    TR_ID: C62978915
    NAME: Verify GA tracking when Max Pay Out Banner is triggered_BetReciept_My Bets
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
