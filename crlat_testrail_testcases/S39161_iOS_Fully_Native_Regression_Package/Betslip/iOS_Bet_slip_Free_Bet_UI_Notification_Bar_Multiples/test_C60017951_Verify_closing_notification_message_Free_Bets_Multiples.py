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
class Test_C60017951_Verify_closing_notification_message_Free_Bets_Multiples(Common):
    """
    TR_ID: C60017951
    NAME: Verify closing notification message (Free Bets)  (Multiples)
    DESCRIPTION: Test case verifies ability to close notification message(Free Bets) when bet slip expanded (Multiples)
    PRECONDITIONS: Install native app
    PRECONDITIONS: Open the app
    PRECONDITIONS: User is on Home page
    PRECONDITIONS: User has Free bets
    PRECONDITIONS: Bet slip contains several selections (more than 2, e.g.: 5 selections)
    PRECONDITIONS: Bet slip collapsed
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2b112b404f05777b64a74
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea99a2471f61ebb869f0445
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
        EXPECTED: * Notification message about Free Bets closed
        """
        pass

    def test_003__collapse__expand_bet_slip(self):
        """
        DESCRIPTION: * Collapse / Expand bet slip
        EXPECTED: * Bet slip is expanded
        EXPECTED: * Notification message about Free Bets is not displayed
        """
        pass

    def test_004__remove_selections_from_bet_slip_kill_the_app(self):
        """
        DESCRIPTION: * Remove selections from bet slip
        DESCRIPTION: * Kill the app
        EXPECTED: * selections removed
        EXPECTED: * App killed
        """
        pass

    def test_005__open_app_add_the_same_selections_to_bet_slip_expand_betslip(self):
        """
        DESCRIPTION: * Open App
        DESCRIPTION: * Add the same selections to bet slip
        DESCRIPTION: * Expand betslip
        EXPECTED: * App opened
        EXPECTED: * Selections were added to bet slip
        EXPECTED: * bet slip expanded
        EXPECTED: * notification message about Free Bets displays along top of the bet slip with close option
        """
        pass

    def test_006__tap_on_use_free_bet_button_on_any_available_selection_coral__ladbrokesindexphpattachmentsget121005885_indexphpattachmentsget121005886(self):
        """
        DESCRIPTION: * Tap on "Use Free Bet" button on any available selection
        DESCRIPTION: * Coral / Ladbrokes:
        DESCRIPTION: ![](index.php?/attachments/get/121005885) ![](index.php?/attachments/get/121005886)
        EXPECTED: * Notification message about Free Bets closes automatically
        EXPECTED: * free bet overlay which lists all the free bets available for user to use is opened
        """
        pass

    def test_007__close_free_bet_overlay_and_collapse_bet_slip(self):
        """
        DESCRIPTION: * Close free bet overlay and collapse bet slip
        EXPECTED: * Free bet overlay
        EXPECTED: * Bets lip collapsed
        EXPECTED: * Notification message about Free Bets is not displayed
        """
        pass

    def test_008__expand_bet_slip(self):
        """
        DESCRIPTION: * Expand bet slip
        EXPECTED: * Bets lip is expanded with single selection
        EXPECTED: * Notification message about Free Bets is not displayed
        """
        pass
