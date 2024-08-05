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
class Test_C59898506_Single_bet_is_split_into_2_part_of_the_stake_is_offered_at_LP_and_the_rest_at_SPLinked(Common):
    """
    TR_ID: C59898506
    NAME: Single bet is split into 2: part of the stake is offered at LP and the rest at SP.(Linked)
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

    def test_002_split_the_single_bet_into_2_1st_part_of_the_stake_is_offered_at_lp_and_the_2nd_part_at_splinked(self):
        """
        DESCRIPTION: Split the single bet into 2: 1st part of the stake is offered at LP and the 2nd part at SP.(Linked)
        EXPECTED: Customer should see in the counter offer 2 singles, with the stake highlighted for LP selection and price and stake highlighted for SP selection
        """
        pass

    def test_003_check_the_potential_returns(self):
        """
        DESCRIPTION: Check the Potential returns
        EXPECTED: Potential returns for the single offered at LP should show updated potential returns
        EXPECTED: Potential returns for the single offered at SP should be N/A and the total potential returns should be N/A
        EXPECTED: Customer is able to accept, remove second offer, or decline the counter offer.
        """
        pass

    def test_004_if_customer_removes_second_single_and_accepted_other_single(self):
        """
        DESCRIPTION: If customer removes second single and accepted other single
        EXPECTED: The bet receipt should show only one single bet with updated potential returns and only one single bet is shown in My Bets and Account History.
        """
        pass

    def test_005_if_customer_accepts_the_offer_without_removing_any_single(self):
        """
        DESCRIPTION: If Customer accepts the offer (without removing any single)
        EXPECTED: The two bets are placed and the user is taken to the bet receipt where two bets are shown in My Bets and Account History
        """
        pass

    def test_006_if_the_offer_is_declined(self):
        """
        DESCRIPTION: If the offer is declined
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        pass

    def test_007_split_the_single_bet_into_2_1st_part_of_the_stake_is_offered_at_sp_and_the_2nd_part_at_lplinked(self):
        """
        DESCRIPTION: Split the single bet into 2: 1st part of the stake is offered at SP and the 2nd part at LP.(Linked)
        EXPECTED: Customer should see in the counter offer 2 singles, with the stake highlighted for LP selection and price and stake highlighted for SP selection
        """
        pass

    def test_008_repeat_steps_3___6(self):
        """
        DESCRIPTION: Repeat steps 3 - 6.
        EXPECTED: 
        """
        pass
