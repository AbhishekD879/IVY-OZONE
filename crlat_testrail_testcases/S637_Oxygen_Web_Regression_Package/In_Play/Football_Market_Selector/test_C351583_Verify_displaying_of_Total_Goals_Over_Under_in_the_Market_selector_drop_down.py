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
class Test_C351583_Verify_displaying_of_Total_Goals_Over_Under_in_the_Market_selector_drop_down(Common):
    """
    TR_ID: C351583
    NAME: Verify displaying of Total Goals Over/Under in the Market selector drop down
    DESCRIPTION: This test case verifies displaying of Total Goals Over/Under in the Market selector drop down with different "rawHandicapValue" values
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following marketTemplates:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |Next Team to Score| - "Next Team to Score"
    PRECONDITIONS: * |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: * |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 1.5"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 2.5"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 3.5"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 4.5"
    PRECONDITIONS: * |To Qualify| - "To Qualify"
    PRECONDITIONS: * |Penalty Shoot-Out Winner| - "Penalty Shoot-Out Winner"
    PRECONDITIONS: * |Extra-Time Result| - "Extra Time Result"
    PRECONDITIONS: * |Draw No Bet| - "Draw No Bet"
    PRECONDITIONS: * |First-Half Result| - "1st Half Result"
    PRECONDITIONS: 2) Be aware that market switching using 'Market Selector' is applied only for events from the 'Live Now' section
    PRECONDITIONS: 3) To check the available options in 'Market Selector' use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORTS::XX::LIVE_EVENT"
    PRECONDITIONS: where:
    PRECONDITIONS: XX - Category ID
    PRECONDITIONS: ![](index.php?/attachments/get/10272745)
    PRECONDITIONS: 4) To check the availability of selected market in 'Market Selector' from dropdown list use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::{templateMarketName}::XXX"
    PRECONDITIONS: where:
    PRECONDITIONS: XX - Category ID
    PRECONDITIONS: XXX - Type ID
    PRECONDITIONS: ![](index.php?/attachments/get/18576769)
    PRECONDITIONS: 5) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the 'In-Play' page
    PRECONDITIONS: 3. Choose the 'Football' tab
    """
    keep_browser_open = True

    def test_001_in_the_ob_system_add_overunder_total_goals_market_with_rawhandicapvalue__15_for_any_football_event(self):
        """
        DESCRIPTION: In the OB system add 'Over/Under Total Goals' market with "rawHandicapValue" = 1.5 for any Football event
        EXPECTED: Market is added successfully
        """
        pass

    def test_002_back_to_the_app_refresh_the_page_and_check_if_total_goals_overunder_15_option_is_available_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Back to the app, refresh the page and check if 'Total Goals Over/Under 1.5' option is available in the 'Market Selector' dropdown list
        EXPECTED: 'Total Goals Over/Under 1.5' option is present in the 'Market Selector' dropdown list
        """
        pass

    def test_003_select_the_total_goals_overunder_15_option_from_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select the 'Total Goals Over/Under 1.5' option from the 'Market Selector' dropdown list
        EXPECTED: * Event for the selected market is shown
        EXPECTED: * Values on Fixture header are changed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: * templateMarketName="Total Goals Over/Under" and rawHandicapValue="1.5" are received in the response
        """
        pass

    def test_004_repeat_steps_1_3_but_add_the_overunder_total_goals_market_with_different_rawhandicapvalue_values_253545(self):
        """
        DESCRIPTION: Repeat steps 1-3 but add the 'Over/Under Total Goals' market with different "rawHandicapValue" values (2.5;3.5;4.5)
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_1_2_but_add_overunder_total_goals_market_with_rawhandicapvalue__15253545_for_example_05_for_the_event_from_another_competition(self):
        """
        DESCRIPTION: Repeat steps 1-2 but add 'Over/Under Total Goals' market with "rawHandicapValue" != 1.5/2.5/3.5/4.5 (for example 0.5) for the event from another competition
        EXPECTED: 'Total Goals Over/Under X.X' option is NOT present in the 'Market Selector' dropdown list
        """
        pass

    def test_006_repeat_steps_1_5_on_football_landing_page__gt_in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-5 on 'Football Landing Page' -&gt; 'In-Play' tab
        EXPECTED: 
        """
        pass
