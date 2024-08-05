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
class Test_C60017952_Verify_displaying_notification_messageFree_Bets_in_pair_with_other_notifications(Common):
    """
    TR_ID: C60017952
    NAME: Verify displaying notification message(Free Bets) in pair with other notifications
    DESCRIPTION: Test case verifies displaying of notification message(Free Bets) in pair with other notifications
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
        EXPECTED: * Bet slip expanded with selected selections
        EXPECTED: * notification message about Free Bets displays along top of the bet slip with close option
        """
        pass

    def test_002__trigger_at_the_same_moment_odds_change_for_any_of_addedselectionsdata_will_be_mocked_for_ui_testing_until__backend_set_up_coral__ladbrokesindexphpattachmentsget121005892_indexphpattachmentsget121005893(self):
        """
        DESCRIPTION: * Trigger at the same moment Odds change for any of added
        DESCRIPTION: selections
        DESCRIPTION: (***Data will be mocked for UI testing until  backend set up )
        DESCRIPTION: Coral / Ladbrokes:
        DESCRIPTION: ![](index.php?/attachments/get/121005892) ![](index.php?/attachments/get/121005893)
        EXPECTED: * Notification about Odds change displays along top of the bet slip with close option
        """
        pass

    def test_003__verify_correctness_of_displaying_2_notifications_verify_that_displaying_of_2_notifications_in_expanded_bet_slip_conforms_to_next_principle_notifications_display_one_under_another_and_not_overlapping_each_otherindexphpattachmentsget121005894(self):
        """
        DESCRIPTION: * Verify correctness of displaying 2 notifications
        DESCRIPTION: * Verify that displaying of 2 notifications in expanded bet slip conforms to next principle (notifications display one under another and not overlapping each other):
        DESCRIPTION: ![](index.php?/attachments/get/121005894)
        EXPECTED: * 2 notifications correclty displays in expanded bet slip and displaying conforms to the principle (notifications display one under another and not overlapping each other)
        """
        pass
