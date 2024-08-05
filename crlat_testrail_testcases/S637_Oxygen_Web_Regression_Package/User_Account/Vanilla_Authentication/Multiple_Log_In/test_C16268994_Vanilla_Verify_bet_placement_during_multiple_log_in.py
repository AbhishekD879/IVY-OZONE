import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C16268994_Vanilla_Verify_bet_placement_during_multiple_log_in(Common):
    """
    TR_ID: C16268994
    NAME: [Vanilla] Verify bet placement during multiple log in
    DESCRIPTION: This test case verifies bet placement during multiple log in
    PRECONDITIONS: User should be logged in the same account with posotive balance from multiple devices
    """
    keep_browser_open = True

    def test_001_make_multiple_login_the_same_account(self):
        """
        DESCRIPTION: Make multiple login the same account
        EXPECTED: 
        """
        pass

    def test_002_make_a_single_bet_placement_from_device_1(self):
        """
        DESCRIPTION: Make a single bet placement from Device 1
        EXPECTED: Bet placement is successful
        """
        pass

    def test_003_make_a_single_bet_placement_from_device_2(self):
        """
        DESCRIPTION: Make a single bet placement from Device 2
        EXPECTED: Bet placement is successful
        """
        pass

    def test_004_make_a_multiple_bet_placement_from_device_1(self):
        """
        DESCRIPTION: Make a multiple bet placement from Device 1
        EXPECTED: Bet placement is successful
        """
        pass

    def test_005_make_a_multiple_bet_placement_from_device_2(self):
        """
        DESCRIPTION: Make a multiple bet placement from Device 2
        EXPECTED: Bet placement is successful
        """
        pass
