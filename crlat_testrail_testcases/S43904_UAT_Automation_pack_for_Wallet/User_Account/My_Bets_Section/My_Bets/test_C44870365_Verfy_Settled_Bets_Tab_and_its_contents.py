import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870365_Verfy_Settled_Bets_Tab_and_its_contents(Common):
    """
    TR_ID: C44870365
    NAME: Verfy Settled Bets Tab and its contents.
    DESCRIPTION: This TC is to verify Settled Tab and its contents.
    PRECONDITIONS: Used should be logged in
    PRECONDITIONS: User must have some single, double, each way and accumulator bets placed.
    PRECONDITIONS: User should have some settled bets.
    """
    keep_browser_open = True

    def test_001__verfiy_settled_bets_tab_header_for_following_bet_type_for_each_bet_single__double__acca_etc__result_label_for_the_overall_bet_lost_won_cashed_out_void__leftright_layout(self):
        """
        DESCRIPTION: -Verfiy Settled Bets Tab Header for following
        DESCRIPTION: * Bet type for each bet (Single / Double / ACCA etc )
        DESCRIPTION: * Result label for the overall bet (Lost/ Won/ Cashed out, Void) ( Left/Right Layout)
        EXPECTED: User is able to see
        EXPECTED: * Bet type for each bet (Single / Double / ACCA etc ) (Left side of bet header)
        EXPECTED: * Result label for the overall bet (Lost/ Won/ Cashed out, Void) (Right side of the bet header)
        """
        pass

    def test_002_verify_user_can_see__profit__loss_information_with_down_arrow(self):
        """
        DESCRIPTION: Verify user can see  Profit / Loss information with down arrow.
        EXPECTED: User is able to see Profit/Loss section just above the bets with down arrow on it.
        """
        pass

    def test_003_verify_user_can_see_profitloss_information_by_clicking_on_it(self):
        """
        DESCRIPTION: Verify user can see Profit/Loss information by clicking on it.
        EXPECTED: Uses is able Profit/Loss information by clicking on it (This will show information based on dates set in the calendar)
        """
        pass

    def test_004_verify_information_which_appears_on_screen_is_based_on_dates_chosenverify_sports_lotto_and_pools_tab_in_settled_betsverify_settled_bets_tab_and_the_footer_lists_contains_the_stake_potential_return_receipt_id_time_and_date_stamp(self):
        """
        DESCRIPTION: Verify information which appears on screen is based on dates chosen
        DESCRIPTION: Verify Sports, Lotto and Pools tab in 'Settled Bets'
        DESCRIPTION: Verify Settled Bets Tab and the footer lists Contains
        DESCRIPTION: -The stake
        DESCRIPTION: -Potential return
        DESCRIPTION: -Receipt ID
        DESCRIPTION: -Time and date stamp
        EXPECTED: User is able to see information based on dates set in the calendar for following tabs Sports, Lotto and Pools.
        EXPECTED: User is able to see following details.
        EXPECTED: -The stake
        EXPECTED: -Potential return
        EXPECTED: -Receipt ID
        EXPECTED: -Time and date stamp
        """
        pass
