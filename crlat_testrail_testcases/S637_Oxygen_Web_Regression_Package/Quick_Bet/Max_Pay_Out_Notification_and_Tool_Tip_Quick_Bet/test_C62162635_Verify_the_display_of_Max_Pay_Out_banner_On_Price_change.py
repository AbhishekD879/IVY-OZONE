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
class Test_C62162635_Verify_the_display_of_Max_Pay_Out_banner_On_Price_change(Common):
    """
    TR_ID: C62162635
    NAME: Verify the display of Max Pay Out banner- On Price change
    DESCRIPTION: This test case verifies the display of Max payout banner on Price change
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

    def test_003_enter_stake(self):
        """
        DESCRIPTION: Enter Stake
        EXPECTED: 
        """
        pass

    def test_004_trigger_price_change_from_obupdated_price_should_trigger_potential_estimated_returns_higher_than_the_maximum_payout_configured(self):
        """
        DESCRIPTION: Trigger Price change from OB
        DESCRIPTION: (Updated Price should trigger Potential /Estimated Returns higher than the Maximum payout configured)
        EXPECTED: * Max Pay out banner should be displayed
        EXPECTED: * Text displayed should be same as configured in CMS
        EXPECTED: * T&C'S link should be displayed
        EXPECTED: * 'i' icon should be displayed
        """
        pass
