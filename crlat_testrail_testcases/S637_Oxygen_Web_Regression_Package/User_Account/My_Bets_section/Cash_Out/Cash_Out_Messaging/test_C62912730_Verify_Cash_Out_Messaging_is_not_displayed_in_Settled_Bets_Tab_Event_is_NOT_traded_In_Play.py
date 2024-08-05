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
class Test_C62912730_Verify_Cash_Out_Messaging_is_not_displayed_in_Settled_Bets_Tab_Event_is_NOT_traded_In_Play(Common):
    """
    TR_ID: C62912730
    NAME: Verify Cash Out Messaging is not displayed in Settled Bets Tab_Event is NOT traded In-Play
    DESCRIPTION: This test case verifies that the Cash Out messaging is not displayed in the Settled bet tab when Event is Not traded In-Play
    DESCRIPTION: When the Displayed status is No, Active status is S, Is OFF flag is N and cash out Flag is Y
    PRECONDITIONS: * User should place bet
    PRECONDITIONS: * Cash Out Messaging should be configured in CMS
    PRECONDITIONS: * In OB /TI make the below changes
    PRECONDITIONS: **Event Level**
    PRECONDITIONS: * Display status is  **No**
    PRECONDITIONS: * Active status is  **S**
    PRECONDITIONS: * Is OFF flag is  **N**
    PRECONDITIONS: * Cash out Flag is  **Y**
    """
    keep_browser_open = True

    def test_001_launch__ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch  Ladbrokes/Coral application
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

    def test_003_in_ob_make_the_changes_as_mentioned_in_the_pre_conditionsevent_level_display_status_is__no_active_status_is__s_is_off_flag_is__n_cash_out_flag_is__y(self):
        """
        DESCRIPTION: In OB make the changes as mentioned in the Pre-Conditions
        DESCRIPTION: **Event Level**
        DESCRIPTION: * Display status is  **No**
        DESCRIPTION: * Active status is  **S**
        DESCRIPTION: * Is OFF flag is  **N**
        DESCRIPTION: * Cash out Flag is  **Y**
        EXPECTED: 
        """
        pass

    def test_004_in_fe_navigate_to_my_bets_gt_open_bets(self):
        """
        DESCRIPTION: In FE navigate to My Bets &gt; Open Bets
        EXPECTED: * Cash Out Button should not be displayed
        EXPECTED: * Cash Out Messaging should be displayed as configured in CMS
        EXPECTED: * Find Out More Link should be displayed
        """
        pass

    def test_005_in_ob_settle_the_event(self):
        """
        DESCRIPTION: In OB settle the event
        EXPECTED: 
        """
        pass

    def test_006_navigate_to_my_bets_gt_settled_bets(self):
        """
        DESCRIPTION: Navigate to My Bets &gt; Settled Bets
        EXPECTED: * Cash Out Button should not be displayed
        EXPECTED: * Cash Out Messaging should not be displayed
        """
        pass
