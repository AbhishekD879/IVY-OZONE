import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C64368346_Verify_the_Max_Pay_Tool_Tip_info_icon_displayed_in_Settled_Bets_when_User_placed_bet_on_SP(Common):
    """
    TR_ID: C64368346
    NAME: Verify the Max Pay Tool Tip info icon displayed in Settled Bets when User placed bet on SP
    DESCRIPTION: This test case verifies the display of 'i' icon in My Bets Settled Bets
    PRECONDITIONS: 1: Maximum Payout should be configured in Open bet
    PRECONDITIONS: 2: Potential/Estimated returns should be greater than Maximum Payout configured in OB
    PRECONDITIONS: 3: Max Pay Out banner should be enabled in CMS
    PRECONDITIONS: 4: User should place bet on HR/ GH events with SP price
    PRECONDITIONS: 5: When the Bet is settled SP should be higher so that the potential returns Exceed the Max Pay configured in OB
    PRECONDITIONS: Max Payout is already returned to us by OpenBet via the max_payout value as part of the reqBetBuild request.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral Application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_click_on_any_selection_from_any_with_sp_price_from_hrgh_events(self):
        """
        DESCRIPTION: Click on any selection from ANY with SP price from HR/GH events
        EXPECTED: Desktop : Selection should be added to Betslip
        EXPECTED: Mobile: Click on Add to Betslip in Quick bet Overlay
        """
        pass

    def test_003_enter_stake_and_place_bet(self):
        """
        DESCRIPTION: Enter Stake and Place Bet
        EXPECTED: * Bet Should be placed
        EXPECTED: * Bet Receipt should be generated
        EXPECTED: * Potential/Estimated Returns should be displayed as NA
        """
        pass

    def test_004_navigate_to_my_betsopen_bets(self):
        """
        DESCRIPTION: Navigate to My Bets/Open Bets
        EXPECTED: * Bet should be displayed
        EXPECTED: * Tool Tip icon is NOT displayed
        """
        pass

    def test_005_settle_the_bet_from_ob_with_sp_value_higher_so_that_potential_returns_exceed_the_max_pay_configured_give_the_lp_set_results_gt_sp_higher(self):
        """
        DESCRIPTION: Settle the Bet from OB with SP value higher so that Potential Returns Exceed the Max Pay configured
        DESCRIPTION: * Give the LP
        DESCRIPTION: * Set Results &gt; SP higher
        EXPECTED: 
        """
        pass

    def test_006_navigate_to_my_bets_section_gt_settled_bets(self):
        """
        DESCRIPTION: Navigate to My Bets section &gt; Settled Bets
        EXPECTED: * Look for the placed bet
        EXPECTED: * 'i' icon is displayed before Returns
        """
        pass

    def test_007_click_or_hover_on_the_info_icon(self):
        """
        DESCRIPTION: Click or Hover on the info icon
        EXPECTED: Tool Tip Text is displayed
        """
        pass

    def test_008_only_mobilerepeat_the_same_for_quick_bet_receipt(self):
        """
        DESCRIPTION: **ONLY MOBILE**
        DESCRIPTION: Repeat the same for Quick Bet Receipt
        EXPECTED: 
        """
        pass

    def test_009_repeat_the_same_with_sp_value_at_settlement_is_less_so_that_max_pay_is_not_triggered_validate_that_tool_tip_info_icon_is_not_displayed(self):
        """
        DESCRIPTION: Repeat the same with SP value at settlement is less so that Max Pay is not triggered
        DESCRIPTION: * Validate that tool tip info icon is not displayed
        EXPECTED: * Bet is displayed in settled bets
        EXPECTED: * User should not see any tool tip info icon
        """
        pass

    def test_010_repeat_the_above_with_bog_enabled(self):
        """
        DESCRIPTION: Repeat the above with BOG enabled
        EXPECTED: 
        """
        pass
