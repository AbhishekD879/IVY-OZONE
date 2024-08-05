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
class Test_C62162610_Verify_the_display_of_Max_Pay_Out_banner__Free_Bet_Used(Common):
    """
    TR_ID: C62162610
    NAME: Verify the display of Max Pay Out banner - Free Bet Used
    DESCRIPTION: This test case verifies the display of Max payout banner when free bet is used
    PRECONDITIONS: 1: Maximum Payout should be configured in Open bet
    PRECONDITIONS: 2: Potential/Estimated returns should be greater than Maximum Payout configured in OB
    PRECONDITIONS: 3: Max Pay Out banner should be enabled in CMS
    PRECONDITIONS: 4: User should have Free bets
    PRECONDITIONS: Max Payout is already returned to us by Open Bet via the max_payout value as part of the reqBetBuild request.
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

    def test_003_use_free_bets_and_validate_the_display_of_max_payout_bannerfree_bet_should_trigger_the_estimated_potential_returns_higher_than_maximum_payout_configured(self):
        """
        DESCRIPTION: Use Free Bets and Validate the display of Max Payout banner
        DESCRIPTION: (Free bet should trigger the estimated /potential returns higher than Maximum Payout configured)
        EXPECTED: * Max Pay out banner should be displayed
        EXPECTED: * Text displayed should be same as configured in CMS
        EXPECTED: * T&C'S link should be displayed
        EXPECTED: * 'i' icon should be displayed
        EXPECTED: ![](index.php?/attachments/get/161019017)
        EXPECTED: ![](index.php?/attachments/get/161019019)
        """
        pass

    def test_004_repeat_2__3_with_free_bet_and_stake(self):
        """
        DESCRIPTION: Repeat 2 & 3 with Free Bet and Stake
        EXPECTED: * Max Pay out banner should be displayed
        EXPECTED: * Text displayed should be same as configured in CMS
        EXPECTED: * T&C'S link should be displayed
        EXPECTED: * 'i' icon should be displayed
        EXPECTED: ![](index.php?/attachments/get/161019017)
        EXPECTED: ![](index.php?/attachments/get/161019019)
        """
        pass
