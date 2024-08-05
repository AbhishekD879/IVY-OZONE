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
class Test_C62764584_Verify_the_Cash_Out_Messaging_When_Events_are_not_traded_In_Play_for_ACCA_bets(Common):
    """
    TR_ID: C62764584
    NAME: Verify the Cash Out Messaging- When Events are not traded In Play for ACCA bets
    DESCRIPTION: This test case verifies the display of Cash Out messaging & Find Out More link when Event is not traded In Play
    DESCRIPTION: When the Displayed status is No, Active status is S, Is OFF flag is N and cash out Flag is Y
    PRECONDITIONS: * User should place ACCA bet which has Cash Out
    PRECONDITIONS: * Cash Out Messaging should be configured in CMS
    PRECONDITIONS: * In OB /TI make the below changes
    PRECONDITIONS: * Display status is  **No**
    PRECONDITIONS: * Active status is  **S**
    PRECONDITIONS: * Is OFF flag is  **N**
    PRECONDITIONS: * Cash out Flag is  **Y**
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

    def test_003__in_ob_make_the_changes_as_mentioned_in_pre_conditions_for_any_one_of_the_selection_in_the_acca_bet_display_status_is_no_active_status_is_s_is_off_flag_is_n_cash_out_flag_is_yselection_in_event_has_passed_the_event_start_time_ie_start_time__20210729_1100_and_load_time_is_210729_1110(self):
        """
        DESCRIPTION: * In OB make the changes as mentioned in Pre-Conditions for any ONE of the selection in the ACCA bet
        DESCRIPTION: * Display status is **No**
        DESCRIPTION: * Active status is **S**
        DESCRIPTION: * Is OFF flag is **N**
        DESCRIPTION: * Cash out Flag is **Y**
        DESCRIPTION: Selection in event has passed the event start time ie start time = 2021/07/29 11:00 and load time is 21/07/29 11:10
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
        EXPECTED: * Bet should not be displayed in Cash Out bets
        """
        pass

    def test_007_repeat_for_two_or_more_selections_in_the_bet_and_validate_the_message_content_in_the_pop_up(self):
        """
        DESCRIPTION: Repeat for two or more selections in the bet and validate the message content in the pop-up
        EXPECTED: * Cash Out Button should not be displayed
        EXPECTED: * Cash Out Messaging should be displayed as configured in CMS
        EXPECTED: * Find Out More Link should be displayed
        EXPECTED: **On Clicking Find Out More Link**
        EXPECTED: * Message Pop-up should be displayed
        EXPECTED: * Message pop up with events (which causing cash out button removed) and Got it button
        """
        pass
