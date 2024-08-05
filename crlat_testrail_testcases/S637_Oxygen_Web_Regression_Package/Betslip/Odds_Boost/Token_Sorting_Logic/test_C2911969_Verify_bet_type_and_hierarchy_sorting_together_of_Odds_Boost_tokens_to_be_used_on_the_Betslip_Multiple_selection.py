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
class Test_C2911969_Verify_bet_type_and_hierarchy_sorting_together_of_Odds_Boost_tokens_to_be_used_on_the_Betslip_Multiple_selection(Common):
    """
    TR_ID: C2911969
    NAME: Verify bet type and hierarchy sorting together of Odds Boost tokens to be used on the Betslip (Multiple selection)
    DESCRIPTION: This Test Сase verifies that odds boost tokens are sorted by the Bet Type  and then by hierarchy to be used on the Betslip
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Create Odds Boost tokens with different Bet type using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: **Token1**: Bet Type = ANY
    PRECONDITIONS: **Token1a**: Bet Type = ANY
    PRECONDITIONS: **Token1b**: Bet Type = ANY
    PRECONDITIONS: **Token2**: Bet Type = SINGLE
    PRECONDITIONS: **Token3**: Bet Type = DOUBLE
    PRECONDITIONS: **Token4**: Bet Type = TREBLE
    PRECONDITIONS: Create Redemption Values in https://backoffice-tst2.coral.co.uk/office (Campaign Manager->Offers->Redemption Values)
    PRECONDITIONS: For Example:
    PRECONDITIONS: **Value1** = Class level e.g. Football England;
    PRECONDITIONS: **Value2** = Type level e.g. Premier League;
    PRECONDITIONS: **Value3** = Event level e.g. Brighton vs Chelsea (event from Class in Value2 (from Premier League);
    PRECONDITIONS: Add this tokens for USER1 in https://backoffice-tst2.coral.co.uk/office (Campaign Manager->Offers->Adhoc Tokens)
    PRECONDITIONS: Add **Token1** (Bet Type=ANY)  with Value = ANY
    PRECONDITIONS: Add **Token1a** (Bet Type=ANY) with Value = Value2 (expiration date = Tomorrow at 12:02)
    PRECONDITIONS: Add **Token1b** (Bet Type=ANY) with Value = Value2 (expiration date = Tomorrow at 12:01)
    PRECONDITIONS: Add **Token2** (Bet Type=SINGLE) with Value = Value3 (expiration date = Tomorrow at 12:00)
    PRECONDITIONS: Add **Token3** (Bet Type=DOUBLE) with Value = Value2
    PRECONDITIONS: Add **Token4** (Bet Type=TREBLE) with Value = Value1
    PRECONDITIONS: Login with USER1
    """
    keep_browser_open = True

    def test_001_add_selection_to_betslip_appropriate_to_event_in_value3verify_that_boost_section_is_available(self):
        """
        DESCRIPTION: Add selection to Betslip appropriate to Event in Value3
        DESCRIPTION: Verify that boost section is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_002_add_stake_and_tap_boost_buttonverify_that_odds_are_boosted(self):
        """
        DESCRIPTION: Add Stake and tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted
        EXPECTED: - Boosted odds are shown
        EXPECTED: - Original odds are displayed as crossed out
        """
        pass

    def test_003_add_one_more_selection_from_type_appropriate_to_value2_premier_leagueverify_that_only_double_is_boosted(self):
        """
        DESCRIPTION: Add one more selection from Type appropriate to Value2 (Premier League)
        DESCRIPTION: Verify that only DOUBLE is boosted
        EXPECTED: - Boosted odds is shown only for DOUBLE
        EXPECTED: - 'i' icon is shown for singles
        EXPECTED: - Original odds are displayed as crossed out only for DOUBLE
        """
        pass

    def test_004_add_stake_for_singles_and_doubletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake for SINGLES and DOUBLE
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with odds boost section and boosted odds for the DOUBLE bet is shown
        """
        pass

    def test_005_navigate_to_odds_boost_pageverify_that_double_token_is_usedtoken3_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that DOUBLE token is used
        DESCRIPTION: **Token3 is NOT shown**
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1
        EXPECTED: - Token1a
        EXPECTED: - Token1b
        EXPECTED: - Token2
        EXPECTED: - Token4
        """
        pass

    def test_006_add_same_two_selections_to_betslip_andverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add SAME two selections to Betslip and
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_007_tap_boost_buttonverify_that_singles_and_double_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that SINGLES and DOUBLE are boosted
        EXPECTED: - Boosted odds are shown for SINGLES and DOUBLE
        EXPECTED: - Original odds are displayed as crossed out for SINGLES and DOUBLE
        """
        pass

    def test_008_add_stake_for_singles_and_doubletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake for SINGLES and DOUBLE
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with odds boost section and boosted odds for SINGLES and DOUBLE is shown
        """
        pass

    def test_009_navigate_to_odds_boost_pageverify_that_token_value__any_is_usedtoken1_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that token Value = ANY is used
        DESCRIPTION: **Token1 is NOT shown**
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1a
        EXPECTED: - Token1b
        EXPECTED: - Token2
        EXPECTED: - Token4
        """
        pass

    def test_010_add_same_two_selections_to_betslip_andverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add SAME two selections to Betslip and
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_011_tap_boost_buttonverify_that_selection_from_event_in_value3_and_double_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that selection from Event in Value3 and DOUBLE are boosted
        EXPECTED: - Boosted odds is shown for SINGLE (Event from Value3) and DOUBLE
        EXPECTED: - 'i' icon is shown for other SINGLE selection
        EXPECTED: - Original odds are displayed as crossed out for SINGLE (Event from Value3) and DOUBLE
        """
        pass

    def test_012_add_stake_for_singles_and_doubletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake for SINGLES and DOUBLE
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds is shown for SINGLE (Event from Value3) and DOUBLE
        """
        pass

    def test_013_navigate_to_odds_boost_pageverify_that_token2_for_event_level_is_usedtoken2_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that Token2 (for event level) is used
        DESCRIPTION: **Token2 is NOT shown**
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1a
        EXPECTED: - Token1b
        EXPECTED: - Token4
        """
        pass

    def test_014_add_4_selections_to_betslip_from_type_appropriate_to_value2_premier_leagueverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add 4 selections to Betslip from Type appropriate to Value2 (Premier League)
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_015_add_stake_for_singles_and_doubletap_boost_buttonverify_that_only_acca4_is_boosted(self):
        """
        DESCRIPTION: Add Stake for SINGLES and DOUBLE
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that only ACCA4 is boosted
        EXPECTED: - Boosted odds is shown only for ACCA4
        EXPECTED: - 'i' icon is shown for SINGLES
        EXPECTED: - Original odds are displayed as crossed out only for ACCA4
        """
        pass

    def test_016_tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds for ACCA4 is shown
        """
        pass

    def test_017_navigate_to_odds_boost_pageverify_that_token4_for_trebletoken4_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that Token4 (for TREBLE)
        DESCRIPTION: **Token4 is NOT shown**
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1a
        EXPECTED: - Token1b
        """
        pass

    def test_018_in_ti_add___token1__any_expiration_date__tomorrow_any_time_to_user(self):
        """
        DESCRIPTION: In TI add - Token1 = ANY (expiration date = Tomorrow any time) to User
        EXPECTED: 
        """
        pass

    def test_019_navigate_back_to_applicationodds_boost_pageverify_that_just_add_token1_is_shown(self):
        """
        DESCRIPTION: Navigate back to application>Odds Boost page
        DESCRIPTION: Verify that just add Token1 is shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1
        EXPECTED: - Token1a
        EXPECTED: - Token1b
        """
        pass

    def test_020_add_2_selections_from_type_appropriate_to_value2_premier_league_and_one_selection_from_any_other_typeverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add 2 selections from Type appropriate to Value2 (Premier League) and one selection from any other Type
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_021_ttap_boost_buttonverify_that_odds_are_boosted_for_singles_and_treble(self):
        """
        DESCRIPTION: Ttap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted for SINGLES and TREBLE
        EXPECTED: - Boosted odds are shown for SINGLES and TREBLE
        EXPECTED: - Original odds are displayed as crossed out for SINGLES and TREBLE
        """
        pass

    def test_022_add_stake_for_singles_and_trebletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake for SINGLES and TREBLE
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with odds boost section and boosted odds for SINGLES and TREBLE is shown
        """
        pass

    def test_023_navigate_to_odds_boost_pageverify_that_token1_for_anytoken1_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that Token1 (for ANY)
        DESCRIPTION: **Token1 is NOT shown**
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1a
        EXPECTED: - Token1b
        """
        pass

    def test_024_add_same_selections_as_in_step20_to_betslipverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add same selections as in step#20 to Betslip
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_025_tap_boost_buttonverify_that_odds_are_boosted_for_singles_from_value2_premier_league_and_treble(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted for SINGLES from Value2 (Premier League) and TREBLE
        EXPECTED: - Boosted odds are shown for SINGLES from Value2 (Premier League) and TREBLE
        EXPECTED: - Original odds are displayed as crossed out for SINGLES from Value2 (Premier League) and TREBLE
        """
        pass

    def test_026_add_stake_for_singles_and_trebletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake for SINGLES and TREBLE
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with odds boost section and boosted odds for SINGLES from Value2 (Premier League) and TREBLE is shown
        """
        pass

    def test_027_navigate_to_odds_boost_pageverify_that_token_with_an_earlier_expiration_date_is_usedtoken1b_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that Token with an earlier expiration date is used
        DESCRIPTION: **Token1b is NOT shown**
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1a
        """
        pass
