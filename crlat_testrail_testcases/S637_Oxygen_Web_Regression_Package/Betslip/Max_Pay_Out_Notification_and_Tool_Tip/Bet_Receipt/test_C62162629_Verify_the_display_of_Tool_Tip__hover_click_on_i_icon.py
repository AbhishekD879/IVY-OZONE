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
class Test_C62162629_Verify_the_display_of_Tool_Tip__hover_click_on_i_icon(Common):
    """
    TR_ID: C62162629
    NAME: Verify the display of Tool Tip - hover/click on 'i' icon
    DESCRIPTION: This test case verifies the display of Tool Tip text
    PRECONDITIONS: 1: Maximum Payout should be configured in Open bet
    PRECONDITIONS: 2: Potential/Estimated returns should be greater than Maximum Payout configured in OB
    PRECONDITIONS: 3: Max Pay Out banner should be enabled in CMS
    PRECONDITIONS: Max Payout is already returned to us by OpenBet via the max_payout value as part of the reqBetBuild request.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
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

    def test_005_click_or_hover_on_the_i_icon(self):
        """
        DESCRIPTION: Click or hover on the 'i' icon
        EXPECTED: * Tool Tip Text should be displayed
        """
        pass

    def test_006_only_mobilerepeat_the_same_for_quick_bet_receipt(self):
        """
        DESCRIPTION: **ONLY MOBILE**
        DESCRIPTION: Repeat the same for Quick Bet Receipt
        EXPECTED: 
        """
        pass