import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C59898486_Automtically_Accept_OA_bet_made_with_a_free_bet_when_the_user_has_OA_turned_off_his_her_stake_factor_is_001_and_the_free_bet_is_greater_than_the_his_her_max_stake_but_less_than_the_max_stake_of_a_10_stake_factor_user(Common):
    """
    TR_ID: C59898486
    NAME: Automtically Accept OA bet made with a free bet when the user has OA turned off, his/her stake factor is 0.01 and the free bet is greater than the his/her max stake, but less than the max stake of a 1.0 stake factor user
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_change_your_users_stake_factor_to_001_and_select_the_block_bet_intercept_option_in_the_block_bet_column_using_the_following_steps1_click_on_customer_in_the_ti2_enter_your_username_and_click_on_search3_when_you_are_in_your_users_record_click_on_account_rules4_at_the_global_level_change_the_stake_to_001_and_select_the_block_bet_intercept_option_in_the_block_bet_column(self):
        """
        DESCRIPTION: Change your user's stake factor to 0.01 and select the Block Bet Intercept option in the Block bet column using the following steps:
        DESCRIPTION: 1. Click on Customer in the TI
        DESCRIPTION: 2. Enter your username and click on Search
        DESCRIPTION: 3. When you are in your user's record, click on Account Rules
        DESCRIPTION: 4. At the Global level, change the Stake to 0.01 and select the Block Bet Intercept option in the block bet column
        EXPECTED: You should have changed your user's stake factor to 0.01 and block bet intercept for your user
        """
        pass

    def test_002_using_openbet_make_the_max_stake_for_any_selection_to_1(self):
        """
        DESCRIPTION: Using Openbet, make the max stake for any selection to £1
        EXPECTED: You should have changed the max bet for any selection to £1
        """
        pass

    def test_003_award_yourself_a_free_bet_of_002(self):
        """
        DESCRIPTION: Award yourself a free bet of £0.02
        EXPECTED: You should have awarded yourself a free bet of  £0.02
        """
        pass

    def test_004_click_on_the_selection_that_you_changed_the_max_stake_for_in_step_2_and_use_your_free_bet_to_place_the_bet(self):
        """
        DESCRIPTION: Click on the selection that you changed the max stake for in step 2 and use your free bet to place the bet.
        EXPECTED: Your bet should go through and you should see the bet receipt.
        """
        pass
