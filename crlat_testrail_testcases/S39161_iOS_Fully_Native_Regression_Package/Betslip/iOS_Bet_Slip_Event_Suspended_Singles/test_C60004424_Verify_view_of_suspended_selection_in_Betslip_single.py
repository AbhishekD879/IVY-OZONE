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
class Test_C60004424_Verify_view_of_suspended_selection_in_Betslip_single(Common):
    """
    TR_ID: C60004424
    NAME: Verify view of suspended selection in Betslip (single)
    DESCRIPTION: Test case verifies view of suspended selection in  BetSlip
    PRECONDITIONS: Light Theme is enabled on tested device (Setting -> Display & Brightness -> Select "Light" theme)
    PRECONDITIONS: Install the app
    PRECONDITIONS: App is opened
    PRECONDITIONS: BetSlip is empty
    PRECONDITIONS: Design:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2a4647b7dbf551708872f
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea97d562bc36f2375a71eca
    """
    keep_browser_open = True

    def test_001__add_any_single_selection_to_betslip(self):
        """
        DESCRIPTION: * Add any single selection to BetSlip
        EXPECTED: * Selection was successfully added to BetSlip
        EXPECTED: * BetSlip is collapsed
        """
        pass

    def test_002__wait_until_current_selection_will_be_suspended(self):
        """
        DESCRIPTION: * Wait until current selection will be suspended
        EXPECTED: * Selection was suspended
        EXPECTED: * BetSlip is collapsed
        EXPECTED: * "Match suspended" message is not displayed in collapsed BetSlip
        """
        pass

    def test_003__expand_betslip_with_current_selection(self):
        """
        DESCRIPTION: * Expand BetSlip with current selection
        EXPECTED: * BetSlip is expanded
        EXPECTED: * "Match suspended" message is displayed in expanded BetSlip
        EXPECTED: * Keyboard is greyed
        EXPECTED: * "Place bet" button should update to show "BETTING SUSPENDED"
        EXPECTED: * Customer cannot place bet on suspended selection
        EXPECTED: * BetSlip view conforms to Coral/ Ladbrokes Light theme designs
        EXPECTED: Coral / Ladbrokes designs:
        EXPECTED: ![](index.php?/attachments/get/120826010) ![](index.php?/attachments/get/120826011)
        """
        pass

    def test_004__collapse_betslip(self):
        """
        DESCRIPTION: * Collapse Betslip
        EXPECTED: * BetSlip collapsed
        EXPECTED: * "Match suspended" message is not displayed in collapsed BetSlip
        """
        pass

    def test_005__enable_dark_theme_on_device(self):
        """
        DESCRIPTION: * Enable "Dark" theme on device
        EXPECTED: * "Dark" theme on device is enabled
        EXPECTED: * BetSlip is collapsed
        EXPECTED: * "Match suspended" message is not displayed in collapsed BetSlip
        """
        pass

    def test_006__expand_betslip_with_current_selection(self):
        """
        DESCRIPTION: * Expand BetSlip with current selection
        EXPECTED: * BetSlip is expanded
        EXPECTED: * "Match suspended" message is displayed in expanded BetSlip
        EXPECTED: * Keyboard is greyed
        EXPECTED: * "Place bet" button should update to show "BETTING SUSPENDED"
        EXPECTED: * Customer cannot place bet on suspended selection
        EXPECTED: * BetSlip view conforms to Coral/ Ladbrokes Dark theme designs
        EXPECTED: Coral / Ladbrokes designs:
        EXPECTED: ![](index.php?/attachments/get/120826012) ![](index.php?/attachments/get/120826013)
        """
        pass
