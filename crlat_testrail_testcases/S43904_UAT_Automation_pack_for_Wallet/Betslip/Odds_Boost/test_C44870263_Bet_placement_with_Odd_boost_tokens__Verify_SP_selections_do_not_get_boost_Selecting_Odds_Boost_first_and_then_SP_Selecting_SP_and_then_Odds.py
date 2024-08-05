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
class Test_C44870263_Bet_placement_with_Odd_boost_tokens__Verify_SP_selections_do_not_get_boost_Selecting_Odds_Boost_first_and_then_SP_Selecting_SP_and_then_Odds_boost__Verify_Odd_boost_unavailable_popup_for_SP__Place_in_play_boosted_bet_and_verify_bet_receipt_and(Common):
    """
    TR_ID: C44870263
    NAME: "Bet placement with Odd boost tokens - Verify SP selections do not get boost (Selecting Odds Boost first and then SP/ Selecting SP and then Odds boost) - Verify Odd boost unavailable popup for SP - Place in-play boosted bet and verify bet receipt and
    DESCRIPTION: "Bet placement with Odd boost tokens
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_application_and_login_into_the_applicationadd_selection_with_sp_only_availablenavigate_to_betslip_and_add_a_stakeverify_that_the_odds_boost_section_is_not_shown_in_the_betslip(self):
        """
        DESCRIPTION: Load application and Login into the application
        DESCRIPTION: Add selection with SP only available
        DESCRIPTION: Navigate to Betslip and add a stake
        DESCRIPTION: Verify that the Odds Boost section is NOT shown in the Betslip
        EXPECTED: BOOST' button is NOT shown
        EXPECTED: SP odds is shown
        """
        pass

    def test_002_tap_place_bet_buttonverify_that_bet_receipt_is_shown(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that Bet Receipt is shown
        EXPECTED: Bet Receipt is shown with SP odds
        """
        pass

    def test_003_add_selection_with_sp_availablenavigate_to_betslip_and_add_a_stake_to_the_selectionverify_that_the_odds_boost_section_is_shown_in_the_betslip(self):
        """
        DESCRIPTION: Add selection with SP available
        DESCRIPTION: Navigate to Betslip and add a Stake to the selection
        DESCRIPTION: Verify that the Odds Boost section is shown in the Betslip
        EXPECTED: Odds Boost section is shown on the top of Betslip with the following elements:
        EXPECTED: 'BOOST' button
        EXPECTED: 'Tap to boost your betslip' text
        EXPECTED: 'i' icon
        """
        pass

    def test_004_tap_a_boost_button(self):
        """
        DESCRIPTION: Tap a 'BOOST' button
        EXPECTED: User can able to see the boosted odds
        """
        pass

    def test_005_place_in_play_boosted_bet_and_verify_bet_receipt_and_my_bets(self):
        """
        DESCRIPTION: Place in-play boosted bet and verify bet receipt and my bets
        EXPECTED: Boosted bets will be shown in the my bets and bet receipt
        """
        pass

    def test_006_openbet_has_disabled_odd_boost_for_the_event__verify_user_cant_place_boosted_bets_on_the_event(self):
        """
        DESCRIPTION: Openbet has disabled odd boost for the event. , verify user can't place boosted bets on the event
        EXPECTED: user can't place boosted bets on the event
        """
        pass

    def test_007_verify_user_cant_place_boost_bet_more_than_boost_token_max_value(self):
        """
        DESCRIPTION: Verify user can't place boost bet more than boost token max value
        EXPECTED: User can't place boost bet more than boost token max value
        """
        pass

    def test_008_verify_remaning_active_boost_token_count(self):
        """
        DESCRIPTION: Verify remaning active boost token count
        EXPECTED: User should be displayed with the remaining number of odds boost
        """
        pass
