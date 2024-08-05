import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C18753268_Verify_My_Bets_counter_during_Overask(Common):
    """
    TR_ID: C18753268
    NAME: Verify My Bets counter during Overask
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after Overask was triggered and Bet was placed/ not placed
    DESCRIPTION: AUTOTEST [C58665521] TST ONLY
    PRECONDITIONS: - Load Oxygen/Roxanne Application and login
    PRECONDITIONS: - Overask is enabled for logged in user
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: - OB TI tool:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True

    def test_001__add_selection_to_quick_betbetslip_trigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: * Add selection to Quick bet/Betslip
        DESCRIPTION: * Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002__close_betslip_or_refresh_the_page_check_my_bets_counter(self):
        """
        DESCRIPTION: * Close betslip or refresh the page
        DESCRIPTION: * Check My bets counter
        EXPECTED: My bets counter remains the same
        """
        pass

    def test_003_accept_the_bet_in_ob_ti_tool_and_check_bet_is_placed_on_coralladbrokes(self):
        """
        DESCRIPTION: Accept the bet in OB TI tool and check bet is placed on Coral/Ladbrokes
        EXPECTED: * Bet is placed and bet receipt is displayed
        """
        pass

    def test_004__close_betslip_check_my_bets_counter(self):
        """
        DESCRIPTION: * Close betslip
        DESCRIPTION: * Check My bets counter
        EXPECTED: My bets counter is increased by one
        """
        pass

    def test_005_repeat_step_1_2_and_decline_the_bet_in_ob_ti_toolcheck_bet_is_not_placed_on_coralladbrokes(self):
        """
        DESCRIPTION: Repeat step #1-2 and Decline the bet in OB TI tool
        DESCRIPTION: check bet is NOT placed on Coral/Ladbrokes
        EXPECTED: * Bet is NOT placed
        """
        pass

    def test_006__close_betslip_check_my_bets_counter(self):
        """
        DESCRIPTION: * Close betslip
        DESCRIPTION: * Check My bets counter
        EXPECTED: My bets counter remains the same
        """
        pass

    def test_007_repeat_step_1_2_and_make_an_offer_in_ob_ti_tool(self):
        """
        DESCRIPTION: Repeat step #1-2 and make an offer in OB TI tool
        EXPECTED: Bet is NOT placed and offer is shown to user
        """
        pass

    def test_008__close_betslip_check_my_bets_counter(self):
        """
        DESCRIPTION: * Close betslip
        DESCRIPTION: * Check My bets counter
        EXPECTED: My bets counter remains the same
        """
        pass

    def test_009__open_betslip_and_confirm_the_offer_reject_the_offer_check_my_bets_counter(self):
        """
        DESCRIPTION: * Open betslip and confirm the offer/ reject the offer
        DESCRIPTION: * Check My bets counter
        EXPECTED: * My bets counter is increased by one if offer was accepted
        EXPECTED: * My bets counter remains the same if offer was rejected
        """
        pass
