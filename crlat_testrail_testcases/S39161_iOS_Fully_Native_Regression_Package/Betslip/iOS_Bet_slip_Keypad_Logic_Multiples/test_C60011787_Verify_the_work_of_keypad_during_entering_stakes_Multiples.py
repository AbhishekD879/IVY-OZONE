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
class Test_C60011787_Verify_the_work_of_keypad_during_entering_stakes_Multiples(Common):
    """
    TR_ID: C60011787
    NAME: Verify the work of keypad during entering stakes (Multiples)
    DESCRIPTION: Test case verifies  keypad functionality (Multiples).
    PRECONDITIONS: App installed and launched
    PRECONDITIONS: Bet slip contains several selections (more then 2)
    PRECONDITIONS: Betslip expanded
    PRECONDITIONS: Designs:
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2aea0d688528346b808f0
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/dashboard?sid=5ea989452d8bd3bda177b7c0
    PRECONDITIONS: Example of max stake input - https://zpl.io/adJD9re
    """
    keep_browser_open = True

    def test_001__tap_on_multiple_stake_field(self):
        """
        DESCRIPTION: * Tap on Multiple "Stake" field
        EXPECTED: *Stake field becomes active
        EXPECTED: * Must display 0 input in stake field without currency symbol
        EXPECTED: "Stake" field states designs:
        EXPECTED: ![](index.php?/attachments/get/120936931)
        EXPECTED: ![](index.php?/attachments/get/120936932)
        EXPECTED: ![](index.php?/attachments/get/120936933)
        EXPECTED: ![](index.php?/attachments/get/120936934)
        EXPECTED: ![](index.php?/attachments/get/120936935)
        """
        pass

    def test_002__enter_into_stake_field_more_than_9_digits(self):
        """
        DESCRIPTION: * Enter into 'Stake' field more than 9 digits
        EXPECTED: * Crop point for an edge case according to design is displayed:
        """
        pass

    def test_003__remove_all_digits(self):
        """
        DESCRIPTION: * Remove all digits
        EXPECTED: * All digits one by one are removed from 'Stake' field
        EXPECTED: '0' input value is displayed
        """
        pass

    def test_004__try_to_enter_13_digits_before_dot_into_stake_field(self):
        """
        DESCRIPTION: * Try to enter 13 digits before dot into 'Stake' field
        EXPECTED: * Only 12 digits before dot are allowed to enter into 'Stake' field
        """
        pass

    def test_005__try_to_enter_more_than_2_digits_after_dot_into_stake_field(self):
        """
        DESCRIPTION: * Try to enter more than 2 digits after dot into 'Stake' field
        EXPECTED: * Not more than 2 digits are allowed to enter after dot into 'Stake' field
        """
        pass

    def test_006__try_to_enter_more_than_one_dot_into_stake_field(self):
        """
        DESCRIPTION: * Try to enter more than one dot into 'Stake' field
        EXPECTED: * Only one dot and digits are alloved to enter into 'Stake' field (15 symbols in general)
        """
        pass
