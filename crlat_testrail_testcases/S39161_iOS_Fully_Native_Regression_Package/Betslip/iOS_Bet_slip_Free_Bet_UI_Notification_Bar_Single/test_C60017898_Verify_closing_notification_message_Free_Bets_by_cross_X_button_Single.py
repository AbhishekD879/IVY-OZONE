import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C60017898_Verify_closing_notification_message_Free_Bets_by_cross_X_button_Single(Common):
    """
    TR_ID: C60017898
    NAME: Verify closing notification message (Free Bets) by cross ('X') button (Single)
    DESCRIPTION: Test case verifies ability to close notification message (Free Bets) by cross button 'X'.
    PRECONDITIONS: App installed and opened
    PRECONDITIONS: User is on Home page
    PRECONDITIONS: Bet slip collapsed and contains 1 selection
    PRECONDITIONS: Coral design: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/dashboard?sid=5eaa983ae1344bbac8b9f021
    PRECONDITIONS: Ladbrokes design: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/dashboard?sid=5ea97d244f68f62598af7515
    """
    keep_browser_open = True

    def test_001__expand_bet_slip(self):
        """
        DESCRIPTION: * Expand bet slip
        EXPECTED: * Bet slip expanded with selected selection
        EXPECTED: * notification message about Free Bets displays along top of the bet slip with close option
        """
        pass

    def test_002__tap_on_cross_button_on_notification_message_about_free_bets(self):
        """
        DESCRIPTION: * Tap on cross button on notification message about Free Bets
        EXPECTED: * Notification message about Free Bets closes
        """
        pass

    def test_003__collapse_bet_slip(self):
        """
        DESCRIPTION: * Collapse bet slip
        EXPECTED: * Bet slip collapsed
        EXPECTED: * Notification message about Free Bets is not displayed
        """
        pass

    def test_004__expand_bet_slip(self):
        """
        DESCRIPTION: * Expand bet slip
        EXPECTED: * Bet slip is expanded with current single selection
        EXPECTED: * Notification message about Free Bets is not displayed
        """
        pass

    def test_005__remove_selection_from_bet_slip_kill_the_app(self):
        """
        DESCRIPTION: * Remove selection from bet slip
        DESCRIPTION: * Kill the app
        EXPECTED: * selection removed
        EXPECTED: * App killed
        """
        pass

    def test_006__open_app_add_the_same_selection_to_bet_slip_expand_betslip(self):
        """
        DESCRIPTION: * Open App
        DESCRIPTION: * Add the same selection to bet slip
        DESCRIPTION: * Expand betslip
        EXPECTED: * App opened
        EXPECTED: * Selection was added to bet slip
        EXPECTED: * bet slip expanded
        EXPECTED: * notification message about Free Bets displays along top of the bet slip with close option
        """
        pass
