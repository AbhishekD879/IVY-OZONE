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
class Test_C60011677_Verify_displaying_of_keypad_Multiples(Common):
    """
    TR_ID: C60011677
    NAME: Verify displaying of keypad  (Multiples)
    DESCRIPTION: Test case verifies displaying of keypad in expanded bet slip when bet slip contains several selections.
    PRECONDITIONS: Light Theme is enabled on tested device (Setting -> Display & Brightness -> Select "Light" theme)
    PRECONDITIONS: App installed and launched
    PRECONDITIONS: Bet slip contains several selections (more then 2)
    PRECONDITIONS: *Designs:*
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2aea0d688528346b808f0
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/dashboard?sid=5ea989452d8bd3bda177b7c0
    """
    keep_browser_open = True

    def test_001__expand_betslip(self):
        """
        DESCRIPTION: * Expand Betslip
        EXPECTED: * Betslip expnanded
        EXPECTED: * Greyed out 'Stake' input within the stake box is displayed
        EXPECTED: * The total stake and potential returns area is sticky when bet slip is expanded
        EXPECTED: Designs Coral/Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/120936843) ![](index.php?/attachments/get/120936844)
        """
        pass

    def test_002__tap_on_any_stake_field(self):
        """
        DESCRIPTION: * Tap on any stake field
        EXPECTED: * Bet slip remains expanded
        EXPECTED: * keypad will open and the background must automatically adjust to display the given selection in the center
        EXPECTED: * Stake field becomes active
        EXPECTED: * Must display 0 input in stake field without currency symbol
        EXPECTED: * Selections in background must be scrollable when keyboard is displayed
        EXPECTED: Designs Coral/Ladbrokes: (Light Theme)
        EXPECTED: ![](index.php?/attachments/get/120936852) ![](index.php?/attachments/get/120936853)
        """
        pass

    def test_003__enable__dark_theme__on_tested_devicesetting___display__brightness___select_dark_theme_verify_that_keypad_view_in_expanded_bet_slip_conforms_to_dark_theme_designs(self):
        """
        DESCRIPTION: * Enable  Dark Theme  on tested device
        DESCRIPTION: (Setting -> Display & Brightness -> Select "Dark" theme)
        DESCRIPTION: * Verify that keypad view in expanded Bet slip conforms to Dark theme designs
        EXPECTED: * Dark theme enabled
        EXPECTED: * keypad view in expanded Bet slip conforms to Dark theme designs
        EXPECTED: Designs Coral/Ladbrokes: (Dark Theme)
        EXPECTED: ![](index.php?/attachments/get/120936854) ![](index.php?/attachments/get/120936855)
        """
        pass

    def test_004__enter_the_value_of_the_stake_into_stake_field_eg10(self):
        """
        DESCRIPTION: * Enter the value of the stake into 'Stake' field (e.g.10)
        EXPECTED: * 'Stake' field must update to reflect the interaction with Keypad
        EXPECTED: * No currency symbol should be displayed across both brands in stake field
        """
        pass

    def test_005__tap_on_another_stake_field(self):
        """
        DESCRIPTION: * Tap on another 'Stake' field
        EXPECTED: * Bet slip remains expanded
        EXPECTED: * Tapped Stake field becomes active
        EXPECTED: * keypad will re-open and the background must automatically adjust to display the given selection in the center
        EXPECTED: * Must display 0 input in stake field without currency symbol
        EXPECTED: * Selections in background must be scrollable when keyboard is displayed
        """
        pass
