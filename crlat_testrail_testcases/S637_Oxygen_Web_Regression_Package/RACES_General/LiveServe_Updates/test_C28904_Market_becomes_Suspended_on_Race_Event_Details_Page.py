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
class Test_C28904_Market_becomes_Suspended_on_Race_Event_Details_Page(Common):
    """
    TR_ID: C28904
    NAME: Market becomes Suspended on <Race> Event Details Page
    DESCRIPTION: Test case verifies market suspension in real time on Race EDP
    PRECONDITIONS: To get SiteServer info about event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYY?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet SiteServer*
    PRECONDITIONS: *   *YYYYYYY- event id*
    PRECONDITIONS: *   *LL - language (e.g. en, ukr) *
    PRECONDITIONS: See attributes on market level to define price types for event:
    PRECONDITIONS: **'priceTypeCodes' **= 'LP'
    PRECONDITIONS: **'priceTypeCodes' **= 'SP'
    PRECONDITIONS: **'priceTypeCodes'** = 'LP, SP'
    PRECONDITIONS: Make sure event is active (**eventStatusCode** = 'A')
    PRECONDITIONS: To observe LiveServe changes make sure:
    PRECONDITIONS: - 'Bet In Play List' flag is checked on 'Event' level in TI
    PRECONDITIONS: - 'Bet in Running' is checked on 'Market' level in TI
    PRECONDITIONS: **Updates are received in push notifications**
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_open_race_event_details_page_where_event_has_lp_price_type_pricetypecodes___lp_(self):
        """
        DESCRIPTION: Open <Race> event details page where event has LP price type (
        DESCRIPTION: **'priceTypeCodes' ** = 'LP' )
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_in_ti_suspend_one_of_the_markets__marketstatuscod_s___navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Suspend one of the markets ( **'marketStatusCod' **= 'S' ) > Navigate to application and observe changes
        EXPECTED: All Price/Odds buttons of this market are immediately displayed as greyed out
        """
        pass

    def test_005_in_ti_unsuspend_market__marketstatuscod_a____navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: UnSuspend market ( **'marketStatusCod' **= 'A' ) >  Navigate to application and observe changes
        EXPECTED: All Price/Odds buttons of this market are no more disabled, they immediately become active
        """
        pass

    def test_006_in_ti_suspend_all_markets_within_market_tabs_betting_wo_and_more_markets_in_a_collapsed_state__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Suspend all markets within market tabs ('Betting WO' and 'More Markets') in a collapsed state > Navigate to application and observe changes
        EXPECTED: All Price/Odds buttons markets are displayed as greyed out when expanding the market(s)
        """
        pass

    def test_007_in_ti_unsuspend_all_markets_within_market_tabs_betting_wo_and_more_markets_in_a_collapsed_state__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: UnSuspend all markets within market tabs ('Betting WO' and 'More Markets') in a collapsed state > Navigate to application and observe changes
        EXPECTED: All Price/Odds buttons markets are no more disabled, they displayed as active when expanding the market(s)
        """
        pass

    def test_008_in_ti_suspend_all_markets_within_market_tabs_betting_wo_and_more_markets_in_an_expanded_state__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Suspend all markets within market tabs ('Betting WO' and 'More Markets') in an expanded state > Navigate to application and observe changes
        EXPECTED: All Price/Odds buttons of markets are immediately displayed as greyed out
        """
        pass

    def test_009_in_ti_unsuspend_all_markets_within_market_tabs_betting_wo_and_more_markets_in_an_expanded_state__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: UnSuspend all markets within market tabs ('Betting WO' and 'More Markets') in an expanded state > Navigate to application and observe changes
        EXPECTED: All Price/Odds buttons markets are no more disabled, they immediately become active
        """
        pass

    def test_010_repeat_steps__3_9_for_event_where_price_type_is_splpsp(self):
        """
        DESCRIPTION: Repeat steps # 3-9 for event where price type is 'SP'/'LP,SP'
        EXPECTED: 
        """
        pass
