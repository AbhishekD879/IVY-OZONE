import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59925275_Betslip_expanded_removal_of_selection(Common):
    """
    TR_ID: C59925275
    NAME: Betslip (expanded) removal of selection
    DESCRIPTION: This test case verifies the possibility of removing selection by swiping in expanded view.
    PRECONDITIONS: * App is installed and launched
    PRECONDITIONS: * Betslip is expanded with 2 selection added
    PRECONDITIONS: Designs:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5eac3790353e411c26318c12 - Ladbrokes
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2af35b74d2b5505416fbe - Coral
    """
    keep_browser_open = True

    def test_001_swipe_selection_in_betslip_to_the_left(self):
        """
        DESCRIPTION: Swipe selection, in betslip, to the left.
        EXPECTED: "Remove" red button is shown.
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/119657441)
        EXPECTED: ![](index.php?/attachments/get/119657442)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/119657443)
        EXPECTED: ![](index.php?/attachments/get/119657444)
        """
        pass

    def test_002_tap_on_remove_button(self):
        """
        DESCRIPTION: Tap on "Remove" button.
        EXPECTED: * Selection is removed.
        EXPECTED: * Betslip is closed.
        """
        pass

    def test_003__repeat_steps_1_2_for_suspended_selection(self):
        """
        DESCRIPTION: * Repeat steps 1-2 for Suspended selection
        EXPECTED: * Results from steps 1-2
        EXPECTED: * Suspended selection was successfully removed from BetSlip
        """
        pass
