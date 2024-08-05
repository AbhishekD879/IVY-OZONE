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
class Test_C59905926_Verify_Betslip_Keypad_UI(Common):
    """
    TR_ID: C59905926
    NAME: Verify Betslip Keypad UI
    DESCRIPTION: This test case verifies Betslip Keypad UI according to design:
    DESCRIPTION: **Ladbrokes:**
    DESCRIPTION: *Light* - https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea97d882661b1bc353c7f13
    DESCRIPTION: *Dark* - https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea97cfd8867e3bdfcc923a5
    DESCRIPTION: **Coral:**
    DESCRIPTION: *Light* - https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2cbc7ba7020573733544c
    DESCRIPTION: *Dark* - https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5eaa984f97f4f5bdb18945a8
    PRECONDITIONS: * The app is installed and launched
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has not 0 balance
    PRECONDITIONS: * User is able make a stake
    PRECONDITIONS: * The Light mode is turn on on the device
    """
    keep_browser_open = True

    def test_001__tap_on_a_odds_button(self):
        """
        DESCRIPTION: * Tap on a odds button
        EXPECTED: * The odd is added to Betslip
        EXPECTED: * The Betslip is shown in collapse state in the bottom of the screen
        """
        pass

    def test_002__expand_the_betslip(self):
        """
        DESCRIPTION: * Expand the Betslip
        EXPECTED: * The Betslip is expanded
        EXPECTED: * User can see all added odds
        EXPECTED: * Stake field is available
        """
        pass

    def test_003__tap_on_the_stake_field(self):
        """
        DESCRIPTION: * Tap on the Stake field
        EXPECTED: * Betslip Keypad is shown
        EXPECTED: * Betslip Keypad UI corresponds to the designs for Light mode
        EXPECTED: * Total stake information is shown below keypad and corresponds to the designs for Light mode
        EXPECTED: * Potential returns information is shown below keypad and corresponds to the designs for Light mode
        EXPECTED: **Ladbrokes:**
        EXPECTED: ![](index.php?/attachments/get/119064569)
        EXPECTED: **Coral:**
        EXPECTED: ![](index.php?/attachments/get/119064570)
        """
        pass

    def test_004__turn_on_the_dark_mode_on_the_device_and_repeat_steps_1_3(self):
        """
        DESCRIPTION: * Turn on the Dark mode on the device and repeat Steps 1-3
        EXPECTED: * Betslip Keypad is shown
        EXPECTED: * Betslip Keypad UI corresponds to the designs for Dark mode
        EXPECTED: * Total stake information is shown below keypad and corresponds to the designs for Dark mode
        EXPECTED: * Potential returns information is shown below keypad and corresponds to the designs for Dark mode
        EXPECTED: **Ladbrokes:**
        EXPECTED: ![](index.php?/attachments/get/119064571)
        EXPECTED: **Coral:**
        EXPECTED: ![](index.php?/attachments/get/119064572)
        """
        pass
