import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898505_Single_bet_is_split_into_2_singles_part_of_the_stake_is_offered_at_one_LP_price_and_the_rest_of_it_at_another_LP_price_Linked(Common):
    """
    TR_ID: C59898505
    NAME: Single bet is split into 2 singles: part of the stake is offered at one LP price and the rest of it at another LP price. (Linked)
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_hr_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add HR selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_split_the_single_bet_into_2_1st_part_of_the_stake_is_offered_at_original_lp_and_the_2nd_part_at_another_lplinked(self):
        """
        DESCRIPTION: Split the single bet into 2: 1st part of the stake is offered at original LP and the 2nd part at another LP.(Linked)
        EXPECTED: Customer should see in the counter offer for 2 singles, with the stakes being highlighted for both the selections
        EXPECTED: Customer is able to accept, remove second offer, or decline the counter offer.
        """
        pass

    def test_003_if_customer_removes_second_single_and_accepted_other_single(self):
        """
        DESCRIPTION: If customer removes second single and accepted other single
        EXPECTED: The bet receipt should show only one single bet with updated potential returns and only one single bet is shown in My Bets and Account History.
        """
        pass

    def test_004_if_customer_accepts_the_offer_without_removing_any_single(self):
        """
        DESCRIPTION: If Customer accepts the offer (without removing any single)
        EXPECTED: The two bets are placed and the user is taken to the bet receipt where two bets are shown in My Bets and Account History
        """
        pass

    def test_005_if_the_offer_is_declined(self):
        """
        DESCRIPTION: If the offer is declined
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        pass

    def test_006_split_the_single_bet_into_2_1st_part_of_the_stake_is_offered_at_sp_and_the_2nd_part_at_another_lplinked(self):
        """
        DESCRIPTION: Split the single bet into 2: 1st part of the stake is offered at SP and the 2nd part at another LP.(Linked)
        EXPECTED: Customer should see in the counter offer for 2 singles, with the stakes being highlighted for both the selections
        EXPECTED: Customer is able to accept, remove second offer, or decline the counter offer.
        """
        pass

    def test_007_repeat_step_3_to_5(self):
        """
        DESCRIPTION: Repeat step 3 to 5.
        EXPECTED: 
        """
        pass
