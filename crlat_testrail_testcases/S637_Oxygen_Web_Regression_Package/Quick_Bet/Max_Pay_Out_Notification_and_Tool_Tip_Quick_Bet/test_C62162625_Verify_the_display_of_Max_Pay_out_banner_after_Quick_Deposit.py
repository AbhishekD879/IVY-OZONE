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
class Test_C62162625_Verify_the_display_of_Max_Pay_out_banner_after_Quick_Deposit(Common):
    """
    TR_ID: C62162625
    NAME: Verify the display of Max Pay out banner after Quick Deposit
    DESCRIPTION: This test case verifies the display of Max pay out banner on Quick Bet after Quick Deposit
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

    def test_003_enter_stake_stake_should_be_higher_than_the_user_account_balance___trigger_deposit_banner_stake_entered_should_trigger_potential_estimated_returns_higher_than_the_maximum_payout_configured(self):
        """
        DESCRIPTION: Enter Stake
        DESCRIPTION: * Stake should be higher than the User account balance - Trigger Deposit banner
        DESCRIPTION: * Stake entered should trigger Potential /Estimated Returns higher than the Maximum payout configured
        EXPECTED: * Deposit banner should be displayed
        EXPECTED: * Max Pay out banner should be displayed
        EXPECTED: * Text displayed should be same as configured in CMS
        EXPECTED: * T&C'S link should be displayed
        EXPECTED: * 'i' icon should be displayed
        """
        pass

    def test_004_make_quick_deposit(self):
        """
        DESCRIPTION: Make Quick Deposit
        EXPECTED: * User should be able to complete the deposit successfully
        EXPECTED: * User should be displayed quick bet overlay
        EXPECTED: * Stake entered earlier should be pre-filled
        """
        pass

    def test_005_validate_the_display_of_max_payout_banner(self):
        """
        DESCRIPTION: Validate the display of Max payout banner
        EXPECTED: * Max payout banner should be displayed
        """
        pass
