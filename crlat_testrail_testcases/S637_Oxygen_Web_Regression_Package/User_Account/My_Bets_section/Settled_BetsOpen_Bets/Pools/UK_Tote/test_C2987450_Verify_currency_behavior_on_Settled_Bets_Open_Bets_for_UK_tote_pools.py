import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C2987450_Verify_currency_behavior_on_Settled_Bets_Open_Bets_for_UK_tote_pools(Common):
    """
    TR_ID: C2987450
    NAME: Verify currency behavior on Settled Bets/Open Bets for UK tote pools
    DESCRIPTION: This test case verifies currency sign display on Settled Bets/Open Bets for UK tote pools when user and pool currencies are different.
    PRECONDITIONS: User is logged in with different currency than UK tote pool currency (eg user currency - 'EUR', UK pool currency - ''GBP'')
    PRECONDITIONS: User has placed some single/multiple bet/s from any pool type available (Win/Place/Execta/Trifecta...)
    PRECONDITIONS: User has placed some single/multiple bet/s from any pool type available (Win/Place/Execta/Trifecta...) and bets are already SETTLED
    PRECONDITIONS: User is on My bets tab 'Open Bets: Pools' section
    """
    keep_browser_open = True

    def test_001_verify_stake_currency_sign_for_single_bet_placed_from_any_pool_type(self):
        """
        DESCRIPTION: Verify Stake currency sign for single bet placed from any pool type
        EXPECTED: Stake currency sign is displayed under the bet in User currency and user currency sign
        """
        pass

    def test_002_verify_stake_currency_sign_for_multiple_bet_placed_from_any_pool_type(self):
        """
        DESCRIPTION: Verify Stake currency sign for multiple bet placed from any pool type
        EXPECTED: Stake currency sign is displayed under the bet in User currency and user currency sign
        """
        pass

    def test_003_navigate_to_settled_bets_pools_tab_and_verify_stake_currency_sign_for_settled_single_bet_from_any_pool_type(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets: Pools' tab and verify Stake currency sign for settled single bet from any pool type
        EXPECTED: Stake currency sign is displayed under the bet in User currency and user currency sign
        """
        pass

    def test_004_verify_stake_currency_sign_for_settled_multiple_bet_from_any_pool_type(self):
        """
        DESCRIPTION: Verify Stake currency sign for settled multiple bet from any pool type
        EXPECTED: Stake currency sign is displayed under the bet in User currency and user currency sign
        """
        pass
