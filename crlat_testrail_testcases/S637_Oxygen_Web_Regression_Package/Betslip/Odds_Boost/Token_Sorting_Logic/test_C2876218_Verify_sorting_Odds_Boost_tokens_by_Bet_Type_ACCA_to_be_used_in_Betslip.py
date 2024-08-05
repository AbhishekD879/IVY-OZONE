import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C2876218_Verify_sorting_Odds_Boost_tokens_by_Bet_Type_ACCA_to_be_used_in_Betslip(Common):
    """
    TR_ID: C2876218
    NAME: Verify sorting Odds Boost tokens by Bet Type (ACCA) to be used in Betslip
    DESCRIPTION: This Test Сase verifies that odds boost tokens are sorted by the Bet Type to be used on the Betslip
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Create THREE Odds Boost tokens with different Bet type using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Token1: Bet Type = ANY
    PRECONDITIONS: Token2: Bet Type = ACCA4
    PRECONDITIONS: Token3: Bet Type = ACCA6
    PRECONDITIONS: Add this tokens for User1 in  https://backoffice-tst2.coral.co.uk/office (Campaign Manager->Offers->Adhoc Tokens)
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add selection to Betslip
    """
    keep_browser_open = True

    def test_001_navigate_to_odds_boost_pageverify_that_3_tokens_are_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that 3 tokens are shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1
        EXPECTED: - Token2
        EXPECTED: - Token3
        """
        pass

    def test_002_navigate_to_betslipverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: BOOST button is shown
        """
        pass

    def test_003_tap_boost_buttonverify_that_boosted_odds_is_shown(self):
        """
        DESCRIPTION: Tap BOOST button
        DESCRIPTION: Verify that BOOSTED odds is shown
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is displayed as crossed out
        """
        pass

    def test_004_add_two_more_selection_to_betslipverify_that_boosted_odds_is_shown_for_singles_and_treble(self):
        """
        DESCRIPTION: Add TWO more selection to Betslip
        DESCRIPTION: Verify that BOOSTED odds is shown for SINGLES and TREBLE
        EXPECTED: - Boosted odds is shown for SINGLES and TREBLE
        EXPECTED: - Original odds is displayed as crossed out for SINGLES and TREBLE
        """
        pass

    def test_005_add_stake_to_singles_and_trebletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds_for_singles_and_treble(self):
        """
        DESCRIPTION: Add stake to Singles and Treble
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds for SINGLES and TREBLE
        EXPECTED: - Bet receipt is shown
        EXPECTED: - Odds Boost title is shown for SINGLES and TREBLE on bet receipt
        """
        pass

    def test_006_navigate_to_odds_boost_pageverify_that_token1_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that Token1 is not shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token2
        EXPECTED: - Token3
        """
        pass

    def test_007_add_3_selections_to_betslipverify_that_odds_boost_section_is_not_shown_in_betslip(self):
        """
        DESCRIPTION: Add 3 selections to Betslip
        DESCRIPTION: Verify that Odds Boost section is NOT shown in Betslip
        EXPECTED: BOOST button is NOT shown
        """
        pass

    def test_008_add_one_more_selection_to_betslipverify_that_odds_boost_section_is_shown_in_betslip(self):
        """
        DESCRIPTION: Add one more selection to Betslip
        DESCRIPTION: Verify that Odds Boost section is shown in Betslip
        EXPECTED: BOOST button is shown
        """
        pass

    def test_009_tap_boost_buttonverify_that_boosted_odds_is_shown_for_acca4_only(self):
        """
        DESCRIPTION: Tap BOOST button
        DESCRIPTION: Verify that BOOSTED odds is shown for ACCA4 only
        EXPECTED: Betslip is shown with appropriate elemens:
        EXPECTED: - BOOSTED button
        EXPECTED: - Boosted odds for ACCA4
        EXPECTED: - Original odds is displayed as crossed out for ACCA4
        EXPECTED: - 'i' is shown for SINGLES
        """
        pass

    def test_010_add_one_more_selection_to_betslipverify_that_boosted_odds_is_shown_for_acca5_only(self):
        """
        DESCRIPTION: Add one more selection to Betslip
        DESCRIPTION: Verify that BOOSTED odds is shown for ACCA5 only
        EXPECTED: Betslip is shown with appropriate elemens:
        EXPECTED: - BOOSTED button
        EXPECTED: - Boosted odds for ACCA5
        EXPECTED: - Original odds is displayed as crossed out for ACCA5
        EXPECTED: - 'i' is shown for SINGLES
        """
        pass

    def test_011_add_stake_to_singles_and_acca5tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_acca5_odds(self):
        """
        DESCRIPTION: Add stake to Singles and ACCA5
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted ACCA5 odds
        EXPECTED: - Bet receipt is shown
        EXPECTED: - Odds Boost title is shown for ACCA5 on bet receipt
        """
        pass

    def test_012_navigate_to_odds_boost_pageverify_that_token2_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that Token2 is not shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token3
        """
        pass

    def test_013_add_4_selection_to_betslipverify_that_odds_boost_section_is_not_shown_in_betslip(self):
        """
        DESCRIPTION: Add 4 selection to Betslip
        DESCRIPTION: Verify that Odds Boost section is NOT shown in Betslip
        EXPECTED: BOOST button is NOT shown
        """
        pass

    def test_014_add_2_more_selections_to_betslipverify_that_odds_boost_section_is_shown_in_betslip(self):
        """
        DESCRIPTION: Add 2 more selections to Betslip
        DESCRIPTION: Verify that Odds Boost section is shown in Betslip
        EXPECTED: BOOST button is shown
        """
        pass

    def test_015_tap_boost_buttonverify_that_boosted_odds_is_shown_for_acca6_only(self):
        """
        DESCRIPTION: Tap BOOST button
        DESCRIPTION: Verify that BOOSTED odds is shown for ACCA6 only
        EXPECTED: Betslip is shown with appropriate elemens:
        EXPECTED: - BOOSTED button
        EXPECTED: - Boosted odds for ACCA6
        EXPECTED: - Original odds is displayed as crossed out for ACCA6
        EXPECTED: - 'i' is shown for SINGLES
        """
        pass

    def test_016_add_stake_to_singles_and_acca6tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_acca6_odds(self):
        """
        DESCRIPTION: Add stake to Singles and ACCA6
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted ACCA6 odds
        EXPECTED: - Bet receipt is shown
        EXPECTED: - Odds Boost title is shown for ACCA6 on bet receipt
        """
        pass

    def test_017_navigate_to_odds_boost_pageverify_that_token1_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that Token1 is not shown
        EXPECTED: 0 tokens are shown on Odds Boost page
        """
        pass
