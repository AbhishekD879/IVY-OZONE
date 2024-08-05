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
class Test_C60004534_Verify_Betslip_view_when_suspended_selection_becomes_active_again(Common):
    """
    TR_ID: C60004534
    NAME: Verify Betslip view when suspended selection becomes active again
    DESCRIPTION: Test case verifies BetSlip view when suspended selection becomes active again
    PRECONDITIONS: Install the app
    PRECONDITIONS: App is opened
    PRECONDITIONS: BetSlip is empty
    PRECONDITIONS: Design:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2a4647b7dbf551708872f
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea97d562bc36f2375a71eca
    """
    keep_browser_open = True

    def test_001__add_any_single_selection_to_betslip_expand_betslip_and_wait_until_current_selection_will_be_suspended(self):
        """
        DESCRIPTION: * Add any single selection to BetSlip
        DESCRIPTION: * Expand BetSlip and wait until current selection will be suspended
        EXPECTED: * Selection was successfully added to BetSlip
        EXPECTED: * BetSlip expanded
        EXPECTED: * Selection was suspended
        EXPECTED: * "Match suspended" message is displayed in expanded BetSlip
        EXPECTED: * Keyboard is greyed
        EXPECTED: * "Place bet" button should update to show "BETTING SUSPENDED"
        EXPECTED: * Customer can not place bet on suspended selection
        EXPECTED: * BetSlip view conforms to Coral/ Ladbrokes Light theme designs:
        EXPECTED: ![](index.php?/attachments/get/120826016) ![](index.php?/attachments/get/120826017)
        """
        pass

    def test_002__collapse_expand_betslip(self):
        """
        DESCRIPTION: * Collapse/ Expand Betslip
        EXPECTED: * Selection remains suspended
        EXPECTED: * BetSlip is expanded
        EXPECTED: * "Match suspended" message is displayed in expanded BetSlip
        EXPECTED: * Keyboard is greyed
        EXPECTED: *  "BETTING SUSPENDED" button displays
        EXPECTED: * Customer can not place bet on suspended selection
        EXPECTED: * BetSlip view conforms to Coral/ Ladbrokes Light theme designs:
        EXPECTED: ![](index.php?/attachments/get/120826016) ![](index.php?/attachments/get/120826017)
        """
        pass

    def test_003__wait_until_current_selection_will_be_active_again(self):
        """
        DESCRIPTION: * Wait until current selection will be active again
        EXPECTED: * Selection is active again
        EXPECTED: * BetSlip expanded
        EXPECTED: * Keyboard is not greyed
        EXPECTED: * "Match suspended" message is not displayed in expanded BetSlip
        EXPECTED: * "BETTING SUSPENDED" button should update to show "Place bet" button
        EXPECTED: * User can place a bet
        """
        pass

    def test_004__collapse_expand_betslip(self):
        """
        DESCRIPTION: * Collapse/ Expand Betslip
        EXPECTED: * Selection remains active
        EXPECTED: * BetSlip expanded
        EXPECTED: * Keyboard is not greyed
        EXPECTED: * "Match suspended" message is not displayed in expanded BetSlip
        EXPECTED: * "Place bet" button displays
        EXPECTED: * User can place a bet
        """
        pass
