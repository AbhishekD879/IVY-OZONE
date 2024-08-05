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
class Test_C62162270_Verify_Cash_Out_Suspended_Button__Event_is_Pre_play(Common):
    """
    TR_ID: C62162270
    NAME: Verify Cash Out Suspended Button - Event is Pre-play
    DESCRIPTION: This test case verifies the Cash Out Suspended Button is displayed when event is suspended in Pre-Play
    DESCRIPTION: When the Displayed status is Y, Active status is S, Is OFF flag is N and cash out Flag is Y
    PRECONDITIONS: * User should place bet which has Cash Out
    PRECONDITIONS: * Cash Out Messaging should be configured in CMS
    PRECONDITIONS: * In OB /TI make the below changes
    PRECONDITIONS: * Display status is  **Y**
    PRECONDITIONS: * Active status is  **S**
    PRECONDITIONS: * Is OFF flag is  **N**
    PRECONDITIONS: * Cash out Flag is  **Y**
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

    def test_003__in_ob_make_the_changes_as_mentioned_in_the_pre_conditions_display_status_is_y_active_status_is_s_is_off_flag_is_n_cash_out_flag_is_y(self):
        """
        DESCRIPTION: * In OB make the changes as mentioned in the pre-conditions
        DESCRIPTION: * Display status is **Y**
        DESCRIPTION: * Active status is **S**
        DESCRIPTION: * Is OFF flag is **N**
        DESCRIPTION: * Cash out Flag is **Y**
        EXPECTED: 
        """
        pass

    def test_004_in_fe_navigate_to_my_bets_gt_open_bets(self):
        """
        DESCRIPTION: In FE navigate to My Bets &gt; Open Bets
        EXPECTED: * Cash Out Suspended Button should be displayed in Disabled state
        EXPECTED: **CO Messaging should NOT  be displayed**
        """
        pass
