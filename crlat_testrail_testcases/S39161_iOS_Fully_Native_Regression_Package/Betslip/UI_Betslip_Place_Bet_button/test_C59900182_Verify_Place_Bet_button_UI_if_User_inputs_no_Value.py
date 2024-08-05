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
class Test_C59900182_Verify_Place_Bet_button_UI_if_User_inputs_no_Value(Common):
    """
    TR_ID: C59900182
    NAME: Verify Place Bet button UI if User inputs no Value
    DESCRIPTION: Test case verifies 'Place Bet' button in case if User inputs no Value
    PRECONDITIONS: - The app is installed and launched
    PRECONDITIONS: - User is logged in to the Application
    PRECONDITIONS: Designs:
    PRECONDITIONS: Ladbrokes: https://zpl.io/a3BJ7kW
    PRECONDITIONS: Coral: https://zpl.io/brZOn05
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is added to the Betslip
        """
        pass

    def test_002_expand_betslip(self):
        """
        DESCRIPTION: Expand Betslip
        EXPECTED: - The Betslip is expanded
        EXPECTED: - Keyboard is in view
        EXPECTED: - No one value is inputed
        """
        pass

    def test_003_verify_that_place_bet_button_is_in_view_but_inactiv(self):
        """
        DESCRIPTION: Verify that 'Place bet' button is in view but inactiv
        EXPECTED: 'Place bet' button is in view but inactive as per designs:
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/118935551)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/118935552)
        """
        pass

    def test_004_add_one_more_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add one more selection to the Betslip
        EXPECTED: Selection is added to the Betslip
        """
        pass

    def test_005_repeat_step_2_3_with_2_or_more_selections_in_the_betslip(self):
        """
        DESCRIPTION: Repeat step 2-3 with 2 or more selections in the Betslip
        EXPECTED: 'Place bet' button is in view but inactive as per designs:
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/118935555)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/118935556)
        """
        pass
