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
class Test_C62162601_Verify_the_redirection_of_page_on_clicking_TCs_link(Common):
    """
    TR_ID: C62162601
    NAME: Verify the redirection of page on clicking T&C's link
    DESCRIPTION: This test case verifies the redirection of page on clicking T&C's link
    PRECONDITIONS: 1: Maximum Payout should be configured in Open bet
    PRECONDITIONS: 2: Potential/Estimated returns should be greater than Maximum Payout configured in OB
    PRECONDITIONS: 3: Max Pay Out banner should be enabled in CMS
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able launch the application successfully
        """
        pass

    def test_002_click_on_any_selection_from_any_eventsportracing(self):
        """
        DESCRIPTION: Click on any selection from ANY event(Sport/Racing)
        EXPECTED: Desktop : Selection should be added to Betslip
        EXPECTED: Mobile: Click on Add to Betslip in Quick bet Overlay
        """
        pass

    def test_003_enter_stakeentered_stake_should_trigger_the_estimated_potential_returns_higher_than_maximum_payout_configured(self):
        """
        DESCRIPTION: Enter Stake
        DESCRIPTION: (Entered Stake should trigger the estimated /potential returns higher than Maximum Payout configured)
        EXPECTED: * Max Pay out banner should be displayed
        EXPECTED: * Text displayed should be same as configured in CMS
        EXPECTED: * T&C'S link should be displayed
        EXPECTED: * 'i' icon should be displayed
        """
        pass

    def test_004_ladbrokes__click_on_tcs_link(self):
        """
        DESCRIPTION: Ladbrokes- Click on T&C's link
        EXPECTED: User should be redirected to
        EXPECTED: https://help.ladbrokes.com/en/sports-help/sports-rules#maxpayouts
        """
        pass

    def test_005_coral__click_on_tcs_link(self):
        """
        DESCRIPTION: Coral- Click on T&C's link
        EXPECTED: User should be redirected to
        EXPECTED: https://help.coral.co.uk/en/sports-help/sports-rules
        """
        pass
