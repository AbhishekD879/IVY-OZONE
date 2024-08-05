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
class Test_C59925274_Betslip_collapsed_removal_of_selection(Common):
    """
    TR_ID: C59925274
    NAME: Betslip (collapsed) removal of selection
    DESCRIPTION: This test case verifies the possibility of removing selection by swiping in collapsed view.
    PRECONDITIONS: App is installed and launched:
    PRECONDITIONS: Designs:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5eac3790353e411c26318c12 - Ladbrokes
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2af35b74d2b5505416fbe - Coral
    """
    keep_browser_open = True

    def test_001__tap_on_any_selection(self):
        """
        DESCRIPTION: * Tap on any selection
        EXPECTED: * Collapsed betslip is opened.
        """
        pass

    def test_002__swip_selection_in_betslip_to_the_left(self):
        """
        DESCRIPTION: * Swip selection, in betslip, to the left.
        EXPECTED: "Remove" red button is shown.
        EXPECTED: ![](index.php?/attachments/get/119657445)
        """
        pass

    def test_003__tap_on_remove_button(self):
        """
        DESCRIPTION: * Tap on "Remove" button.
        EXPECTED: * Selection is removed.
        EXPECTED: * Betslip is closed.
        """
        pass

    def test_004__repeat_steps_1_3_for_suspended_selection(self):
        """
        DESCRIPTION: * Repeat steps 1-3 for Suspended selection
        EXPECTED: * Results from steps 1-3
        EXPECTED: * Suspended selection was successfully removed from BetSlip
        """
        pass
