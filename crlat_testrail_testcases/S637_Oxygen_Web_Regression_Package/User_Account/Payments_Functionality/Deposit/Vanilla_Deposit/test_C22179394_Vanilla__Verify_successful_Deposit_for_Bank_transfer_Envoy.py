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
class Test_C22179394_Vanilla__Verify_successful_Deposit_for_Bank_transfer_Envoy(Common):
    """
    TR_ID: C22179394
    NAME: [Vanilla] - Verify successful Deposit for Bank transfer (Envoy)
    DESCRIPTION: This test case verifies Deposit of Funds for registered Payment Methods.
    PRECONDITIONS: 
    """
    keep_browser_open = True
