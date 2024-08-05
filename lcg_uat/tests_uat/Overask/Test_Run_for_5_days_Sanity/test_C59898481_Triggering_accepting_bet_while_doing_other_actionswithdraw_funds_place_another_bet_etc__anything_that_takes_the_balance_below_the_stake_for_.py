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
class Test_C59898481_Triggering_accepting_bet_while_doing_other_actionswithdraw_funds_place_another_bet_etc__anything_that_takes_the_balance_below_the_stake_for_the_OA_bet_negative_case(Common):
    """
    TR_ID: C59898481
    NAME: Triggering accepting bet while doing other actions(withdraw funds, place another bet, etc) - anything that takes the balance below the stake for the OA bet (negative case)
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

    def test_002_open_site_in_different_browser_and_do_withdraw_funds_place_another_bet_etcanything_that_takes_the_balance_below_the_stake_for_the_oa_bet(self):
        """
        DESCRIPTION: Open site in different browser and do withdraw funds, place another bet, etc(anything that takes the balance below the stake for the OA bet)
        EXPECTED: Balance should be update accordingly on FE
        """
        pass

    def test_003_trigger_accepting_bet_in_ob_ti(self):
        """
        DESCRIPTION: Trigger accepting bet in OB TI
        EXPECTED: Bet should not be placed as customer has a balance less than the stake of the offer.
        """
        pass
