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
class Test_C22179391_Vanilla__Verify_successful_Deposit_for_Paysafecard(Common):
    """
    TR_ID: C22179391
    NAME: [Vanilla] - Verify successful Deposit for Paysafecard
    DESCRIPTION: This test case verifies Deposit of Funds for registered Payment Methods.
    PRECONDITIONS: 1. User should register at least 1 payment method - Paysafecard;
    PRECONDITIONS: 2. User logged into the application;
    """
    keep_browser_open = True
