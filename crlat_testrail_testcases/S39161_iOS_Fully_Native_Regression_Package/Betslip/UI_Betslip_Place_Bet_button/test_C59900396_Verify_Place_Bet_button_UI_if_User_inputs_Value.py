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
class Test_C59900396_Verify_Place_Bet_button_UI_if_User_inputs_Value(Common):
    """
    TR_ID: C59900396
    NAME: Verify Place Bet button UI if User inputs Value
    DESCRIPTION: Test case verifies 'Place Bet' button in case if User inputs Value
    PRECONDITIONS: - The app is installed and launched
    PRECONDITIONS: - User is logged in to the Application
    PRECONDITIONS: Designs:
    PRECONDITIONS: Ladbrokes: https://zpl.io/VD03r5v
    PRECONDITIONS: Coral: https://zpl.io/V0BOGeO
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
        EXPECTED: The Betslip is expanded
        EXPECTED: Keyboard is in view
        """
        pass

    def test_003_enter_any_value_into_stake_field(self):
        """
        DESCRIPTION: Enter any value into 'Stake' field
        EXPECTED: Stake value is inputed
        """
        pass

    def test_004_verify_place_bet_button(self):
        """
        DESCRIPTION: Verify 'Place bet' button
        EXPECTED: 'Place bet' CTA is in view and active as per designs:
        EXPECTED: Coral:
        EXPECTED: TO ADD after Design updating
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/119064574)
        """
        pass

    def test_005_add_one_more_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add one more selection to the Betslip
        EXPECTED: Selection is added to the Betslip
        """
        pass

    def test_006_repeat_step_2_4_with_2_or_more_selections_in_the_betslip(self):
        """
        DESCRIPTION: Repeat step 2-4 with 2 or more selections in the Betslip
        EXPECTED: 'Place bet' CTA is in view and active as per designs:
        EXPECTED: Coral:
        EXPECTED: Correct Design is not provided
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/119064574)
        """
        pass
