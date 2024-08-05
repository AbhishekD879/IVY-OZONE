import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C2987485_Verify_that_each_way_bets_can_be_boosted_and_placed_in_Quick_Bet(Common):
    """
    TR_ID: C2987485
    NAME: Verify that each way bets can be boosted and placed in Quick Bet
    DESCRIPTION: This test case verifies that each way bet can be boosted and placed in Quick Bet
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: For creating Odds Boost tokens use instruction: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: CREATE Odds Boost token with ANY Bet Type
    PRECONDITIONS: Add 2(two) just created odds boost tokens to USER1
    PRECONDITIONS: Login with USER1.
    """
    keep_browser_open = True

    def test_001_add_selection_from_horse_racinggreyhounds_ew_market_with_lp_available_to_quick_betadd_a_stake_to_selectionverify_that_odds_boost_button_is_available(self):
        """
        DESCRIPTION: Add selection from Horse Racing/Greyhounds (E/W market with LP available) to Quick Bet
        DESCRIPTION: Add a Stake to selection
        DESCRIPTION: Verify that odds boost button is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_002_check_each_way_checkboxverify_that_total_stake_and_total_est_return_are_updated_appropriately(self):
        """
        DESCRIPTION: Check 'Each Way' checkbox
        DESCRIPTION: Verify that Total Stake and Total Est. Return are updated appropriately
        EXPECTED: - 'Each Way' checkbox is checked
        EXPECTED: - Updated Total Stake is shown
        EXPECTED: - Updated Total Est. Returns is shown
        """
        pass

    def test_003_tap_boost_buttonverify_that_odds_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted
        EXPECTED: Quick Bet is shown with appropriate elements:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds are shown
        EXPECTED: - Updated Total Est. Returns is shown
        """
        pass

    def test_004_tap_place_bet_buttonverify_that_bet_is_placed_with_each_way_stake_and_boosted_odds(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with each way stake and boosted odds
        EXPECTED: Bet receipt is shown with appropriate elements:
        EXPECTED: - Odds boost title
        EXPECTED: - Boosted odds
        EXPECTED: - E/W bet (2 Lines at £1.00 per line)
        EXPECTED: - Stake for this bet: currency(amount)
        EXPECTED: - Potential Returns: currency(amount)
        """
        pass

    def test_005_tap_reuse_selection_buttonand_add_stakeverify_that_odds_boost_button_is_shown(self):
        """
        DESCRIPTION: Tap 'Reuse selection' button
        DESCRIPTION: And add Stake
        DESCRIPTION: Verify that odds boost button is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_006_tap_boost_buttondo_not_check__each_way_checkbox(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Do not check  'Each Way' checkbox
        EXPECTED: Quick Bet is shown with appropriate elements:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds are shown
        EXPECTED: - Updated TotalEst. Returns is shown
        """
        pass

    def test_007_tap_place_bet_buttonverify_that_bet_is_placed_and_boosted_odds(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed and boosted odds
        EXPECTED: Bet receipt is shown with appropriate elements:
        EXPECTED: - Odds boost title
        EXPECTED: - Boosted odds
        EXPECTED: - Stake for this bet: currency(amount)
        EXPECTED: - Potential Returns: currency(amount)
        """
        pass
