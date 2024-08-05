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
class Test_C22179405_TO_BE_UpdatedVanilla__Verify_successful_Deposit_for_Visa_direct_Through_Safecharge(Common):
    """
    TR_ID: C22179405
    NAME: [TO BE Updated]][Vanilla] - Verify successful Deposit for Visa direct (Through Safecharge)
    DESCRIPTION: This test case verifies Deposit of Funds for registered Payment Methods.
    PRECONDITIONS: 
    """
    keep_browser_open = True
