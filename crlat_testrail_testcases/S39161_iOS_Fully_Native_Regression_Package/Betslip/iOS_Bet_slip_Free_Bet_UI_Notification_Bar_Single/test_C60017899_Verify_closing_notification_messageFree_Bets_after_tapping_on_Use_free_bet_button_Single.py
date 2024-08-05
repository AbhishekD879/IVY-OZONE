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
class Test_C60017899_Verify_closing_notification_messageFree_Bets_after_tapping_on_Use_free_bet_button_Single(Common):
    """
    TR_ID: C60017899
    NAME: Verify closing notification message(Free Bets) after tapping on  "Use free bet" button (Single)
    DESCRIPTION: Test case verifies ability to close notification message (Free Bets) by tapping on "Use free bet" button
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

    def test_002__tap_on_use_free_bet_button_coral__ladbrokesindexphpattachmentsget119425536_indexphpattachmentsget119425535(self):
        """
        DESCRIPTION: * Tap on "Use Free Bet" button
        DESCRIPTION: * Coral / Ladbrokes:
        DESCRIPTION: ![](index.php?/attachments/get/119425536) ![](index.php?/attachments/get/119425535)
        EXPECTED: * Notification message about Free Bets closes automatically
        EXPECTED: * free bet overlay which lists all the free bets available for user to use is opened
        """
        pass

    def test_003__close_free_bet_overlay_and_collapse_bet_slip(self):
        """
        DESCRIPTION: * Close free bet overlay and collapse bet slip
        EXPECTED: * Free bet overlay closed
        EXPECTED: * Bets lip collapsed
        EXPECTED: * Notification message about Free Bets is not displayed
        """
        pass

    def test_004__expand_bet_slip(self):
        """
        DESCRIPTION: * Expand bet slip
        EXPECTED: * Bets lip is expanded with  single selection
        EXPECTED: * Notification message about Free Bets is not displayed
        """
        pass
