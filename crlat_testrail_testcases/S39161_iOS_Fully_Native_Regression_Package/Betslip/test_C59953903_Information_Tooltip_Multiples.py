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
class Test_C59953903_Information_Tooltip_Multiples(Common):
    """
    TR_ID: C59953903
    NAME: Information Tooltip (Multiples)
    DESCRIPTION: This test case verifies appearence information icon about each of the different bet types.
    PRECONDITIONS: * Application is installed and launched
    PRECONDITIONS: Test designs:
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2ae62315c95838ed2c0cf
    PRECONDITIONS: Ladbokes: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea989664ac83325cfa54439
    """
    keep_browser_open = True

    def test_001_select_two_selections_from_different_events_and_expand_the_betslip(self):
        """
        DESCRIPTION: Select two selections from different events and expand the Betslip
        EXPECTED: * Selections are added.
        EXPECTED: * Betslip is opened.
        EXPECTED: * Information icon "i" is placed next to "Accumulator bet" area
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/120241984)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/120241993)
        """
        pass

    def test_002_tap_on_information_icon(self):
        """
        DESCRIPTION: Tap on Information icon.
        EXPECTED: * Explanation pop-up message is shown:
        EXPECTED: * "Find out more" button is displayed.
        EXPECTED: * "Close" button is displayed
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/120241990)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/120241991)
        """
        pass

    def test_003_tap_on_close_button(self):
        """
        DESCRIPTION: Tap on "Close" button
        EXPECTED: * Pop up is closed.
        EXPECTED: * Betslip remains opened.
        """
        pass

    def test_004__repeat_12_steps(self):
        """
        DESCRIPTION: * Repeat 1,2 steps.
        EXPECTED: * Explanation pop-up message is shown:
        EXPECTED: * "Find out more" button is displayed.
        EXPECTED: * "Close" button is displayed
        """
        pass

    def test_005_tap_on_find_our_more_button(self):
        """
        DESCRIPTION: Tap on "Find our more" button.
        EXPECTED: User is redirected to the appropriate page
        """
        pass
