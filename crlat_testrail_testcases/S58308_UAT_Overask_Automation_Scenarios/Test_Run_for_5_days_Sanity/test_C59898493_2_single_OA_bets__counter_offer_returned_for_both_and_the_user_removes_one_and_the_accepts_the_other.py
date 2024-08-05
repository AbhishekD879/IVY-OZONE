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
class Test_C59898493_2_single_OA_bets__counter_offer_returned_for_both_and_the_user_removes_one_and_the_accepts_the_other(Common):
    """
    TR_ID: C59898493
    NAME: 2 single OA bets - counter offer returned for both and the user removes one and the accepts the other.
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_two_single_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add two single selections to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_counter_offer_by_price_for_both_singles(self):
        """
        DESCRIPTION: Counter offer by price for both singles
        EXPECTED: Counter offer with the new prices highlighted and updated potential returns shown to the customer
        """
        pass

    def test_003_verify_remove_button(self):
        """
        DESCRIPTION: Verify Remove button
        EXPECTED: User should be able to remove one of the singles and then accept the offer for the other single.
        EXPECTED: Bet receipt, My Bets and Account History should only show the bet accepted by the user.
        """
        pass
