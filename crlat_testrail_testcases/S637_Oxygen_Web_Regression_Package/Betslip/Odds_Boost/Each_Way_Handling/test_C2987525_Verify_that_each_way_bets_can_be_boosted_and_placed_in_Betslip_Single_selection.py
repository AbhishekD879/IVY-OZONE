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
class Test_C2987525_Verify_that_each_way_bets_can_be_boosted_and_placed_in_Betslip_Single_selection(Common):
    """
    TR_ID: C2987525
    NAME: Verify that each way bets can be boosted and placed in Betslip (Single selection)
    DESCRIPTION: This test case verifies that each way bet can be boosted and placed in Betslip for Single selection
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: For creating Odds Boost tokens use instruction: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: CREATE Odds Boost token with ANY Bet Type
    PRECONDITIONS: Add 2(two) just created odds boost tokens to USER1
    PRECONDITIONS: Login with USER1.
    PRECONDITIONS: Add single selection from Horse Racing/Greyhounds (E/W market with LP available) to Betslip
    """
    keep_browser_open = True

    def test_001_navigate_to_betslipadd_a_stake_to_selectionverify_that_odds_boost_section_is_available(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Add a Stake to selection
        DESCRIPTION: Verify that odds boost section is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_002_check_each_way_checkboxverify_that_total_stake_and_total_est_return_are_updated_appropriately(self):
        """
        DESCRIPTION: Check 'Each Way' checkbox
        DESCRIPTION: Verify that Total Stake and Total Est. Return are updated appropriately
        EXPECTED: - 'Each Way' checkbox is checked
        EXPECTED: - Updated Total Stake is shown
        EXPECTED: - Updated Est. Returns and Total Est. Returns are shown
        """
        pass

    def test_003_tap_boost_buttonverify_that_odds_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted
        EXPECTED: Betslip is shown with appropriate elements:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds are shown
        EXPECTED: - Updated Returns are shown
        """
        pass

    def test_004_tap_place_bet_buttonverify_that_bet_is_placed_with_each_way_stake_and_boosted_odds(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with each way stake and boosted odds
        EXPECTED: Bet receipt is shown with appropriate elements:
        EXPECTED: **BeforeOX99**
        EXPECTED: - Odds boost title
        EXPECTED: - Boosted odds
        EXPECTED: - Unit stake: (amount) E/W
        EXPECTED: - Total Stake: (amount)
        EXPECTED: **After OX99**
        EXPECTED: - Odds boost title
        EXPECTED: - Boosted odds
        EXPECTED: - 2Lines at (Amount) per line
        EXPECTED: - Stake = Total Stake
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
        EXPECTED: Betslip is shown with appropriate elements:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds are shown
        EXPECTED: - Updated Returns are shown
        """
        pass

    def test_007_tap_bet_now_buttonverify_that_bet_is_placed_and_boosted_odds(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        DESCRIPTION: Verify that bet is placed and boosted odds
        EXPECTED: Bet receipt is shown with appropriate elements:
        EXPECTED: - Odds boost title
        EXPECTED: - Boosted odds
        EXPECTED: - Total Stake: (amount)
        EXPECTED: **After OX99**: '- 2Lines at (Amount) per line' text is not shown
        """
        pass
