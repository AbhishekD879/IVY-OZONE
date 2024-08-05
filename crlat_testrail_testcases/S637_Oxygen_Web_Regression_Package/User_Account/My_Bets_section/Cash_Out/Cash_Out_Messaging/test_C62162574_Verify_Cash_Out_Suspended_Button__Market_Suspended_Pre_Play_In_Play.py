import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C62162574_Verify_Cash_Out_Suspended_Button__Market_Suspended_Pre_Play_In_Play(Common):
    """
    TR_ID: C62162574
    NAME: Verify Cash Out Suspended Button - Market Suspended- Pre-Play & In-Play
    DESCRIPTION: This test case verifies that Cash Out Suspended button is displayed when Market is Suspended
    PRECONDITIONS: * User should place bet which has Cash Out available
    PRECONDITIONS: * Event should be in Pre-Play
    PRECONDITIONS: * In OB /TI Active Status of the Market should be **S**
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_my_bets_gt_open_bets(self):
        """
        DESCRIPTION: Navigate to My Bets &gt; Open Bets
        EXPECTED: * User should be displayed with Open Bets
        EXPECTED: * Cash Out button should be displayed for the Bet along with Cash Out Value
        """
        pass

    def test_003_in_ob_suspend_the_market(self):
        """
        DESCRIPTION: In OB suspend the Market
        EXPECTED: 
        """
        pass

    def test_004_in_fe_navigate_to_my_bets_gt_open_bets(self):
        """
        DESCRIPTION: In FE navigate to My Bets &gt; Open Bets
        EXPECTED: * Cash Out Suspended button should be displayed
        EXPECTED: * Cash Out Suspended button should be disabled
        """
        pass

    def test_005_in_ob_make_the_event_to_in_playis_off_status_to_ythen_suspend_the_market(self):
        """
        DESCRIPTION: In OB make the event to In-play
        DESCRIPTION: Is OFF status to **Y**
        DESCRIPTION: Then, Suspend the Market
        EXPECTED: 
        """
        pass

    def test_006_in_fe_navigate_to_my_bets_gt_open_bets(self):
        """
        DESCRIPTION: In FE navigate to My Bets &gt; Open Bets
        EXPECTED: * Cash Out Suspended button should be displayed
        EXPECTED: * Cash Out Suspended button should be disabled
        """
        pass

    def test_007_repeat_for_multiple_bets_acca_bets__complex_bets(self):
        """
        DESCRIPTION: Repeat for Multiple Bets, ACCA bets & Complex Bets
        EXPECTED: 
        """
        pass
