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
class Test_C62162606_Verify_the_display_of_Max_Pay_out_banner_on_Quick_Bet(Common):
    """
    TR_ID: C62162606
    NAME: Verify the display of Max Pay out banner on Quick Bet
    DESCRIPTION: This Test case Verifies the display Max payout banner on quick bet when Estimated returns is greater than Maximum payout configured for the bet
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
        EXPECTED: Quick Bet Overlay should be displayed
        """
        pass

    def test_003_enter_stakeentered_stake_should_trigger_the_estimated_potential_returns_higher_than_maximum_payout_configuredvalidate_the_display_of_max_pay_out_banner(self):
        """
        DESCRIPTION: Enter Stake
        DESCRIPTION: (Entered Stake should trigger the estimated /potential returns higher than Maximum Payout configured)
        DESCRIPTION: Validate the display of Max Pay Out banner
        EXPECTED: * Max Pay out banner should be displayed
        EXPECTED: * Text displayed should be same as configured in CMS
        EXPECTED: * T&C'S link should be displayed
        EXPECTED: * 'i' icon should be displayed
        EXPECTED: ![](index.php?/attachments/get/161019017)
        EXPECTED: ![](index.php?/attachments/get/161019019)
        """
        pass
