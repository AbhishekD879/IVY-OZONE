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
class Test_C60079217_Verify_event_displaying_when_selection_name_different_from_names_in_event_name_for_To_Qualify_market(Common):
    """
    TR_ID: C60079217
    NAME: Verify event displaying when selection name different from names in event name for To Qualify market
    DESCRIPTION: This test case verifies event displaying when selection name different from names in event name for To Qualify market
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use previously mentioned URL for creation the markets with following templateMarketName for a particular event:
    PRECONDITIONS: * Match Betting
    PRECONDITIONS: * To Qualify
    PRECONDITIONS: * Over/Under Total Goals (rawHandicapValue="2.5")
    PRECONDITIONS: * Both Teams to Score
    PRECONDITIONS: * Match Result and Both Teams To Score
    PRECONDITIONS: * Draw No Bet
    PRECONDITIONS: * First-Half Result
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Add 'To Qualify' market for event [1] where both of the selection names are NOT exactly the same as the names in the event name in TI
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Go to Football Landing page -> 'Matches' tab
    """
    keep_browser_open = True

    def test_001_verify_if_to_qualify_value_presents_in_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify if 'To Qualify' value presents in Market Selector drop down
        EXPECTED: 'To Qualify' value is NOT displayed in the Market Selector drop down
        """
        pass

    def test_002__open_ti_add_to_qualify_market_for_another_event_2_than_in_preconditions_where_both_of_the_selection_names_are_the_same_as_the_names_in_the_event_name(self):
        """
        DESCRIPTION: * Open TI.
        DESCRIPTION: * Add 'To Qualify' market for another event [2] than in Preconditions where both of the selection names are the same as the names in the event name.
        EXPECTED: Market is added successfully
        """
        pass

    def test_003__go_to_football_landing_page___matches_tab_verify_if_to_qualify_value_presents_in_market_selector_drop_down(self):
        """
        DESCRIPTION: * Go to Football Landing page -> 'Matches' tab.
        DESCRIPTION: * Verify if 'To Qualify' value presents in Market Selector drop down.
        EXPECTED: 'To Qualify' value is displayed in the Market Selector drop down
        """
        pass

    def test_004_select_to_qualify_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Select 'To Qualify' in the Market selector drop down
        EXPECTED: * Event [1] for selected market is NOT shown
        EXPECTED: * Event [2] for selected market is shown
        """
        pass

    def test_005_repeat_steps_1_4_on_competitions_page(self):
        """
        DESCRIPTION: Repeat steps 1-4 on 'Competitions' page
        EXPECTED: 
        """
        pass
