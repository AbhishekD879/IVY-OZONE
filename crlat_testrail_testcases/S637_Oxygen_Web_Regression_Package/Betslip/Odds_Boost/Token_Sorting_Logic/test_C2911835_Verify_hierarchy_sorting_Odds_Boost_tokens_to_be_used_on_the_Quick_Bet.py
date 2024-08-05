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
class Test_C2911835_Verify_hierarchy_sorting_Odds_Boost_tokens_to_be_used_on_the_Quick_Bet(Common):
    """
    TR_ID: C2911835
    NAME: Verify hierarchy sorting Odds Boost tokens to be used on the Quick Bet
    DESCRIPTION: This test case verifies that odds boost tokens are sorted by hierarchy level to be used in Quick Bet
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Create SEVEN Odds Boost tokens with Bet type (ANY) using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Create Redemption Values in https://backoffice-tst2.coral.co.uk/office (Campaign Manager->Offers->Redemption Values)
    PRECONDITIONS: For Example:
    PRECONDITIONS: **Value1** = Category level e.g. Football;
    PRECONDITIONS: **Value2** = Class level e.g. Football England;
    PRECONDITIONS: **Value3** = Type level e.g. Premier League;
    PRECONDITIONS: **Value4** = Event level e.g. Brighton vs Chelsea;
    PRECONDITIONS: **Value5** = Market level e.g. Match Result (market from event which is selected in Event level value);
    PRECONDITIONS: **Value6** = Selection level e.g. Draw (selection from market which is selected in Market level value)
    PRECONDITIONS: Add Odds Boost tokens for User1 selecting the appropriate Redemption Value: (This tokens are shown on Odds Boost page for USER1)
    PRECONDITIONS: **Token1 use Value1** (Token for Category);
    PRECONDITIONS: **Token2 use Value2** (Token for Class);
    PRECONDITIONS: **Token3 use Value3** (Token for Type);
    PRECONDITIONS: **Token4 use Value4** (Token for Event);
    PRECONDITIONS: **Token5 use Value5** (Token for Market);
    PRECONDITIONS: **Token6 use Value6** (Token for Selection);
    PRECONDITIONS: **Token7 use Value** = ANY (Token for ANY)
    PRECONDITIONS: (e.g. Token1 = Football; Token2 = Football England; Token3 = Premier League; Token4 = Brighton vs Chelsea; Token5 = Match Result; Token6 = Draw)
    PRECONDITIONS: Login with User1
    """
    keep_browser_open = True

    def test_001_add_appropriate_to_value6_selection_to_quick_betverify_that_odds_boost_is_available(self):
        """
        DESCRIPTION: Add appropriate to Value6 selection to Quick Bet
        DESCRIPTION: Verify that Odds Boost is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_002_tap_boost_buttonverify_that_odds_is_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds is boosted
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is displayed as crossed out
        """
        pass

    def test_003_tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds is shown
        """
        pass

    def test_004_navigate_to_odds_boost_pageverify_that_token6_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token6** is NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token7
        EXPECTED: - Token5
        EXPECTED: - Token4
        EXPECTED: - Token3
        EXPECTED: - Token2
        EXPECTED: - Token1
        """
        pass

    def test_005_add_selection_one_more_timeverify_that_odds_boost_is_available(self):
        """
        DESCRIPTION: Add selection one more time
        DESCRIPTION: Verify that odds boost is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_006_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds is shown
        """
        pass

    def test_007_navigate_to_odds_boost_pageverify_that_token5_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token5** is NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token7
        EXPECTED: - Token4
        EXPECTED: - Token3
        EXPECTED: - Token2
        EXPECTED: - Token1
        """
        pass

    def test_008_add_selection_one_more_timeverify_that_odds_boost_is_available(self):
        """
        DESCRIPTION: Add selection one more time
        DESCRIPTION: Verify that odds boost is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_009_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and Tap Place Bet button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds is shown
        """
        pass

    def test_010_navigate_to_odds_boost_pageverify_that_token4_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token4** is NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token7
        EXPECTED: - Token3
        EXPECTED: - Token2
        EXPECTED: - Token1
        """
        pass

    def test_011_add_new_selection_to_quick_bet_from_horse_racingverify_that_odds_boost_is_available(self):
        """
        DESCRIPTION: Add new selection to Quick Bet from Horse Racing
        DESCRIPTION: Verify that odds boost is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_012_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds is shown
        """
        pass

    def test_013_navigate_to_odds_boost_pageverify_that_token7_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token7** is NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token3
        EXPECTED: - Token2
        EXPECTED: - Token1
        """
        pass

    def test_014_add_selection_from_any_other_type_than_in_value3_other_than_premier_league_with_class_as_in_value2_football_england_to_quick_betverify_than_odds_boost_is_available(self):
        """
        DESCRIPTION: Add selection from any other Type than in Value3 (other than Premier League) with Class as in Value2 (Football England) to Quick Bet
        DESCRIPTION: Verify than odds boost is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_015_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and Tap Place Bet button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds is shown
        """
        pass

    def test_016_navigate_to_odds_boost_pageverify_that_token2_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token2** is NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token3
        EXPECTED: - Token1
        """
        pass

    def test_017_add_same_selection_one_more_timeverify_that_odds_boost_is_available(self):
        """
        DESCRIPTION: Add same selection one more time
        DESCRIPTION: Verify that odds boost is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_018_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds is shown
        """
        pass

    def test_019_navigate_to_odds_boost_pageverify_that_token1_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token1** is NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token3
        """
        pass
