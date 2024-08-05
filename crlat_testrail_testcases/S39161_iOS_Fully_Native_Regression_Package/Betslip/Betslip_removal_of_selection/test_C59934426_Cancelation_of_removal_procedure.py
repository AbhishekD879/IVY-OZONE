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
class Test_C59934426_Cancelation_of_removal_procedure(Common):
    """
    TR_ID: C59934426
    NAME: Cancelation of removal procedure
    DESCRIPTION: This test case verifies the cancelation of removal procedure
    PRECONDITIONS: App is installed and launched:
    PRECONDITIONS: Designs:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5eac3790353e411c26318c12 - Ladbrokes
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2af35b74d2b5505416fbe - Coral
    """
    keep_browser_open = True

    def test_001_tap_on_any_selection(self):
        """
        DESCRIPTION: Tap on any selection.
        EXPECTED: Collapsed betslip is opened.
        """
        pass

    def test_002_swipe_the_selection_to_the_left_in_the_betslip(self):
        """
        DESCRIPTION: Swipe the selection to the left in the betslip.
        EXPECTED: "Remove" button appears.
        """
        pass

    def test_003_swip_the_selection_to_the_right(self):
        """
        DESCRIPTION: Swip the selection to the right.
        EXPECTED: "Remove" button disappears.
        """
        pass

    def test_004_expand_the_betslip(self):
        """
        DESCRIPTION: Expand the betslip.
        EXPECTED: Betslip is expanded.
        """
        pass

    def test_005_swipe_the_selection_to_the_left_in_the_betslip(self):
        """
        DESCRIPTION: Swipe the selection to the left in the betslip.
        EXPECTED: "Remove" button appears
        """
        pass

    def test_006_swipe_the_selection_to_the_right(self):
        """
        DESCRIPTION: Swipe the selection to the right.
        EXPECTED: "Remove" button disappears.
        """
        pass
