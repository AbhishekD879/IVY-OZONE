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
class Test_C62162590_Verify_the_undisplay_of_Max_Pay_out_banner_on_changing_Stake(Common):
    """
    TR_ID: C62162590
    NAME: Verify the undisplay of Max Pay out banner on changing Stake
    DESCRIPTION: This test case verifies the undisplay of Max payout banner on quick bet on changing the stake to change the Estimated returns less than the Maximum payout configured for the bet
    PRECONDITIONS: 1: Maximum Payout should be configured in Open bet
    PRECONDITIONS: 2: Potential/Estimated returns should be greater than Maximum Payout configured in OB
    PRECONDITIONS: 3: Max Pay Out banner should be enabled in CMS
    PRECONDITIONS: Max Payout is already returned to us by OpenBet via the max_payout value as part of the reqBetBuild request.
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
        EXPECTED: Selection should be added to betslip displayed
        """
        pass

    def test_003_enter_stake_and_validate_the_display_of_max_payout_bannerentered_stake_should_trigger_the_estimated_potential_returns_higher_than_maximum_payout_configured(self):
        """
        DESCRIPTION: Enter Stake and Validate the display of Max payout banner
        DESCRIPTION: (Entered Stake should trigger the estimated /potential returns higher than Maximum Payout configured)
        EXPECTED: Max Pay out banner should be displayed
        EXPECTED: Text displayed should be same as configured in CMS
        EXPECTED: T&C'S link should be displayed
        EXPECTED: 'i' icon should be displayed
        """
        pass

    def test_004_edit_the_stake_and_validate_the_display_of_max_payout_banneredited_stake_should_not_trigger_the_estimated_potential_returns_less_than_the_maximum_payout_configured(self):
        """
        DESCRIPTION: Edit the Stake and Validate the display of Max payout banner
        DESCRIPTION: (Edited Stake should not trigger the Estimated /Potential Returns less than the Maximum Payout configured)
        EXPECTED: Max pay out banner should no longer be displayed
        """
        pass
