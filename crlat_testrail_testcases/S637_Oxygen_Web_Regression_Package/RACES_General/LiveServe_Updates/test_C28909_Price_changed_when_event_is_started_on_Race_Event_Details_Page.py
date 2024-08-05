import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28909_Price_changed_when_event_is_started_on_Race_Event_Details_Page(Common):
    """
    TR_ID: C28909
    NAME: Price changed when event is started on <Race> Event Details Page
    DESCRIPTION: Test case verifies price update on Race EDP when flag isStarted' **= 'true'  is received
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYY?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet SiteServer*
    PRECONDITIONS: *   *YYYYYYY- event id*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes on market level to define price types for event:
    PRECONDITIONS: **'priceTypeCodes' **= 'LP'
    PRECONDITIONS: **'priceTypeCodes' **= 'SP'
    PRECONDITIONS: **'priceTypeCodes'** = 'LP, SP'
    PRECONDITIONS: **Updates are received in push notifications**
    PRECONDITIONS: In order to set event **'isStarted'**= 'true' -> in TI on event level set 'is Off' attribute to 'Yes'.
    """
    keep_browser_open = True

    def test_001_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: <Race> Landing page is opened
        """
        pass

    def test_002_open_race_event_details_page_where_event_has_lp_price_type_and_it_is_not_going_to_started_now(self):
        """
        DESCRIPTION: Open <Race> event details page where event has LP price type and it is not going to started now
        EXPECTED: * Event details page is opened
        EXPECTED: * Available market tabs are present
        """
        pass

    def test_003_in_ti_trigger_the_following_situation_for_this_event_when_the_markets_are_collapsedisstarted__trueeventstatuscodesnavigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Trigger the following situation for this event when the market(s) are collapsed:
        DESCRIPTION: **'isStarted' **= 'true'
        DESCRIPTION: **'eventStatusCode'='S'
        DESCRIPTION: Navigate to application and observe changes
        EXPECTED: * Corresponding 'Price/Odds' are displayed as greyed out but still display the prices when expanding the market(s).
        EXPECTED: * All 'Price/Odds' buttons become disabled for all markets associated with this event
        """
        pass

    def test_004_collapsed_the_markets(self):
        """
        DESCRIPTION: Collapsed the market(s)
        EXPECTED: 
        """
        pass

    def test_005_in_ti_change_price_for_one_of_the_selections_within_the_market_tab__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Change price for one of the selections within the market tab > Navigate to application and observe changes
        EXPECTED: * Corresponding 'Price/Odds' button is displayed the new price when expanding the market(s).
        EXPECTED: * Price/Odds' button doesn't change the color
        EXPECTED: * Previous Odds, under Price/Odds button, is updated/added respectively
        """
        pass

    def test_006_in_ti_trigger_the_following_situation_for_this_event_when_the_markets_are_collapsedisstarted__trueeventstatuscodeanavigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Trigger the following situation for this event when the market(s) are collapsed:
        DESCRIPTION: **'isStarted' **= 'true'
        DESCRIPTION: **'eventStatusCode'='A'
        DESCRIPTION: Navigate to application and observe changes
        EXPECTED: All 'Price/Odds' buttons are no more disabled, they become active for all market types when expanding the market(s).
        """
        pass

    def test_007_in_ti_change_price_for_one_of_the_selections__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Change price for one of the selections > Navigate to application and observe changes
        EXPECTED: Corresponding 'Price/Odds' button is immediately displayed new price and for a few seconds changed their color to:
        EXPECTED: * blue color if price has decreased;
        EXPECTED: * pink color if price has increased;
        EXPECTED: Previous Odds, under Price/Odds button, are updated/added respectively
        """
        pass

    def test_008_repeat_steps__3_9_for_the_event_where_price_type_is_splpsp_and_the_markets_are_expanded(self):
        """
        DESCRIPTION: Repeat steps # 3-9 for the event where price type is 'SP'/'LP,SP' and the market(s) are expanded
        EXPECTED: 
        """
        pass
