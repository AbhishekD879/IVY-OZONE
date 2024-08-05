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
class Test_C62162631_CoralVerify_the_info_icon_is_displayed_next_to_Returns_for_Settled_Bets(Common):
    """
    TR_ID: C62162631
    NAME: Coral:Verify the info icon is displayed next to Returns for Settled Bets
    DESCRIPTION: This test case verifies the display of 'i' icon in My Bets Settled Bets
    PRECONDITIONS: 1: Maximum Payout should be configured in Open bet
    PRECONDITIONS: 2: Potential/Estimated returns should be greater than Maximum Payout configured in OB
    PRECONDITIONS: 3: Max Pay Out banner should be enabled in CMS
    PRECONDITIONS: Max Payout is already returned to us by OpenBet via the max_payout value as part of the reqBetBuild request.
    """
    keep_browser_open = True

    def test_001_launch_coral_application(self):
        """
        DESCRIPTION: Launch Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_click_on_any_selection_from_any_eventsportracing(self):
        """
        DESCRIPTION: Click on any selection from ANY event(Sport/Racing)
        EXPECTED: Desktop : Selection should be added to Betslip
        EXPECTED: Mobile: Click on Add to Betslip in Quick bet Overlay
        """
        pass

    def test_003_enter_stake_and_validate_the_display_of_max_payout_bannerentered_stake_should_trigger_the_estimated_potential_returns_higher_than_maximum_payout_configured(self):
        """
        DESCRIPTION: Enter Stake and Validate the display of Max payout banner
        DESCRIPTION: (Entered Stake should trigger the estimated /potential returns higher than Maximum Payout configured)
        EXPECTED: * Max Pay out banner should be displayed
        EXPECTED: * Text displayed should be same as configured in CMS
        EXPECTED: * T&C'S link should be displayed
        EXPECTED: * 'i' icon should be displayed
        """
        pass

    def test_004_click_on_place_bet_and_validate_the_display_of_i_icon(self):
        """
        DESCRIPTION: Click on Place Bet and Validate the display of 'i' icon
        EXPECTED: * User should be able to Place bet successfully
        EXPECTED: * Bet receipt should be generated
        EXPECTED: * 'i' icon should be displayed after Estimated/Potential Returns text
        """
        pass

    def test_005_settle_the_bet_from_ob(self):
        """
        DESCRIPTION: Settle the Bet from OB
        EXPECTED: 
        """
        pass

    def test_006_navigate_to_my_bets_section(self):
        """
        DESCRIPTION: Navigate to My Bets section
        EXPECTED: * Cash Out Bets tab is displayed
        """
        pass

    def test_007_click_on_settled_bets_tab(self):
        """
        DESCRIPTION: Click on Settled Bets tab
        EXPECTED: * 'i' icon is displayed next to Returns
        """
        pass

    def test_008_click_or_hover_on_the_info_icon(self):
        """
        DESCRIPTION: Click or Hover on the info icon
        EXPECTED: Tool Tip Text is displayed
        """
        pass

    def test_009_only_mobilerepeat_the_same_for_quick_bet_receipt(self):
        """
        DESCRIPTION: **ONLY MOBILE**
        DESCRIPTION: Repeat the same for Quick Bet Receipt
        EXPECTED: 
        """
        pass