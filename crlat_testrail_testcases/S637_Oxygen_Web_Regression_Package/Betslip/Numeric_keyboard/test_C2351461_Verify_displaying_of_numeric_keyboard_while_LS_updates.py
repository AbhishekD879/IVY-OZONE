import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C2351461_Verify_displaying_of_numeric_keyboard_while_LS_updates(Common):
    """
    TR_ID: C2351461
    NAME: Verify displaying of numeric keyboard while LS updates
    DESCRIPTION: This test case verifies displaying of numeric keyboard while Live Serve updates
    DESCRIPTION: Applies for Mobile only
    DESCRIPTION: AUTOTEST: [C9698227]
    DESCRIPTION: Note: On OX100 Key pad should not open by default BMA-45311
    PRECONDITIONS: Application is loaded on Mobile device
    """
    keep_browser_open = True

    def test_001_add_one_selection_to_the_betslip__open_betslip(self):
        """
        DESCRIPTION: Add one selection to the Betslip > Open Betslip
        EXPECTED: - Betslip is opened
        EXPECTED: - One selection is available within Betslip
        EXPECTED: **Before OX99**
        EXPECTED: - Stake box is focused <currency symbol>0.00 is shown within box
        EXPECTED: - The numeric keyboard is displayed
        EXPECTED: **After OX101**
        EXPECTED: - 'Stake' box is NOT focused
        EXPECTED: - The numeric keyboard is NOT displayed
        """
        pass

    def test_002_for_ox101tap_on_stake_field(self):
        """
        DESCRIPTION: **For OX101**
        DESCRIPTION: Tap on 'Stake' field
        EXPECTED: - 'Stake' box is focused
        EXPECTED: - The numeric keyboard is displayed
        """
        pass

    def test_003_in_ob_backoffice_trigger_suspension_for_a_selection_from_betslip(self):
        """
        DESCRIPTION: In OB Backoffice trigger suspension for a selection from Betslip
        EXPECTED: **Before OX99**
        EXPECTED: - Error messages are displayed
        EXPECTED: - 'Stake' box is NOT focused and '<currency symbol> 0.00' is shown within box
        EXPECTED: - Numeric keyboard is NOT displayed
        EXPECTED: **After OX99**
        EXPECTED: - Selection is greyed out
        EXPECTED: - Appropriate message for suspension is shown
        EXPECTED: - Only Ladbrokes: Message for suspension is shown at the top of Betslip for 5s
        EXPECTED: - 'Stake' box is NOT focused and 'Stake' is shown within box
        """
        pass

    def test_004_in_ob_backoffice_trigger_return_selection_from_step_2_to_active_state(self):
        """
        DESCRIPTION: In OB Backoffice trigger return selection (from step 2) to active state
        EXPECTED: **Before OX99**
        EXPECTED: - Error messages are NOT displayed
        EXPECTED: - 'Stake' box becomes focused and '<currency symbol>' is shown within box
        EXPECTED: - Numeric keyboard is shown
        EXPECTED: **After OX99**
        EXPECTED: - Selection become active
        EXPECTED: - Appropriate message for suspension is NOT shown
        EXPECTED: - 'Stake' box becomes focused and '<currency symbol>' is shown within box
        EXPECTED: - Numeric keyboard is shown
        EXPECTED: **After OX101**
        EXPECTED: - 'Stake' box is NOT focused
        EXPECTED: - Numeric keyboard is NOT shown
        """
        pass

    def test_005_for_ox101tap_on_stake_field(self):
        """
        DESCRIPTION: **For OX101**
        DESCRIPTION: Tap on 'Stake' field
        EXPECTED: - 'Stake' box is focused
        EXPECTED: - The numeric keyboard is displayed
        """
        pass

    def test_006_in_ob_backoffice_trigger_price_change_for_a_selection_from_betslip(self):
        """
        DESCRIPTION: In OB Backoffice trigger price change for a selection from Betslip
        EXPECTED: **Before OX99**
        EXPECTED: - New odds are displayed near old values
        EXPECTED: - Warning message is displayed
        EXPECTED: - 'Stake' box remains focused and '<currency symbol>' is shown within box
        EXPECTED: - Numeric keyboard is shown
        EXPECTED: **After OX99**
        EXPECTED: - Message for price change is shown above the selection
        EXPECTED: - Warning message is shown at the bottom of Betslip
        EXPECTED: - Only Ladbrokes: Message for Price change is shown at the top of Betslip for 5s
        EXPECTED: - 'Stake' box remains focused
        EXPECTED: -  Numeric keyboard is shown
        """
        pass

    def test_007_add_other_selections_to_the_betslip__open_betslip(self):
        """
        DESCRIPTION: Add other selections to the Betslip > Open Betslip
        EXPECTED: - Betslip is opened
        EXPECTED: - Added selections are available within Betslip
        EXPECTED: - Numeric keyboard is NOT displayed
        """
        pass

    def test_008_set_focus_on_any_stake_field(self):
        """
        DESCRIPTION: Set focus on any 'Stake' field
        EXPECTED: - 'Stake' box becomes focused
        EXPECTED: - Numeric keyboard is shown
        """
        pass

    def test_009_in_ob_backoffice_trigger_suspension_for_a_selection_with_focused_stake_field_from_step_8_from_betslip(self):
        """
        DESCRIPTION: In OB Backoffice trigger suspension for a selection with focused 'Stake' field (from step 8) from Betslip
        EXPECTED: **Before OX99:**
        EXPECTED: - Error messages are displayed
        EXPECTED: - 'Stake' box is NOT focused and '<currency symbol> 0.00' is shown within box
        EXPECTED: - Numeric keyboard is NOT displayed
        EXPECTED: **After OX99**
        EXPECTED: - Selection is greyed out
        EXPECTED: - Appropriate message for suspension is shown
        EXPECTED: - Only Ladbrokes: Message for suspension is shown at the top of Betslip for 5s
        EXPECTED: - 'Stake' box is NOT focused and 'Stake' is shown within box
        EXPECTED: - Numeric keyboard is NOT displayed
        """
        pass

    def test_010_in_ob_backoffice_trigger_return_selection_from_step_6_to_active_state(self):
        """
        DESCRIPTION: In OB Backoffice trigger return selection (from step 6) to active state
        EXPECTED: - Previously selected 'Stake' box is no longer focused
        EXPECTED: - Numeric keyboard does not appear
        """
        pass

    def test_011_set_focus_on_any_stake_field(self):
        """
        DESCRIPTION: Set focus on any 'Stake' field
        EXPECTED: - 'Stake' box becomes focused
        EXPECTED: - Numeric keyboard is shown
        """
        pass

    def test_012_in_ob_backoffice_trigger_price_change_for_a_selection_with_focused_stake_box_from_step_9(self):
        """
        DESCRIPTION: In OB Backoffice trigger price change for a selection with focused 'Stake' box (from step 9)
        EXPECTED: **Before OX99:**
        EXPECTED: - New odds are displayed near old values
        EXPECTED: - Warning message is displayed
        EXPECTED: - 'Stake' box remains focused and '<currency symbol>' is shown within box
        EXPECTED: - Numeric keyboard is shown
        EXPECTED: **After OX99**
        EXPECTED: - Message for price change is shown above the selection
        EXPECTED: - Warning message is shown at the bottom of Betslip
        EXPECTED: - Only Ladbrokes: Message for Price change is shown at the top of Betslip for 5s
        EXPECTED: - 'Stake' box remains focused
        EXPECTED: - Numeric keyboard is shown
        """
        pass
