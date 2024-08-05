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
class Test_C141221_Price_Odds_button_on_the_Race_page_if_price_wasnt_sent_from_SiteServer(Common):
    """
    TR_ID: C141221
    NAME: Price/Odds button on the <Race> page if price wasn't sent from SiteServer
    DESCRIPTION: This test case verifies displaying Price/Odds button on the <Race> page if price wasn't sent from SiteServer
    DESCRIPTION: Applies to mobile, tablet and desktop
    PRECONDITIONS: To get SiteServer info about an event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYY?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: X.XX - current supported version of OpenBet SiteServer
    PRECONDITIONS: YYYYYYY- event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes on market level to define price types for an event:
    PRECONDITIONS: 'priceTypeCodes' = 'LP'
    PRECONDITIONS: 'priceTypeCodes' = 'LP, SP'
    PRECONDITIONS: Event is started, if it has attribute 'Status'='S' and '**isOff'**='Yes' in OpenBet (TST2-environment)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: HomePage is opened
        """
        pass

    def test_002_tap_on_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap on <Race> icon from the Sports Menu Ribbon
        EXPECTED: <Race> Event Landing page is opened
        """
        pass

    def test_003_open_event_details_page_where_event_has_lp_price_type_pricetypecodes__lp_without_odds_and_it_is_not_going_to_start_now(self):
        """
        DESCRIPTION: Open Event Details Page where Event has LP price type (**'priceTypeCodes'** = LP) without Odds and it is not going to start now
        EXPECTED: * Event details page is opened
        EXPECTED: * Price/Odds button for selected outcome displayed as greyed out and is disabled
        EXPECTED: * 'SP' is displayed on Price/Odds button
        """
        pass

    def test_004_repeat_steps__3_for_event_where_price_type_is_lpsp(self):
        """
        DESCRIPTION: Repeat steps # 3 for event where price type is 'LP,SP'
        EXPECTED: 
        """
        pass
