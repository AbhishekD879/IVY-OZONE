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
class Test_C62773528_Verify_the_Cash_Out_Button_Events_are_in_Pre_Play__ACCA_bets(Common):
    """
    TR_ID: C62773528
    NAME: Verify the Cash Out Button -Events are in Pre-Play - ACCA bets
    DESCRIPTION: This test case verifies the display of Cash Out Button in Pre-play event
    DESCRIPTION: When the Displayed status is Y, Active status is A, Is OFF flag is N and cash out Flag is Y
    PRECONDITIONS: * User should place ACCA bet which has Cash Out
    PRECONDITIONS: * Cash Out Messaging should be configured in CMS
    PRECONDITIONS: * In OB /TI make the below changes
    PRECONDITIONS: Display status is  **Y**
    PRECONDITIONS: Active status is  **A**
    PRECONDITIONS: Is OFF flag is  **N**
    PRECONDITIONS: Cash out Flag is  **Y**
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

    def test_003__in_ob_make_the_changes_as_mentioned_in_the_pre_condition_for_any_one_of_the_selection_in_acca_betdisplay_status_is_yactive_status_is_ais_off_flag_is_ncash_out_flag_is_y(self):
        """
        DESCRIPTION: * In OB make the changes as mentioned in the pre-condition for ANY ONE of the selection in ACCA bet
        DESCRIPTION: Display status is **Y**
        DESCRIPTION: Active status is **A**
        DESCRIPTION: Is OFF flag is **N**
        DESCRIPTION: Cash out Flag is **Y**
        EXPECTED: 
        """
        pass

    def test_004_in_fe_navigate_to_my_bets_gt_open_bets(self):
        """
        DESCRIPTION: In FE navigate to My Bets &gt; Open Bets
        EXPECTED: * Cash Out Button is displayed with Cash Out Value
        EXPECTED: **CO Messaging should NOT be displayed**
        """
        pass

    def test_005__in_ob_make_the_changes_as_mentioned_in_the_pre_condition_for_all_of_the_selection_in_acca_betdisplay_status_is_yactive_status_is_ais_off_flag_is_ncash_out_flag_is_y(self):
        """
        DESCRIPTION: * In OB make the changes as mentioned in the pre-condition for ALL of the selection in ACCA bet
        DESCRIPTION: Display status is **Y**
        DESCRIPTION: Active status is **A**
        DESCRIPTION: Is OFF flag is **N**
        DESCRIPTION: Cash out Flag is **Y**
        EXPECTED: 
        """
        pass

    def test_006_in_fe_navigate_to_my_bets_gt_open_bets(self):
        """
        DESCRIPTION: In FE navigate to My Bets &gt; Open Bets
        EXPECTED: * Cash Out Button is displayed with Cash Out Value
        EXPECTED: **CO Messaging should NOT be displayed**
        """
        pass
