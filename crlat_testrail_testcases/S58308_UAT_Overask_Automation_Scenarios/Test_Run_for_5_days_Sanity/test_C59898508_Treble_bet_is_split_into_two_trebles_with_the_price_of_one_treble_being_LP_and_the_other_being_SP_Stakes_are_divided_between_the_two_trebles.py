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
class Test_C59898508_Treble_bet_is_split_into_two_trebles_with_the_price_of_one_treble_being_LP_and_the_other_being_SP_Stakes_are_divided_between_the_two_trebles_Linked(Common):
    """
    TR_ID: C59898508
    NAME: Treble bet is split into two trebles, with the price of one treble being LP and the other being SP. Stakes are divided between the two trebles. (Linked)
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_treble_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add treble selections to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_split_the_treble_bets_into_two_trebles_with_the_price_of_1st_treble_being_lp_and_the_2nd_treble_being_splinkedstakes_are_divided_between_the_two_trebles(self):
        """
        DESCRIPTION: Split the treble bets into two trebles, with the price of 1st treble being LP and the 2nd treble being SP(Linked)
        DESCRIPTION: Stakes are divided between the two trebles.
        EXPECTED: Customer sees in the counter offer 2 treble bets, with the original stake being spread over the two bets - the first will be offered at unchanged LP prices, so only the stake will be highlighted
        EXPECTED: The second at SP prices, so both price and stake are highlighted.
        """
        pass

    def test_003_customer_is_able_to_accept_remove_second_offer_or_decline_the_counter_offer(self):
        """
        DESCRIPTION: Customer is able to accept, remove second offer, or decline the counter offer.
        EXPECTED: 
        """
        pass

    def test_004_if_customer_removes_second_treble_and_accepted_other(self):
        """
        DESCRIPTION: If customer removes second Treble and accepted other
        EXPECTED: The bet receipt should show only one Treble bet with updated potential returns and only one  bet is shown in My Bets and Account History.
        """
        pass

    def test_005_if_customer_accepts_the_offer_without_removing_any_treble(self):
        """
        DESCRIPTION: If Customer accepts the offer (without removing any Treble)
        EXPECTED: The two bets are placed and the user is taken to the bet receipt where two bets are shown in My Bets and Account History
        """
        pass

    def test_006_if_the_offer_is_declined(self):
        """
        DESCRIPTION: If the offer is declined
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        pass

    def test_007_split_the_treble_bets_into_two_trebles_with_the_price_of_1st_treble_being_sp_and_the_2nd_treble_being_lplinkedstakes_are_divided_between_the_two_trebles(self):
        """
        DESCRIPTION: Split the treble bets into two trebles, with the price of 1st treble being SP and the 2nd treble being LP(Linked)
        DESCRIPTION: Stakes are divided between the two trebles.
        EXPECTED: Customer sees in the counter offer 2 treble bets, with the original stake being spread over the two bets - the first will be offered at unchanged LP prices, so only the stake will be highlighted
        EXPECTED: The second at SP prices, so both price and stake are highlighted.
        """
        pass

    def test_008_repeat_step_3_to_6(self):
        """
        DESCRIPTION: Repeat step 3 to 6.
        EXPECTED: 
        """
        pass
