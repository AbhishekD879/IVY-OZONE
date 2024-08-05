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
class Test_C62969379_Verify_GA_tracking_when_Max_Pay_Out_Banner_is_triggered_Betslip_QuickBet(Common):
    """
    TR_ID: C62969379
    NAME: Verify GA tracking when Max Pay Out Banner is triggered_Betslip_QuickBet
    DESCRIPTION: This Test case verifies the GA tracking when Max Payout banner is triggered on Quick Bet & Betslip
    PRECONDITIONS: 1: Max Pay Out should be configured in CMS
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
        EXPECTED: Mobile Simulator: Click on Add to Betslip in Quick bet Overlay
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

    def test_004_validate_ga_tracking_in_console(self):
        """
        DESCRIPTION: Validate GA tracking in Console
        EXPECTED: 
        """
        pass

    def test_005_repeat_the_same_for_quick_bet_in_simulator(self):
        """
        DESCRIPTION: Repeat the same for Quick Bet in simulator
        EXPECTED: 
        """
        pass
