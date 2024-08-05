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
class Test_C163244_Verify_displaying_of_Next_Team_To_Score_Goal_market(Common):
    """
    TR_ID: C163244
    NAME: Verify displaying of 'Next Team To Score Goal' market
    DESCRIPTION: This test case verifies displaying of 'Next Team To Score' market
    PRECONDITIONS: 1. Add market for any Football event using 'Next Team To Score' market template and 'Next Team To Score' market name in TI
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Go to Football Landing page
    PRECONDITIONS: 4. Click/Tap on Competition Module header
    PRECONDITIONS: 5. Click/Tap on sub-category (Class ID) with Type ID's
    PRECONDITIONS: 6. Choose Competition (Type ID) that contains event from step 1
    PRECONDITIONS: Notes:
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_go_to_network___all___preview_and_find_templatemarketname_attribute_for_next_team_to_score_market_in_ss_response(self):
        """
        DESCRIPTION: Go to Network -> All -> Preview and find 'templateMarketName attribute' for "Next Team To Score" market in SS response
        EXPECTED: The following value is displayed in the SS response:
        EXPECTED: * templateMarketName="Next Team To Score"
        """
        pass

    def test_002_verify_if_value_is_available_for_football_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify if value is available for Football in the Market selector drop down
        EXPECTED: 'Next Team To Score' item is present in the Market selector drop down
        """
        pass

    def test_003_choose_next_team_to_score_item_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Choose 'Next Team To Score' item in the Market selector drop down
        EXPECTED: * Only event that contains 'Next Team To Score' market is displayed
        EXPECTED: * The fixture header for this market contains following titles:
        EXPECTED: * Home
        EXPECTED: * Away
        EXPECTED: * No Goal
        """
        pass

    def test_004_verify_if_goals_number_is_displayed_on_sports_card_under_priceodds_button_before_plus__markets_link(self):
        """
        DESCRIPTION: Verify if goals number is displayed on Sports card under Price/Odds button before "+ # Markets" link
        EXPECTED: Goals number is NOT displayed on Sports card
        """
        pass

    def test_005_edit_market_for_event_from_step_1_of_preconditions_and_add_goals_number_to_market_name_something_like_next_team_to_score_goal_1_in_ti(self):
        """
        DESCRIPTION: Edit market for event from step 1 of Preconditions and add goals number to market name, something like "Next Team To Score Goal 1" in TI
        EXPECTED: Changes are added successfully
        """
        pass

    def test_006_repeat_steps_1_2_for_the_same_event(self):
        """
        DESCRIPTION: Repeat steps 1-2 for the same event
        EXPECTED: 
        """
        pass

    def test_007_verify_if_goals_number_is_displayed_on_sports_card_under_priceodds_buttons(self):
        """
        DESCRIPTION: Verify if goals number is displayed on Sports card under Price/Odds buttons
        EXPECTED: Goals number is displayed on Sports card under Price/Odds buttons
        """
        pass

    def test_008_repeat_steps_1_4_for_different_number_of_goals(self):
        """
        DESCRIPTION: Repeat steps 1-4 for different number of goals
        EXPECTED: 
        """
        pass
