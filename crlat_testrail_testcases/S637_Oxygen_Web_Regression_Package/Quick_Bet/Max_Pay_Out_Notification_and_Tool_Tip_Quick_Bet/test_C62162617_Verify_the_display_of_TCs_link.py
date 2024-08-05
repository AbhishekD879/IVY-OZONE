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
class Test_C62162617_Verify_the_display_of_TCs_link(Common):
    """
    TR_ID: C62162617
    NAME: Verify the display of T&C's link
    DESCRIPTION: This test case verifies the display of T&C's link
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

    def test_003_enter_stake_and_validate_the_display_of_tcs_linkentered_stake_should_trigger_the_estimated_potential_returns_higher_than_maximum_payout_configured(self):
        """
        DESCRIPTION: Enter Stake and Validate the display of T&C's link
        DESCRIPTION: (Entered Stake should trigger the estimated /potential returns higher than Maximum Payout configured)
        EXPECTED: * Max Pay out banner should be displayed
        EXPECTED: * Text displayed should be same as configured in CMS
        EXPECTED: * T&C'S link should be displayed
        EXPECTED: * 'i' icon should be displayed
        EXPECTED: ![](index.php?/attachments/get/161019017)
        EXPECTED: ![](index.php?/attachments/get/161019019)
        """
        pass
