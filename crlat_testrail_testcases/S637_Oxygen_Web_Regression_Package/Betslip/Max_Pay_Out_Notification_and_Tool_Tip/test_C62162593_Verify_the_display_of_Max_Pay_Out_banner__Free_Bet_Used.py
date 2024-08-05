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
class Test_C62162593_Verify_the_display_of_Max_Pay_Out_banner__Free_Bet_Used(Common):
    """
    TR_ID: C62162593
    NAME: Verify the display of Max Pay Out banner - Free Bet Used
    DESCRIPTION: This Test case verifies the display Of Max Payout banner on Betslip when Free bets are used
    PRECONDITIONS: 1: Maximum Payout should be configured in Open bet
    PRECONDITIONS: 2: Potential/Estimated returns should be greater than Maximum Payout configured in OB
    PRECONDITIONS: 3: Max Pay Out banner should be enabled in CMS
    PRECONDITIONS: 4: Free bets should be available for the User
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

    def test_003_use_free_bets_and__validate_the_display_of_max_payout_bannerfree_bets_used_should_trigger_the_estimated_potential_returns_higher_than_maximum_payout_configured(self):
        """
        DESCRIPTION: Use Free bets and  Validate the display of Max payout banner
        DESCRIPTION: (Free Bets Used should trigger the estimated /potential returns higher than Maximum Payout configured)
        EXPECTED: * Max Pay out banner should be displayed
        EXPECTED: * Text displayed should be same as configured in CMS
        EXPECTED: * T&C'S link should be displayed
        EXPECTED: * 'i' icon should be displayed
        """
        pass
