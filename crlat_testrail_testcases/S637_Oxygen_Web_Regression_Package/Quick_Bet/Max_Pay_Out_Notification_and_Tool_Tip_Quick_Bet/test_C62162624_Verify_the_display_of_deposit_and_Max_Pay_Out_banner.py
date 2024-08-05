import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C62162624_Verify_the_display_of_deposit_and_Max_Pay_Out_banner(Common):
    """
    TR_ID: C62162624
    NAME: Verify the display of deposit and Max Pay Out banner
    DESCRIPTION: This test case verifies the display of Deposit and Max pay out banner on Quick Bet
    PRECONDITIONS: 1: Maximum Payout should be configured in Open bet
    PRECONDITIONS: 2: Potential/Estimated returns should be greater than Maximum Payout configured in OB
    PRECONDITIONS: 3: Max Pay Out banner should be enabled in CMS
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_in_mobile_web_or_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral in Mobile Web or app
        EXPECTED: User should be able launch the application successfully
        """
        pass

    def test_002_click_on_any_selection_from_any_eventsportracing(self):
        """
        DESCRIPTION: Click on any selection from ANY event(Sport/Racing)
        EXPECTED: Quick Bet Overlay should be displayed
        """
        pass

    def test_003_enter_stake_and_validate_the_display_of_deposit_banner_and_max_payout_banner_stake_should_be_higher_than_the_user_account_balance___trigger_deposit_banner_stake_entered_should_trigger_potential_estimated_returns_higher_than_the_maximum_payout_configured(self):
        """
        DESCRIPTION: Enter Stake and Validate the display of deposit banner and Max Payout banner
        DESCRIPTION: * Stake should be higher than the User account balance - Trigger Deposit banner
        DESCRIPTION: * Stake entered should trigger Potential /Estimated Returns higher than the Maximum payout configured
        EXPECTED: * Deposit banner should be displayed
        EXPECTED: * Max Pay out banner should be displayed
        EXPECTED: * Text displayed should be same as configured in CMS
        EXPECTED: * T&C'S link should be displayed
        EXPECTED: * 'i' icon should be displayed
        """
        pass
