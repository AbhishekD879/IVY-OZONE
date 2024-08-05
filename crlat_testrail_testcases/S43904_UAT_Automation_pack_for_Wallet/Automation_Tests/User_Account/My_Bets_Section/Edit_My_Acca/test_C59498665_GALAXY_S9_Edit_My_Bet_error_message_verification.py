import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C59498665_GALAXY_S9_Edit_My_Bet_error_message_verification(Common):
    """
    TR_ID: C59498665
    NAME: [GALAXY S9] Edit My Bet error message verification
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001___________1_create_events__________2_login_into_app__________3_place_multiple_bet__________4_navigate_to_the_bet_history__________5_go_to_open_bets_tab___verify_that_edit_my_bet_button_is_available(self):
        """
        DESCRIPTION: *          1. Create events
        DESCRIPTION: *          2. Login into App
        DESCRIPTION: *          3. Place Multiple bet
        DESCRIPTION: *          4. Navigate to the Bet History
        DESCRIPTION: *          5. Go to 'Open Bets' tab -> verify that Edit My Bet button is available
        EXPECTED: *
        """
        pass

    def test_002___________remove_few_selections_from_the_bet(self):
        """
        DESCRIPTION: *          Remove few selections from the bet
        EXPECTED: *          'UNDO' button is shown for removed selections
        EXPECTED: *          'CONFIRM' button is shown and enabled
        EXPECTED: *          Stake and Est. Returns are updated
        """
        pass

    def test_003___________tap_confirm_button__________in_the_same_time_suspend_any_eventmarketselection_from_the_bet_in_ti__________verify_that_new_bet_is_not_placed__________verify_that_edit_mode_is_opened_with_an_error_message(self):
        """
        DESCRIPTION: *          Tap 'CONFIRM' button
        DESCRIPTION: *          In the same time suspend any event/market/selection from the bet in TI
        DESCRIPTION: *          Verify that new bet is NOT placed;
        DESCRIPTION: *          Verify that edit mode is opened with an error message
        EXPECTED: *          Edit mode is shown with appropriate elements:
        EXPECTED: *          Error Message: "text from CMS"
        EXPECTED: *          'SUSPENDED' label and disabled 'Selection Removal' button for suspended selections
        EXPECTED: *          Disabled 'Selection Removal' buttons for all selections
        EXPECTED: *          New Stake and New Est. Returns
        EXPECTED: *          'CONFIRM' button is disabled
        EXPECTED: *          'CANCEL EDITING' is enabled
        """
        pass

    def test_004___________verify_the_pop_up_msg(self):
        """
        DESCRIPTION: *          Verify the pop up msg
        EXPECTED: *          Leave the EMB page  before confirming EMB, pop up msg should be displayed.
        EXPECTED: *          Note: Do you want to cancel editing msg should be displayed.
        """
        pass
