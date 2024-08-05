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
class Test_C62162277_Verify_Cash_Out_Suspended_Button__Market_Suspended__Pre_Play_Event(Common):
    """
    TR_ID: C62162277
    NAME: Verify Cash Out Suspended Button - Market Suspended - Pre-Play Event
    DESCRIPTION: This test case verifies the display of Cash Out Suspended button when Market is Suspended
    DESCRIPTION: Event-Display status is Y Active status is A, Is OFF Flag is N and cash out Flag is Y
    DESCRIPTION: Market-Display status is Y, Active status is S and Cash out Flag is Y
    PRECONDITIONS: * User should place bet which has Cash Out
    PRECONDITIONS: * Cash Out Messaging should be configured in CMS
    PRECONDITIONS: * In OB /TI make the below changes
    PRECONDITIONS: **Event Level**
    PRECONDITIONS: Event-Display status is Y Active status is A, Is OFF Flag is N and cash out Flag is Y
    PRECONDITIONS: **Market Level**
    PRECONDITIONS: Market-Display status is Y, Active status is S and Cash out Flag is Y
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

    def test_003_in_ob_make_the_changesevent_levelevent_display_status_is_y_active_status_is_a_is_off_flag_is_n_and_cash_out_flag_is_ymarket_levelmarket_display_status_is_y_active_status_is_s_and_cash_out_flag_is_y(self):
        """
        DESCRIPTION: In OB make the changes
        DESCRIPTION: **Event Level**
        DESCRIPTION: Event-Display status is Y Active status is A, Is OFF Flag is N and cash out Flag is Y
        DESCRIPTION: **Market Level**
        DESCRIPTION: Market-Display status is Y, Active status is S and Cash out Flag is Y
        EXPECTED: 
        """
        pass

    def test_004_in_fe_navigate_to_my_bets_gt_open_bets(self):
        """
        DESCRIPTION: In FE navigate to My Bets &gt; Open Bets
        EXPECTED: * Cash Out Suspended Button should be displayed
        EXPECTED: **CO messaging should NOT be displayed**
        """
        pass
