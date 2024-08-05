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
class Test_C59898513_Verify_Odds_Boost_token_is_NOT_used_up_if_trader_declines_times_out_or_user_cancels_times_out(Common):
    """
    TR_ID: C59898513
    NAME: Verify Odds Boost token is NOT used up if trader declines/times out or user cancels/times out.
    DESCRIPTION: 
    PRECONDITIONS: User needs to have odds boost tokens assigned.
    """
    keep_browser_open = True

    def test_001_add_any_selection_click_on_odds_boost_and_trigger_oa(self):
        """
        DESCRIPTION: Add any selection, click on odds boost and trigger OA.
        EXPECTED: Trader should see the bet in OB.
        """
        pass

    def test_002_trader_times_out_the_bet(self):
        """
        DESCRIPTION: Trader times out the bet
        EXPECTED: User should see the message and able to use odds boost token for same or other bet.
        """
        pass

    def test_003_repeat_step_1__2_but_trader_declining_bet_this_time(self):
        """
        DESCRIPTION: Repeat step 1 & 2 but trader declining bet this time.
        EXPECTED: User should see the message and able to use odds boost token for same or other bet.
        """
        pass

    def test_004_add_any_selection_click_on_odds_boost_and_trigger_oa(self):
        """
        DESCRIPTION: Add any selection, click on odds boost and trigger OA.
        EXPECTED: Trader should see the bet in OB.
        """
        pass

    def test_005_trader_offers_price_or_stake(self):
        """
        DESCRIPTION: Trader offers price or stake
        EXPECTED: User should see the offer.
        """
        pass

    def test_006_user_times_out_the_offer(self):
        """
        DESCRIPTION: User times out the offer
        EXPECTED: User should see the message and able to use odds boost token for same or other bet.
        """
        pass

    def test_007_repeat_steps_4_and_5(self):
        """
        DESCRIPTION: Repeat steps 4 and 5
        EXPECTED: 
        """
        pass

    def test_008_user_cancels_the_offer(self):
        """
        DESCRIPTION: User cancels the offer
        EXPECTED: User should see the message and able to use odds boost token for same or other bet.
        """
        pass
