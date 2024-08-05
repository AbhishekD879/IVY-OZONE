import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C22179397_Vanilla__Verify_successful_Deposit_for__AIB_acquirer(Common):
    """
    TR_ID: C22179397
    NAME: [Vanilla] - Verify successful Deposit for - AIB (acquirer)
    DESCRIPTION: This test case verifies Deposit of Funds for registered Payment Methods.
    PRECONDITIONS: 
    """
    keep_browser_open = True
