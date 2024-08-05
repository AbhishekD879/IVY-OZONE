import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C1922184_Warning_messages_for_Betslip_limitation_for_Tote_bets(Common):
    """
    TR_ID: C1922184
    NAME: Warning messages for Betslip limitation for Tote bets
    DESCRIPTION: This test case verifies warning messages for Tote bets in the betslip, which appear in the following cases:
    DESCRIPTION: * when user tries to place a bet with stake below minimum stake
    DESCRIPTION: * when user tries to place a bet with stake above maximum stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User's balance is sufficient to cover the bet stake
    PRECONDITIONS: * Overask is disabled for the user in TI tool
    PRECONDITIONS: * User has added UK Tote bet (any pool type) to the betslip
    PRECONDITIONS: * Betslip is opened
    """
    keep_browser_open = True

    def test_001_enter_stake_that_is_less_than_minimum_allowed_value_for_unit_stake_and_tap_bet_now(self):
        """
        DESCRIPTION: Enter stake that is **less** than minimum allowed value for **unit** stake and tap "BET NOW"
        EXPECTED: Error message appears:
        EXPECTED: **"Stake too small. The minimum stake per line is <MinStakePerLine> The minimum stake per bet is<MinStakePerBet>"**
        """
        pass

    def test_002_enter_stake_that_is_less_than_minimum_allowed_value_for_total_stake_but_more_than_minimum_allowed_value_for_unit_stake_and_tap_bet_now(self):
        """
        DESCRIPTION: Enter stake that is **less** than minimum allowed value for **total** stake (but more than minimum allowed value for unit stake) and tap "BET NOW"
        EXPECTED: Error message appears:
        EXPECTED: **"Stake too small. The minimum stake per line is <MinStakePerLine> The minimum stake per bet is<MinStakePerBet>"**
        """
        pass

    def test_003_enter_stake_that_is_more_than_maximum_allowed_value_for_unit_stake_but_less_than_maximum_allowed_value_for_total_stake_and_tap_bet_now(self):
        """
        DESCRIPTION: Enter stake that is **more** than maximum allowed value for **unit** stake (but less than maximum allowed value for total stake) and tap "BET NOW"
        EXPECTED: Error message appears:
        EXPECTED: **"Stake too high. The maximum stake per line is <MaxStakePerLine> The maximum stake per bet is<MaxStakePerBet>"**
        """
        pass

    def test_004_enter_stake_that_is_more_than_maximum_allowed_value_for_total_stake_but_less_than_maximum_allowed_value_for_unit_stake_and_tap_bet_nowto_edit_is_this_step_valid_how_can_we_enter_a_value__maxstake_and__maxunit_if_maxunit__maxstake(self):
        """
        DESCRIPTION: Enter stake that is **more** than maximum allowed value for **total** stake (but less than maximum allowed value for unit stake) and tap "BET NOW"
        DESCRIPTION: **TO EDIT** Is this step valid? How can we enter a value > MaxStake and < MaxUnit if MaxUnit < MaxStake?
        EXPECTED: Error message appears:
        EXPECTED: **"Stake too high. The maximum stake per line is <MaxStakePerLine> The maximum stake per bet is<MaxStakePerBet>"**
        """
        pass

    def test_005_enter_stake_with_an_incorrect_increment_and_tap_bet_now(self):
        """
        DESCRIPTION: Enter stake with an **incorrect** increment and tap "BET NOW"
        EXPECTED: Error message appears:
        EXPECTED: **"Stake must be in increments of £<incrementValue>"**
        """
        pass
