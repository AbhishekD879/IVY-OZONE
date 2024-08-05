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
class Test_C2987526_Verify_that_each_way_bets_can_be_boosted_and_placed_in_Betslip_Multiple_selections(Common):
    """
    TR_ID: C2987526
    NAME: Verify that each way bets can be boosted and placed in Betslip (Multiple selections)
    DESCRIPTION: This test case verifies that each way bet can be boosted and placed in Betslip for Multiple selection
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: For creating Odds Boost tokens use instruction: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: CREATE Odds Boost token with ANY Bet Type
    PRECONDITIONS: Add 2(two) just created odds boost tokens to USER1
    PRECONDITIONS: Login with USER1
    PRECONDITIONS: Add two selections from Horse Racing/Greyhounds (E/W market with LP available) to Betslip
    """
    keep_browser_open = True

    def test_001_navigate_to_betslipadd_a_stake_to_singles_and_doubleverify_that_odds_boost_section_is_available(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Add a Stake to SINGLES and DOUBLE
        DESCRIPTION: Verify that odds boost section is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_002_check_each_way_checkbox_for_singles_and_doubleverify_that_total_stake_and_est_returns_are_updated_appropriately(self):
        """
        DESCRIPTION: Check 'Each Way' checkbox for SINGLES and DOUBLE
        DESCRIPTION: Verify that Total Stake and Est. Returns are updated appropriately
        EXPECTED: - 'Each Way' checkbox is checked for SINGLES and DOUBLE
        EXPECTED: - Updated Est. Returns for SINGLES and DOUBLE are shown
        EXPECTED: - Updated Estimated/Potential Returns is shown
        EXPECTED: - Updated Total Stake is shown
        """
        pass

    def test_003_tap_boost_buttonverify_that_odds_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted
        EXPECTED: Betslip is shown with appropriate elements for SINGLES and DOUBLE:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds are shown for SINGLES and DOUBLE
        EXPECTED: - Updated Est. Returns are shown for SINGLES are shown
        EXPECTED: - Updated Est. Returns are shown for DOUBLE as N/A
        EXPECTED: - Updated Estimated/Potential Returns is shown
        """
        pass

    def test_004_tap_place_bet_buttonverify_that_bet_is_placed_with_each_way_stake_and_boosted_odds(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with each way stake and boosted odds
        EXPECTED: Bet receipt is shown with appropriate elements for SINGLES and DOUBLE:
        EXPECTED: - Odds boost title
        EXPECTED: - Calculated odds
        EXPECTED: - 2Lines at (Amount) per line
        EXPECTED: - Stake = Total Stake
        """
        pass

    def test_005_tap_reuse_selection_buttonadd_one_more_selection_from_horse_racinggreyhounds_ew_market_with_sp_only_to_betslipand_add_stake_for_singles_and_trebleverify_that_odds_boost_button_is_shown(self):
        """
        DESCRIPTION: Tap 'Reuse selection' button
        DESCRIPTION: Add one more selection from Horse Racing/Greyhounds (E/W market with SP ONLY) to Betslip
        DESCRIPTION: And add Stake for SINGLES and TREBLE
        DESCRIPTION: Verify that odds boost button is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_006_tap_boost_button(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        EXPECTED: Betslip is shown with appropriate elements:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds are shown for SINGLES with LP
        EXPECTED: - 'i' icon is shown for SINGLE with SP and for TREBLE
        EXPECTED: - Updated Est. Returns is shown for SINGLES with LP
        EXPECTED: - N/A Est. returns is shown for SINGLE with SP and for TREBLE
        EXPECTED: - N/A Estimated/Potential Returns is shown
        """
        pass

    def test_007_check_each_way_checkbox_for_singles_and_trebleverify_that_total_stake_and_est_return_are_updated_appropriately(self):
        """
        DESCRIPTION: Check 'Each Way' checkbox for SINGLES and TREBLE
        DESCRIPTION: Verify that Total Stake and Est. Return are updated appropriately
        EXPECTED: - 'Each Way' checkbox is checked for SINGLES and TREBLE
        EXPECTED: - Updated Total Stake is shown
        EXPECTED: - Estimated/Potential Returns is N/A
        """
        pass

    def test_008_tap_place_bet_buttonverify_that_bet_is_placed_and_boosted_odds(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed and boosted odds
        EXPECTED: Bet receipt is shown with appropriate elements for for SINGLES and TREBLE:
        EXPECTED: - Odds boost title
        EXPECTED: - Calculated odds for LP SINGLES
        EXPECTED: - N/A odds for TREBLE and SP Single
        EXPECTED: - 2Lines at (Amount) per line
        EXPECTED: - Stake = Total Stake
        """
        pass
