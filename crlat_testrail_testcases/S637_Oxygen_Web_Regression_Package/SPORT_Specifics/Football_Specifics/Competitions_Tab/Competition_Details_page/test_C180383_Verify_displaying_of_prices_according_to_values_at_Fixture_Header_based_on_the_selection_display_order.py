import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C180383_Verify_displaying_of_prices_according_to_values_at_Fixture_Header_based_on_the_selection_display_order(Common):
    """
    TR_ID: C180383
    NAME: Verify displaying of prices according to values at Fixture Header based on the selection display order
    DESCRIPTION: This test case verifies displaying of prices according to values at Fixture Header based on the selection display order on Football Competitions page
    PRECONDITIONS: To get ti tool use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/ti/
    PRECONDITIONS: To get SiteServer info about event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Note:
    PRECONDITIONS: An outcome that has the lowest display order number should have its price displayed under 'Home' value of Fixture Header, the outcome that has the second lowest display order number should have its price displayed under 'Draw' and the outcome that has the highest display order number should have its price displayed under 'Away'.
    PRECONDITIONS: The same logic applies for 'Home'/'Away'/'No Goal' - lowest display order number/second lowest display order number/highest display order number
    """
    keep_browser_open = True

    def test_001_load_ti_tool(self):
        """
        DESCRIPTION: Load ti tool
        EXPECTED: TI tool is loaded
        """
        pass

    def test_002_add_market_for_any_football_event_using_next_team_to_score_market_template_and_next_team_to_score_market_name(self):
        """
        DESCRIPTION: Add market for any Football event using 'Next Team To Score' market template and 'Next Team To Score' market name
        EXPECTED: Market is added successfully
        """
        pass

    def test_003_add_three_selections_to_market_from_step_2(self):
        """
        DESCRIPTION: Add three selections to market from step 2
        EXPECTED: Selections are added successfully
        """
        pass

    def test_004_set_different_display_order_number_for_previously_added_selections(self):
        """
        DESCRIPTION: Set different Display Order number for previously added selections
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_005_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_006_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: Football Landing page is opened
        """
        pass

    def test_007_clicktap_on_competition_module_header(self):
        """
        DESCRIPTION: Click/Tap on Competition Module header
        EXPECTED: List of sub-categories (Class ID's) is loaded
        """
        pass

    def test_008_clicktap_on_sub_category_class_id_with_type_ids(self):
        """
        DESCRIPTION: Click/Tap on sub-category (Class ID) with Type ID's
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: The leagues (Types) are displayed in list view within expanded Classes accordion
        EXPECTED: **For Desktop:**
        EXPECTED: The leagues (Types) are displayed in Horizontal position within expanded Classes accordion
        """
        pass

    def test_009_choose_league_type_that_contains_event_from_step_2(self):
        """
        DESCRIPTION: Choose league (Type) that contains event from step 2
        EXPECTED: List of Events is displayed
        """
        pass

    def test_010_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the 'Market selector' drop down
        EXPECTED: * The ‘Market Selector’ displayed within opened by default Matches section below the First level accordion
        EXPECTED: * 'Match Result' is selected by default in 'Market selector' drop down
        """
        pass

    def test_011_choose_next_team_to_score_item_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Choose 'Next Team To Score' item in the Market selector drop down
        EXPECTED: * Only event that contains 'Next Team To Score' market is displayed
        EXPECTED: * The fixture header for this market contains following titles:
        EXPECTED: * Home
        EXPECTED: * Away
        EXPECTED: * No Goal
        """
        pass

    def test_012_verify_if_priceodds_buttons_are_displayed_in_appropriate_order_according_to_set_display_order_number_in_step_4(self):
        """
        DESCRIPTION: Verify if 'Price/Odds' buttons are displayed in appropriate order according to set Display Order number in step 4
        EXPECTED: * Outcome with lowest display order number is displayed in column under 'Home' value
        EXPECTED: * Outcome with second lowest display order number is displayed in column under 'Away' value
        EXPECTED: * Outcome with highest display order number is displayed in column under 'No Goal' value
        """
        pass

    def test_013_repeat_steps_1_10_for_event_with_extra_time_result_market(self):
        """
        DESCRIPTION: Repeat steps 1-10 for event with 'Extra-Time Result' market
        EXPECTED: 
        """
        pass

    def test_014_choose_extra_time_result_item_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Choose 'Extra Time Result' item in the Market selector drop down
        EXPECTED: * Only event that contains 'Next Team To Score' market is displayed
        EXPECTED: * The fixture header for this market contains following titles:
        EXPECTED: * Home
        EXPECTED: * Draw
        EXPECTED: * Away
        """
        pass

    def test_015_verify_if_priceodds_buttons_are_displayed_in_appropriate_order_according_to_set_display_order_number(self):
        """
        DESCRIPTION: Verify if 'Price/Odds' buttons are displayed in appropriate order according to set Display Order number
        EXPECTED: * Outcome with lowest display order number is displayed in column under 'Home' value
        EXPECTED: * Outcome with second lowest display order number is displayed in column under 'Draw' value
        EXPECTED: * Outcome with highest display order number is displayed in column under 'Away' value
        """
        pass
