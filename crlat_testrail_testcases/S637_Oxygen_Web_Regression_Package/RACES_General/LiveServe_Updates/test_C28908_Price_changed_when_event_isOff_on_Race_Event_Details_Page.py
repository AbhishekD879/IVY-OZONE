import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28908_Price_changed_when_event_isOff_on_Race_Event_Details_Page(Common):
    """
    TR_ID: C28908
    NAME: Price changed when event isOff on <Race> Event Details Page
    DESCRIPTION: Test case verifies price change on Race EDP when event is off
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYY?translationLang=LL ,
    PRECONDITIONS: where:
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet SiteServer*
    PRECONDITIONS: *   *YYYYYYY- event id*
    PRECONDITIONS: *   *LL - language (e.g. en, ukr) *
    PRECONDITIONS: See attributes on market level to define price types for an event:
    PRECONDITIONS: **'priceTypeCodes' **= 'LP'
    PRECONDITIONS: **'priceTypeCodes' **= 'SP'
    PRECONDITIONS: **'priceTypeCodes'** = 'LP,SP'
    PRECONDITIONS: **Updates are received in push notifications**
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_on_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap on <Race> icon from the Sports Menu Ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_open_race_event_details_page_where_event_has_lp_price_type_pricetypecodes__lp_and_it_is_not_going_to_started_now(self):
        """
        DESCRIPTION: Open <Race> event details page where event has LP price type (**'priceTypeCodes'** = 'LP') and it is not going to started now
        EXPECTED: * Event details page is opened
        EXPECTED: * Available market tabs are present
        """
        pass

    def test_004_in_ti_trigger_the_following_situation_for_this_event_where_the_markets_are_expandedstatus__sisoffyesnavigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Trigger the following situation for this event where the market(s) are expanded:
        DESCRIPTION: **'Status' **= 'S'
        DESCRIPTION: **'isOff'**='Yes'
        DESCRIPTION: Navigate to application and observe changes
        EXPECTED: * All 'Price/Odds' buttons for this event immediately start displaying as greyed out but still display the prices
        EXPECTED: * All 'Price/Odds' buttons become disabled for all markets associated with this event
        """
        pass

    def test_005_in_ti_change_price_for_one_of_the_selections__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Change price for one of the selections > Navigate to application and observe changes
        EXPECTED: * Corresponding 'Price/Odds' button is immediately displayed new price
        EXPECTED: * Price/Odds' button doesn't change the color
        EXPECTED: * Previous Odds, under Price/Odds button, is updated/added respectively
        """
        pass

    def test_006_repeat_steps__3_5_for_the_event_where_price_type_is_splpsp_and_the_markets_are_collapsed(self):
        """
        DESCRIPTION: Repeat steps # 3-5 for the event where price type is 'SP'/'LP,SP' and the market(s) are collapsed
        EXPECTED: 
        """
        pass
