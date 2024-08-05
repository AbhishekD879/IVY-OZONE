import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C355733_Verify_displaying_of_Next_Team_To_Score_Goal_market_on_In_Play_page(Common):
    """
    TR_ID: C355733
    NAME: Verify displaying of 'Next Team To Score Goal' market on In-Play page
    DESCRIPTION: This test case verifies displaying of 'Next Team To Score Goal' market on In-Play page
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Create Football Event using 'Next Team To Score' market template and 'Next Team To Score' market name in TI
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Navigate to 'In-Play' page
    PRECONDITIONS: 3. Tap on 'Football' icon on Ribbon
    """
    keep_browser_open = True

    def test_001_go_to_network__gt_all__gt_preview_and_find_templatemarketname_attribute_for_next_team_to_score_market_in_ss_response(self):
        """
        DESCRIPTION: Go to Network -&gt; All -&gt; Preview and find 'templateMarketName attribute' for "Next Team To Score" market in SS response
        EXPECTED: The following value is displayed in the SS response for the event:
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

    def test_005_open_tiedit_market_for_the_event_and_add_goals_number_to_market_name_something_like_next_team_to_score_goal_1(self):
        """
        DESCRIPTION: Open TI
        DESCRIPTION: Edit market for the event and add goals number to market name, something like "Next Team To Score Goal 1"
        EXPECTED: Changes are added successfully
        """
        pass

    def test_006_back_to_the_app_and_refresh_the_pagerepeat_steps_1_4_for_the_same_event(self):
        """
        DESCRIPTION: Back to the app and refresh the page
        DESCRIPTION: Repeat steps 1-4 for the same event
        EXPECTED: 
        """
        pass

    def test_007_verify_if_goals_number_is_displayed_on_sports_card_under_priceodds_button_before_plus__markets_link(self):
        """
        DESCRIPTION: Verify if goals number is displayed on Sports card under Price/Odds button before "+ # Markets" link
        EXPECTED: Goals number is displayed on Sports card under Price/Odds button before "+ # Markets" link
        """
        pass

    def test_008_repeat_steps_1_7_for_in_play_tab_on_football_landing_page(self):
        """
        DESCRIPTION: Repeat steps 1-7 for In-Play tab on Football Landing page
        EXPECTED: 
        """
        pass
