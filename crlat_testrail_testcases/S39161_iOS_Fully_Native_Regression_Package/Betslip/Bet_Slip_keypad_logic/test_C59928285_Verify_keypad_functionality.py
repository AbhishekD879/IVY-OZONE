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
class Test_C59928285_Verify_keypad_functionality(Common):
    """
    TR_ID: C59928285
    NAME: Verify keypad functionality
    DESCRIPTION: This test case verifies keypad functionality
    DESCRIPTION: Design:
    DESCRIPTION: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5eaaf045cc16338ef685881f
    PRECONDITIONS: - Selection is added to the Bet slip
    PRECONDITIONS: - Bet slip is expanded
    """
    keep_browser_open = True

    def test_001_enter_into_stake_field_more_than_9_digits(self):
        """
        DESCRIPTION: Enter into 'Stake' field more than 9 digits
        EXPECTED: - Crop point for an edge case according to design is displayed:
        EXPECTED: ![](index.php?/attachments/get/119788294)
        """
        pass

    def test_002_remove_all_digits(self):
        """
        DESCRIPTION: Remove all digits
        EXPECTED: - All digits one by one are removed from 'Stake' field
        EXPECTED: - '0' input value is displayed
        """
        pass

    def test_003_try_to_enter_13_digits_before_dot_into_stake_field(self):
        """
        DESCRIPTION: Try to enter 13 digits before dot into 'Stake' field
        EXPECTED: - Only 12 digits before dot are allowed to enter into 'Stake' field
        """
        pass

    def test_004_try_to_enter_more_than_2_digits_after_dot_into_stake_field(self):
        """
        DESCRIPTION: Try to enter more than 2 digits after dot into 'Stake' field
        EXPECTED: - Not more than 2 digits are allowed to enter after dot into 'Stake' field
        """
        pass

    def test_005_try_to_enter_more_than_one_dot_into_stake_field(self):
        """
        DESCRIPTION: Try to enter more than one dot into 'Stake' field
        EXPECTED: - Only one dot and digits are alloved to enter into 'Stake' field (15 symbols in general)
        """
        pass
