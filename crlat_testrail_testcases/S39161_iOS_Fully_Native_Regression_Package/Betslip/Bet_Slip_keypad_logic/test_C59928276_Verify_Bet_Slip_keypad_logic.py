import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.native
@vtest
class Test_C59928276_Verify_Bet_Slip_keypad_logic(Common):
    """
    TR_ID: C59928276
    NAME: Verify Bet Slip keypad logic
    DESCRIPTION: This test case verifies Tapping on 'Stake' field in the bet slip
    PRECONDITIONS: Designs:
    PRECONDITIONS: https://zpl.io/2yZRxmw - Ladbrokes
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5eaa983ae1344bbac8b9f021 - Coral
    PRECONDITIONS: Example of max stake input - https://zpl.io/adJD9re
    PRECONDITIONS: Keypad Animation - https://coralracing.sharepoint.com/sites/NATIVEPROJECTDELIVERY/Shared%20Documents/General/03-Betslip%20Optimisation/Ladbrokes/03-Prototypes/ladbrokes-single-selection.mp4
    """
    keep_browser_open = True

    def test_001___add_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: - Add selection to the bet slip
        EXPECTED: - Selection is added to the Betslip
        EXPECTED: - Betslip is collapsed
        EXPECTED: - Greyed out 'Stake' input within the stake box is displayed
        EXPECTED: Light mode 'Stake' input:
        EXPECTED: ![](index.php?/attachments/get/119601884)
        EXPECTED: Dark mode 'Stake' input:
        EXPECTED: ![](index.php?/attachments/get/119601885)
        """
        pass

    def test_002___tap_on_stake_field(self):
        """
        DESCRIPTION: - Tap on 'Stake' field
        EXPECTED: - Bet slip is expanded to display keyboard as per designs including animation
        EXPECTED: - Must display 0 input in stake field without currency symbol
        EXPECTED: Designs:
        EXPECTED: Ladbrokes:
        EXPECTED: light mode
        EXPECTED: ![](index.php?/attachments/get/119601886)
        EXPECTED: dark mode:
        EXPECTED: ![](index.php?/attachments/get/119601887)
        EXPECTED: Coral:
        EXPECTED: light mode:
        EXPECTED: ![](index.php?/attachments/get/119601888)
        EXPECTED: dark mode:
        EXPECTED: ![](index.php?/attachments/get/119601889)
        """
        pass

    def test_003___enter_the_value_of_the_stake_into_stake_field(self):
        """
        DESCRIPTION: - Enter the value of the stake into 'Stake' field
        EXPECTED: - 'Stake' field must update to reflect the interaction with Keyboard
        """
        pass

    def test_004___verify_keypad_animation(self):
        """
        DESCRIPTION: - Verify keypad animation
        EXPECTED: Animation:
        EXPECTED: https://coralracing.sharepoint.com/sites/NATIVEPROJECTDELIVERY/Shared%20Documents/General/03-Betslip%20Optimisation/Ladbrokes/03-Prototypes/ladbrokes-single-selection.mp4
        """
        pass
