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
class Test_C2912300_Verify_hierarchy_sorting_of_Odds_Boost_tokens_to_be_used_in_Betslip_Multiple_selections(Common):
    """
    TR_ID: C2912300
    NAME: Verify hierarchy sorting of Odds Boost tokens to be used in Betslip (Multiple selections)
    DESCRIPTION: This Test Сase verifies that odds boost tokens are sorted by the hierarchy to be used on the Betslip for Multiple selection
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Create Redemption Values (RV) in OB
    PRECONDITIONS: Coral: https://backoffice-tst2.coral.co.uk/office;
    PRECONDITIONS: Ladbrokes: https://tst2-backoffice-lcm.ladbrokes.com/office
    PRECONDITIONS: (Campaign Manager->Offers->Redemption Values)
    PRECONDITIONS: Redemption Values for Event level:
    PRECONDITIONS: **RV1 = Event1** (Event1 is from **Class1** e.g Event from Premier League)
    PRECONDITIONS: **RV2 = Event2** (Event2 is from **Class2** e.g Event from Championship)
    PRECONDITIONS: **RV3 = Event3** (Event3 is from **Class2** e.g Event from Championship)
    PRECONDITIONS: Redemption Values for Class level:
    PRECONDITIONS: **RV4 = Class1** (Class1 from Category1 e.g. Football England)
    PRECONDITIONS: **RV5 = Class3** (Class3 from Category1 e.g. Football Spain)
    PRECONDITIONS: Create Redemption Values for Categories
    PRECONDITIONS: **RV6 = Category1** (value for Football category)
    PRECONDITIONS: Create SEVEN Odds Boost tokens with Bet type (ANY) using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Add tokens(name of token is different) where **Bet Type = ANY** with this Remediation Values to USER1:
    PRECONDITIONS: - **Token1 = ANY** (expiration date = Tomorrow any time)
    PRECONDITIONS: - **A_Token1 = RV1** (expiration date = Tomorrow 12:01)
    PRECONDITIONS: - **B_Token2 = RV2** (expiration date = Tomorrow 12:00)
    PRECONDITIONS: - **C_Token3 = RV3** (expiration date = Tomorrow 12:00)
    PRECONDITIONS: - **D_Token4 = RV4** (expiration date = Tomorrow 12:00)
    PRECONDITIONS: - **E_Token5 = RV5** (expiration date = Tomorrow 12:01)
    PRECONDITIONS: - **D_Token6 = RV6** (expiration date = Tomorrow 12:00)
    PRECONDITIONS: Login with USER1
    """
    keep_browser_open = True

    def test_001_add_selections_to_betslip1___from_event1_appropriate_to_rv1_in_token12___from_event2_appropriate_to_rv2_in_token23___from_event3_appropriate_to_rv3_in_token3verify_that_adds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add selections to Betslip:
        DESCRIPTION: 1 - from Event1 (appropriate to RV1 in Token1)
        DESCRIPTION: 2 - from Event2 (appropriate to RV2 in Token2)
        DESCRIPTION: 3 - from Event3 (appropriate to RV3 in Token3)
        DESCRIPTION: Verify that adds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_002_tap_boost_buttonverify_that_all_selections_and_treble_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that ALL selections and TREBLE are boosted
        EXPECTED: - Boosted odds is shown for ALL selections and TREBLE
        EXPECTED: - Original odds is displayed as crossed out for ALL selections and TREBLE
        """
        pass

    def test_003_add_stakes_to_all_singles_and_trebletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add stakes to all SINGLES and TREBLE
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt is shown
        EXPECTED: Boost section and boosted odds are shown for ALL selections and TREBLE
        """
        pass

    def test_004_navigate_to_odds_boost_pageverify_that_token1_token_for_any_is_used_and_not_shownnote_before_ox100_token1_will_be_used_the_last_in_this_step_b_token2_will_be_used(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token1 (token for ANY) is used** and NOT shown
        DESCRIPTION: NOTE: **before OX100** Token1 will be used the last. In this step, B_Token2 will be used
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - A_Token1
        EXPECTED: - B_Token2
        EXPECTED: - C_Token3
        EXPECTED: - D_Token4
        EXPECTED: - E_Token5
        EXPECTED: - D_Token6
        """
        pass

    def test_005_add_the_same_selections_to_betslip_as_in_step11___from_event1_appropriate_to_rv1_in_token12___from_event2_appropriate_to_rv2_in_token23___from_event3_appropriate_to_rv3_in_token3verify_that_adds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add the same selections to Betslip as in step#1:
        DESCRIPTION: 1 - from Event1 (appropriate to RV1 in Token1)
        DESCRIPTION: 2 - from Event2 (appropriate to RV2 in Token2)
        DESCRIPTION: 3 - from Event3 (appropriate to RV3 in Token3)
        DESCRIPTION: Verify that adds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_006_tap_boost_buttonverify_that_only_selection_from_event2_and_treble_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that only selection from Event2 and TREBLE are boosted
        EXPECTED: - Boosted odds is shown for selection from Event2 and TREBLE
        EXPECTED: - Original odds is displayed as crossed out for selection from Event2 and TREBLE
        EXPECTED: - 'i' icon is shown for selections from Event1 and Event3
        """
        pass

    def test_007_add_stakes_to_all_singles_and_trebletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add stakes to all SINGLES and TREBLE
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt is shown
        EXPECTED: Boost section and boosted odds are shown for selection from Event2 and TREBLE
        """
        pass

    def test_008_navigate_to_odds_boost_pageverify_that_b_token2_token_for_event_is_used_and_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **B_Token2 (token for Event) is used** and NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - A_Token1
        EXPECTED: - C_Token3
        EXPECTED: - D_Token4
        EXPECTED: - E_Token5
        EXPECTED: - D_Token6
        """
        pass

    def test_009_add_the_same_selections_to_betslip_as_in_step11___from_event1_appropriate_to_rv1_in_token12___from_event2_appropriate_to_rv2_in_token23___from_event3_appropriate_to_rv3_in_token3verify_that_adds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add the same selections to Betslip as in step#1
        DESCRIPTION: 1 - from Event1 (appropriate to RV1 in Token1)
        DESCRIPTION: 2 - from Event2 (appropriate to RV2 in Token2)
        DESCRIPTION: 3 - from Event3 (appropriate to RV3 in Token3)
        DESCRIPTION: Verify that adds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_010_tap_boost_buttonverify_that_only_selection_from_event3_and_treble_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that only selection from Event3 and TREBLE are boosted
        EXPECTED: - Boosted odds is shown for selection from Event3 and TREBLE
        EXPECTED: - Original odds is displayed as crossed out for selection from Event3 and TREBLE
        EXPECTED: - 'i' icon is shown for selections from Event1 and Event2
        """
        pass

    def test_011_add_stakes_to_all_singles_and_trebletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add stakes to all SINGLES and TREBLE
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt is shown
        EXPECTED: Boost section and boosted odds are shown for selection from Event3 and TREBLE
        """
        pass

    def test_012_navigate_to_odds_boost_pageverify_that_c_token3_token_for_event_is_used_and_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **C_Token3 (token for Event) is used** and NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - A_Token1
        EXPECTED: - D_Token4
        EXPECTED: - E_Token5
        EXPECTED: - D_Token6
        """
        pass

    def test_013_add_two_selections_to_betslip1___from_class_in_rv4_in_token4_selection_from_football_england2___from_class_in_rv5_in_token5_selection_from_football_spainnote_do_not_add_selection_from_event1_appropriate_to_rv1_in_token1verify_that_adds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add TWO selections to Betslip:
        DESCRIPTION: 1 - from Class in RV4 in Token4 (selection from Football England)
        DESCRIPTION: 2 - from Class in RV5 in Token5 (selection from Football Spain)
        DESCRIPTION: NOTE: do NOT add selection from Event1 (appropriate to RV1 in Token1)
        DESCRIPTION: Verify that adds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_014_tap_boost_buttonverify_that_selection_from_class_in_rv4_football_england_and_double_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that selection from Class in RV4 (Football England) and DOUBLE are boosted
        EXPECTED: - Boosted odds is shown for selection from Class in RV4 (selection from Football England) and DOUBLE
        EXPECTED: - Original odds is displayed as crossed out for selection from Class in RV4 (selection from Football England) and DOUBLE
        EXPECTED: - 'i' icon is shown for selection from Class in RV5 (selection from Football Spain)
        """
        pass

    def test_015_add_stakes_to_all_singles_and_doubletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add stakes to all SINGLES and DOUBLE
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt is shown
        EXPECTED: Boost section and boosted odds are shown for selection from Class in RV4 (selection from Football England) and DOUBLE
        """
        pass

    def test_016_navigate_to_odds_boost_pageverify_that_d_token4_token_for_class_is_used_and_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **D_Token4 (token for Class) is used** and NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - A_Token1
        EXPECTED: - E_Token5
        EXPECTED: - D_Token6
        """
        pass

    def test_017_in_ti_add___token1__any_expiration_date__tomorrow_any_time_to_user(self):
        """
        DESCRIPTION: In TI add - **Token1 = ANY** (expiration date = Tomorrow any time) to User
        EXPECTED: 
        """
        pass

    def test_018_navigate_back_to_applicationodds_boost_pageverify_that_just_add_token1_is_shown(self):
        """
        DESCRIPTION: Navigate back to application>Odds Boost page
        DESCRIPTION: Verify that just add Token1 is shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - Token1
        EXPECTED: - A_Token1
        EXPECTED: - E_Token5
        EXPECTED: - D_Token6
        """
        pass

    def test_019_add_the_same_selections_as_in_step13_to_betslipverify_that_adds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add the same selections as in step#13 to Betslip
        DESCRIPTION: Verify that adds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_020_tap_boost_buttonverify_that_singles_and_double_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that SINGLES and DOUBLE are boosted
        EXPECTED: - Boosted odds is shown for SINGLES and DOUBLE
        EXPECTED: - Original odds is displayed as crossed out for SINGLES and DOUBLE
        """
        pass

    def test_021_add_stakes_to_all_singles_and_doubletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add stakes to all SINGLES and DOUBLE
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt is shown
        EXPECTED: Boost section and boosted odds are shown for SINGLES and DOUBLE
        """
        pass

    def test_022_navigate_to_odds_boost_pageverify_that_token1_token_for_any_is_used_and_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **Token1 (token for ANY) is used** and NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - A_Token1
        EXPECTED: - E_Token5
        EXPECTED: - D_Token6
        """
        pass

    def test_023_add_two_selections_from_any_football_class_other_than_class_in_rv5_in_token5_other_than_football_spain_and_other_than_event_in_value1verify_that_adds_boost_section_is_shown(self):
        """
        DESCRIPTION: Add two selections from any Football Class other than Class in RV5 in Token5 (Other than Football Spain) and other than Event in Value1
        DESCRIPTION: Verify that adds boost section is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_024_tap_boost_buttonverify_that_all_selection_and_double_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that all selection and DOUBLE are boosted
        EXPECTED: - Boosted odds is shown for ALL selections and DOUBLE
        EXPECTED: - Original odds is displayed as crossed out for ALL selections and DOUBLE
        """
        pass

    def test_025_add_stakes_to_all_singles_and_doubletap_place_bet_buttonverify_that_bet_is_placed_with_boosted_odds(self):
        """
        DESCRIPTION: Add stakes to all SINGLES and DOUBLE
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with boosted odds
        EXPECTED: Bet receipt is shown
        EXPECTED: Boost section and boosted odds are shown for ALL selections and DOUBLE
        """
        pass

    def test_026_navigate_to_odds_boost_pageverify_that_d_token6_token_for_category_is_used_and_not_shown(self):
        """
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that **D_Token6 (token for Category) is used** and NOT shown
        EXPECTED: Odds Boost page is shown with odds boost tokens:
        EXPECTED: - A_Token1
        EXPECTED: - E_Token5
        """
        pass
