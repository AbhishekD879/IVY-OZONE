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
class Test_C62969380_Verify_GA_tracking_when_Clicked_on_Terms_Conditions_link_in_Max_Pay_Out_Banner(Common):
    """
    TR_ID: C62969380
    NAME: Verify GA tracking when Clicked on Terms & Conditions link in Max Pay Out Banner
    DESCRIPTION: This test case verifies the GA tracking when User clicks on Terms and Conditions link in the Max Pay Out banner
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

    def test_004_click_on_the_terms_and_conditions_link(self):
        """
        DESCRIPTION: Click on the Terms and Conditions Link
        EXPECTED: User should be navigated to Terms and Conditions page as Configured in CMS
        """
        pass

    def test_005_validate_the_ga_tracking_in_console(self):
        """
        DESCRIPTION: Validate the GA tracking in console
        EXPECTED: 
        """
        pass

    def test_006_repeat_the_same_for_quick_bet_in_simulator(self):
        """
        DESCRIPTION: Repeat the same for Quick Bet in simulator
        EXPECTED: 
        """
        pass
