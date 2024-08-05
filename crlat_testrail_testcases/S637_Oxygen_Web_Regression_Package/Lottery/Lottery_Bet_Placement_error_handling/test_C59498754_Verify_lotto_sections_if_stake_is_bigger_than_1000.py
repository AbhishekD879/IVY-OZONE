import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.lotto
@vtest
class Test_C59498754_Verify_lotto_sections_if_stake_is_bigger_than_1000(Common):
    """
    TR_ID: C59498754
    NAME: Verify lotto sections if stake is bigger than 1000
    DESCRIPTION: This test case verifies lotto sections stay inserted after error message that user has insufficient funds to place a bet (stake is bigger than 1000)
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User balance is less than 1000
    """
    keep_browser_open = True

    def test_001_select_numbers_in_any_lotto_section_or_use_lucky_x_quick_buttons(self):
        """
        DESCRIPTION: Select numbers in any lotto section (or use 'Lucky x' quick buttons)
        EXPECTED: Numbers are selected
        """
        pass

    def test_002_insert_stake_into_stake_field_that_equals_1000_and_placeconfirm_bet(self):
        """
        DESCRIPTION: Insert stake into stake field that equals 1000 and place/confirm bet
        EXPECTED: - Error message is displayed to the user that he has insufficient funds to place a bet
        EXPECTED: - Bet is not placed
        EXPECTED: - All numbers remain selected
        """
        pass

    def test_003_change_stake_value_to_a_bigger_one_eg_1001_and_placeconfirm_bet(self):
        """
        DESCRIPTION: Change stake value to a bigger one (eg. 1001) and place/confirm bet
        EXPECTED: - Error message is displayed to the user that he has insufficient funds to place a bet
        EXPECTED: - Bet is not placed
        EXPECTED: - All numbers remain selected
        """
        pass

    def test_004_try_to_include_any_other_options_in_the_bet_eg_include_bonus_ball_checkbox_and_placeconfirm_bet(self):
        """
        DESCRIPTION: Try to include any other options in the bet (eg. 'Include Bonus Ball' checkbox) and place/confirm bet
        EXPECTED: Results remain the same as above
        EXPECTED: ![](index.php?/attachments/get/115915064)
        """
        pass
