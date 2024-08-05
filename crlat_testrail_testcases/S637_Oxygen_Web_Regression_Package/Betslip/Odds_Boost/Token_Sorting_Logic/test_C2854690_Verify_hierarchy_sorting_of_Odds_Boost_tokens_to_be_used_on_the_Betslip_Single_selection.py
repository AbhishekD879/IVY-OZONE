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
class Test_C2854690_Verify_hierarchy_sorting_of_Odds_Boost_tokens_to_be_used_on_the_Betslip_Single_selection(Common):
    """
    TR_ID: C2854690
    NAME: Verify hierarchy sorting of Odds Boost tokens to be used on the Betslip (Single selection)
    DESCRIPTION: This Test Сase verifies that odds boost tokens are sorted by the hierarchy to be used on the Betslip
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Create SEVEN Odds Boost tokens with Bet type (ANY) using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Create Redemption Values in OB:
    PRECONDITIONS: Coral: https://backoffice-tst2.coral.co.uk/office;
    PRECONDITIONS: Ladbrokes: https://tst2-backoffice-lcm.ladbrokes.com/office
    PRECONDITIONS: (Campaign Manager->Offers->Redemption Values)
    PRECONDITIONS: For Example:
    PRECONDITIONS: **Value1** = Category level e.g. Football;
    PRECONDITIONS: **Value2** = Class level e.g. Football England;
    PRECONDITIONS: **Value3** = Type level e.g. Premier League;
    PRECONDITIONS: **Value4** = Event level e.g. Brighton vs Chelsea;
    PRECONDITIONS: **Value5** = Market level e.g. Match Result (market from event which is selected in Event level value);
    PRECONDITIONS: **Value6** = Selection level e.g. Draw (selection from market which is selected in Market level value)
    PRECONDITIONS: Add Odds Boost tokens (Campaign Manager->Adhoc Tokens) for User1 selecting the appropriate Redemption Value, DO NOT set any expiration date(in this case token will be added for 1 day):
    PRECONDITIONS: **Token1** use Value1 (Token for Category);
    PRECONDITIONS: **Token2** use Value2 (Token for Class);
    PRECONDITIONS: **Token3** use Value3 (Token for Type);
    PRECONDITIONS: **Token4** use Value 4 (Token for Event);
    PRECONDITIONS: **Token5** use Value5 (Token for Market);
    PRECONDITIONS: **Token6** use Value6 (Token for Selection);
    PRECONDITIONS: **Token7** use Value = ANY (Token for ANY)
    PRECONDITIONS: (e.g. Token1 = Football; Token2 = Football England; Token3 = Premier League; Token4 = Brighton vs Chelsea; Token5 = Match Result; Token6 = Draw)
    PRECONDITIONS: Login with User1
    """
    keep_browser_open = True

    def test_001_add_a_single_selection_appropriate_to_selection_in_value6_to_the_betslipverify_that_odds_boost_section_is_available(self):
        """
        DESCRIPTION: Add a single selection (appropriate to selection in Value6) to the Betslip
        DESCRIPTION: Verify that odds boost section is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_002_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds is shown
        """
        pass

    def test_003_navigate_to_odds_boost_pageverify_that_token6_token_for_selection_is_used_and_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token6 (Token for Selection) is used** and NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token7
        EXPECTED: - Token5
        EXPECTED: - Token4
        EXPECTED: - Token3
        EXPECTED: - Token2
        EXPECTED: - Token1
        """
        pass

    def test_004_add_same_selection_one_more_timeverify_that_odds_boost_section_is_available(self):
        """
        DESCRIPTION: Add same selection one more time
        DESCRIPTION: Verify that odds boost section is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_005_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake, tap 'BOOST' button and tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds is shown
        """
        pass

    def test_006_navigate_to_odds_boost_pageverify_that_token5_token_for_market_is_used_and_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token5 (Token for Market) is used** and NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token7
        EXPECTED: - Token4
        EXPECTED: - Token3
        EXPECTED: - Token2
        EXPECTED: - Token1
        """
        pass

    def test_007_add_same_selection_one_more_timeverify_that_odds_boost_section_is_available(self):
        """
        DESCRIPTION: Add same selection one more time
        DESCRIPTION: Verify that odds boost section is available
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_008_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds is shown
        """
        pass

    def test_009_navigate_to_odds_boost_pageverify_that_token4_token_for_event_is_used_and__not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token4 (token for Event) is used** and  NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token7
        EXPECTED: - Token3
        EXPECTED: - Token2
        EXPECTED: - Token1
        """
        pass

    def test_010_add_selection_to_betslip_other_than_class_in_value2_other_than_football_england_and_from_the_same_category_that_in_value1_footballverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add selection to Betslip OTHER THAN Class in Value2 (other than Football England) and from the same Category that in Value1 (Football)
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_011_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds is shown
        """
        pass

    def test_012_navigate_to_odds_boost_pageverify_that_token1_token_for_category_is_used_and_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token1 (token for Category) is used** and NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token7
        EXPECTED: - Token3
        EXPECTED: - Token2
        """
        pass

    def test_013_add_selection_to_betslip_appropriate_to_type_in_value3_premier_leaguenavigate_to_betslipverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add selection to Betslip appropriate to Type in Value3 (Premier League)
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_014_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds is shown
        """
        pass

    def test_015_navigate_to_odds_boost_pageverify_that_token3_token_for_type_is_used_and_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token3 (token for Type) is used** and NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token7
        EXPECTED: - Token2
        """
        pass

    def test_016_add_selection_to_betslip_appropriate_to_class_in_value2_football_englandverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add selection to Betslip appropriate to Class in Value2 (Football England)
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_017_add_stake_tap_boost_button_and_tap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add Stake, Tap 'BOOST' button and Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt with boost section and boosted odds is shown
        """
        pass

    def test_018_navigate_to_odds_boost_pageverify_that_token2_token_for_class_is_used_and_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token2 (token for Class) is used** and NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token7
        """
        pass
