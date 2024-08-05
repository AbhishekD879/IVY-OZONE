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
class Test_C62951387_Verify_the_display_of_Max_Pay_out_banner_on_5_A_Side_Bet_Slip(Common):
    """
    TR_ID: C62951387
    NAME: Verify the display of Max Pay out banner on 5-A Side Bet Slip
    DESCRIPTION: This Test case verifies the display Of Max Payout banner on Betslip
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

    def test_002_add_selections_for_5_a_side_bet(self):
        """
        DESCRIPTION: Add Selections for 5-A Side Bet
        EXPECTED: 
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
