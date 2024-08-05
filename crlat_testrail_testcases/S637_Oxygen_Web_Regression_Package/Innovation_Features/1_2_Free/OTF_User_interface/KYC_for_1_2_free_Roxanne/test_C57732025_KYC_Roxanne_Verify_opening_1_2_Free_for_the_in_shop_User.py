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
class Test_C57732025_KYC_Roxanne_Verify_opening_1_2_Free_for_the_in_shop_User(Common):
    """
    TR_ID: C57732025
    NAME: [KYC] [Roxanne] Verify opening 1-2-Free for the in shop User
    DESCRIPTION: This test case verifies the successful navigation to the 1-2-free game flow for the in shop customer.
    PRECONDITIONS: The User is an in shop user.
    PRECONDITIONS: Age /identity checks are completed face to face for in shop users before allowing access and should therefore never be blocked from play 1-2-FREE even if customer is not in reviewed state.
    """
    keep_browser_open = True

    def test_001_tap_on_the_quick_link_for_any_1_2_free_game(self):
        """
        DESCRIPTION: Tap on the quick link for any 1-2-free game.
        EXPECTED: The User will be navigated to the 1-2-free game flow.
        EXPECTED: The User can continue to make a prediction as normal.
        """
        pass
