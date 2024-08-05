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
class Test_C59898460_Any_Counter_Offer_gets_sent_back_and_times_out_on_the_front_end(Common):
    """
    TR_ID: C59898460
    NAME: Any Counter Offer gets sent back and times out on the front end
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_counter_offer_by_stakeprice(self):
        """
        DESCRIPTION: Counter Offer by Stake/Price
        EXPECTED: Counter offer gets sent back
        """
        pass

    def test_003_time_out_on_the_front_end(self):
        """
        DESCRIPTION: Time out on the front end
        EXPECTED: After the Counter Offer has expired, the customer will see the bet slip with the message that the offer has Expired and we should not see a bet in My Bets and Account History.
        """
        pass
