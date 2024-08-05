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
class Test_C62162276_Verify_Cash_Out_Messaging_Market_is_not_traded_for_In_Play(Common):
    """
    TR_ID: C62162276
    NAME: Verify Cash Out Messaging-Market is not traded for In-Play
    DESCRIPTION: This test case verifies the display of Cash Out messaging & Find Out More link when Market is not traded for In-Play
    DESCRIPTION: Event - Display status is Y, Active status is A, Is OFF Flag is Y and cash out Flag is Y for event
    DESCRIPTION: Market -Display status is N, Active status is S and Cash out Flag is Y for Market
    PRECONDITIONS: * User should place bet which has Cash Out
    PRECONDITIONS: * Cash Out Messaging should be configured in CMS
    PRECONDITIONS: * In OB /TI make the below changes
    PRECONDITIONS: **Event Level**
    PRECONDITIONS: Event - Display status is **Y**, Active status is **A**, Is OFF Flag is **Y** and cash out Flag is **Y**
    PRECONDITIONS: **Market Level**
    PRECONDITIONS: Market -Display status is **N**, Active status is **S** and Cash out Flag is **Y**
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

    def test_003_in_ob_make_the_changes_as_mentioned_in_the_pre_conditionsevent_levelevent___display_status_is_y_active_status_is_a_is_off_flag_is_y_and_cash_out_flag_is_ymarket_levelmarket__display_status_is_n_active_status_is_s_and_cash_out_flag_is_y(self):
        """
        DESCRIPTION: In OB make the changes as mentioned in the Pre-Conditions
        DESCRIPTION: **Event Level**
        DESCRIPTION: Event - Display status is **Y**, Active status is **A**, Is OFF Flag is **Y** and cash out Flag is **Y**
        DESCRIPTION: **Market Level**
        DESCRIPTION: Market -Display status is **N**, Active status is **S** and Cash out Flag is **Y**
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

    def test_005_click_on_find_out_more_link(self):
        """
        DESCRIPTION: Click on Find Out More link
        EXPECTED: * Message Pop-up should be displayed
        EXPECTED: * Message pop up with events (which causing cash out button removed) and Got it button
        """
        pass

    def test_006_only_coralnavigate_to_my_bets_gt_cash_out_bets(self):
        """
        DESCRIPTION: **ONLY CORAL**
        DESCRIPTION: Navigate to My Bets &gt; Cash Out Bets
        EXPECTED: Bet should be displayed in Cash Out bets
        """
        pass
