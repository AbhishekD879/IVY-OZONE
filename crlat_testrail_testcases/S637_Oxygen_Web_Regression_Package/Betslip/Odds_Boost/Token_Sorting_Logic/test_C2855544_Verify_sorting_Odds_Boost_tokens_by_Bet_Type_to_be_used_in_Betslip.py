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
class Test_C2855544_Verify_sorting_Odds_Boost_tokens_by_Bet_Type_to_be_used_in_Betslip(Common):
    """
    TR_ID: C2855544
    NAME: Verify sorting Odds Boost tokens by Bet Type to be used in Betslip
    DESCRIPTION: This Test Сase verifies that odds boost tokens are sorted by the Bet Type to be used on the Betslip
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Create FOUR Odds Boost tokens with different Bet type using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Token1: Bet Type = ANY
    PRECONDITIONS: Token2: Bet Type = SINGLE
    PRECONDITIONS: Token3: Bet Type = DOUBLE
    PRECONDITIONS: Token4: Bet Type = TREBLE
    PRECONDITIONS: Add this tokens for User1 in  https://backoffice-tst2.coral.co.uk/office (Campaign Manager->Offers->Adhoc Tokens)
    """
    keep_browser_open = True

    def test_001_navigate_to_odds_boost_pageverify_that_4_tokens_are_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that 4 tokens are shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1
        EXPECTED: - Token2
        EXPECTED: - Token3
        EXPECTED: - Token4
        """
        pass

    def test_002_add_any_selection_to_betslipnavigate_to_betslipverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add any selection to Betslip
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_003_tap_boost_buttonverify_that_boosted_odds_is_shown(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that boosted odds is shown
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is displayed as crossed out
        """
        pass

    def test_004_add_one_more_selection_to_betslipverify_that_boosted_odds_is_shown_only__double(self):
        """
        DESCRIPTION: Add one more selection to Betslip
        DESCRIPTION: Verify that boosted odds is shown only  DOUBLE
        EXPECTED: - Boosted odds are shown only for DOUBLE
        EXPECTED: - Original odds are displayed as crossed out only for DOUBLE
        """
        pass

    def test_005_add_one_more_selection_to_betslipverify_that_boosted_odds_is_shown_only_for_treble(self):
        """
        DESCRIPTION: Add one more selection to Betslip
        DESCRIPTION: Verify that boosted odds is shown only for TREBLE
        EXPECTED: - Boosted odds are shown only for TREBELE
        EXPECTED: - Original odds are displayed as crossed out only for TREBLE
        """
        pass

    def test_006_add_stake_to_singles_and_trebletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add stake to Singles and Treble
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: - Bet receipt is shown
        EXPECTED: - Odds Boost title is shown for TREBLE on bet receipt
        """
        pass

    def test_007_navigate_to_odds_boost_pageverify_that_token4_token_for_treble_is_used(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token4 (Token for TREBLE) is used**
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1
        EXPECTED: - Token2
        EXPECTED: - Token3
        """
        pass

    def test_008_add_same_three_selections_to_betslipverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add same three selections to Betslip
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_009_tap_boost_buttonverify_that_boosted_odds_is_shown_for_treble_only(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that boosted odds is shown for TREBLE only
        EXPECTED: - Boosted odds is shown only for TREBLE
        EXPECTED: - Original odds is displayed as crossed out only for TREBLE
        EXPECTED: - 'i' is shown for SINGLES
        """
        pass

    def test_010_add_stake_to_singles_and_trebletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add stake to Singles and Treble
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: - Bet receipt is shown
        EXPECTED: - Odds Boost title is shown only for TREBLE on bet receipt
        """
        pass

    def test_011_navigate_to_odds_boost_pageverify_that_token3_token_for_double_is_used_and_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token3 (Token for DOUBLE) is used** and not shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1
        EXPECTED: - Token2
        """
        pass

    def test_012_add_same_three_selections_to_betslipverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add same three selections to Betslip
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_013_tap_boost_buttonverify_that_boosted_odds_is_shown_for_singles_and_treble(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that boosted odds is shown for SINGLES and TREBLE
        EXPECTED: - Boosted odds is shown for SINGLES and TREBLE
        EXPECTED: - Original odds is displayed as crossed out for SINGLES and TREBLE
        """
        pass

    def test_014_add_stake_to_singles_and_trebletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add stake to Singles and Treble
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: - Bet receipt is shown
        EXPECTED: - Odds Boost title is shown for SINGLES and TREBLE on bet receipt
        """
        pass

    def test_015_navigate_to_odds_boost_pageverify_that_token2_token_for_single_is_used_and_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token2 (Token for SINGLE) is used** and not shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1
        """
        pass
