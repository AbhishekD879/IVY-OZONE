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
class Test_C16268993_Vanilla_Verify_balance_updating_during_multiple_log_in(Common):
    """
    TR_ID: C16268993
    NAME: [Vanilla] Verify balance updating during multiple log in
    DESCRIPTION: This test case verifies balance updating during multiple log in
    PRECONDITIONS: - User should be logged in the same account from multiple devices.
    PRECONDITIONS: - Remember user's balance
    """
    keep_browser_open = True

    def test_001_important_note_vanilla_vano_503___according_to_this_task_resolution_balance_is_supposed_to_be_updated_in_real_time_only_on_the_device_that_was_refreshedlogged_in_most_recently(self):
        """
        DESCRIPTION: *Important note:* Vanilla, VANO-503 - according to this task resolution, balance is supposed to be updated in real time only on the device that was refreshed/logged in most recently
        EXPECTED: 
        """
        pass

    def test_002_make_multiple_login_the_same_account(self):
        """
        DESCRIPTION: Make multiple login the same account
        EXPECTED: 
        """
        pass

    def test_003_make_a_deposit_from_device_1(self):
        """
        DESCRIPTION: Make a deposit from Device 1
        EXPECTED: - Deposit is successful on Device 2
        EXPECTED: - User's balance is increased
        """
        pass

    def test_004_verify_users_balance_on_device_2(self):
        """
        DESCRIPTION: Verify user's balance on Device 2
        EXPECTED: User's balance is updated in real time
        """
        pass

    def test_005_make_a_withdraw_from_device_1(self):
        """
        DESCRIPTION: Make a withdraw from Device 1
        EXPECTED: - Withdraw is successful on Device 1
        EXPECTED: - User's balance is decreased
        """
        pass

    def test_006_verify_users_balance_on_device_2(self):
        """
        DESCRIPTION: Verify user's balance on Device 2
        EXPECTED: User's balance is updated in real time
        """
        pass

    def test_007_make_a_few_bet_placement_from_device_1(self):
        """
        DESCRIPTION: Make a few bet placement from Device 1
        EXPECTED: - Bet placement is successful on Device 1
        EXPECTED: - User's balance is decreased
        """
        pass

    def test_008_verify_users_balance_on_device_2(self):
        """
        DESCRIPTION: Verify user's balance on Device 2
        EXPECTED: User's balance is updated in real time
        """
        pass
