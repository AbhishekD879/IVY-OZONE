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
class Test_C59898479_Single_E_W_bet_is_split_into_two_bets__one_E_W_bet_and_one_Win_Only_betUnLinked(Common):
    """
    TR_ID: C59898479
    NAME: Single E/W bet is split into two bets - one E/W bet and one Win Only bet(UnLinked)
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_selection_from_any_outright_event_to_quick_betbetsliptrigger_overask__select_ew_checkbox_and_try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection from any outright event to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( Select E/W checkbox and try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_split_the_single_ew_bet__into_two_bets___one_ew_bet_and_one_win_only_bet_with_the_price_of_1st_part_as_lp_and_the_2nd_part_as_spstakes_are_divided_between_the_two_singles(self):
        """
        DESCRIPTION: Split the single E/W bet  into two bets - one E/W bet and one Win Only bet, with the price of 1st part as LP and the 2nd part as SP
        DESCRIPTION: Stakes are divided between the two SINGLES.
        EXPECTED: Customer sees in the counter offer 2 bets, with the original stake being spread over the two bets - the first will be E/W and the second will be win only and only the stakes will be highlighted in both bets.
        EXPECTED: Customer is able to accept, remove one of the offers, or decline the counter offer.
        """
        pass

    def test_003_if_customer_removes_one_single_and_accepted_other_single(self):
        """
        DESCRIPTION: If customer removes one single and accepted other single
        EXPECTED: The bet receipt should show only one single bet with updated potential returns and only one single bet is shown in My Bets and Account History.
        """
        pass

    def test_004_if_customer_accepts_the_offer_without_removing_any_single(self):
        """
        DESCRIPTION: If Customer accepts the offer (without removing any single)
        EXPECTED: The two bets are placed and the user is taken to the bet receipt where two bets are shown in My Bets and Account History
        EXPECTED: Balance should be updated correctly
        """
        pass

    def test_005_if_customer_declines_the_offer(self):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History
        """
        pass

    def test_006_split_the_single_ew_bet__into_two_bets___one_ew_bet_and_one_win_only_bet_with_the_price_of_1st_part_as_sp_and_the_2nd_part_as_lpstakes_are_divided_between_the_two_singles(self):
        """
        DESCRIPTION: Split the single E/W bet  into two bets - one E/W bet and one Win Only bet, with the price of 1st part as SP and the 2nd part as LP
        DESCRIPTION: Stakes are divided between the two SINGLES.
        EXPECTED: Customer sees in the counter offer 2 bets, with the original stake being spread over the two bets - the first will be E/W and the second will be win only and only the stakes will be highlighted in both bets.
        EXPECTED: Customer is able to accept, remove one of the offers, or decline the counter offer.
        """
        pass

    def test_007_repeat_steps_3_to_5(self):
        """
        DESCRIPTION: Repeat steps 3 to 5.
        EXPECTED: 
        """
        pass
