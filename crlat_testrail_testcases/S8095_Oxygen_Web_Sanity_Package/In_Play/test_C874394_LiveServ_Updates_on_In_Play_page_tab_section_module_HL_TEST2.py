import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C874394_LiveServ_Updates_on_In_Play_page_tab_section_module_HL_TEST2(Common):
    """
    TR_ID: C874394
    NAME: LiveServ Updates on 'In-Play' page/tab/section/module [HL/TEST2]
    DESCRIPTION: This test case verifies LiveServ updates on 'In-Play' page/tab/section/module
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the 'In-Play' page > <Sports> tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: 1) Live event should contain the following attributes:
    PRECONDITIONS: * "rawIsOffCode" : "Y"
    PRECONDITIONS: * "isStarted" : "true"
    PRECONDITIONS: * "drilldownTagNames" : "EVFLAG_BL"
    PRECONDITIONS: * "isMarketBetInRun: : "true"
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To get SiteServer info about the event please use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: 2) To verify price updates check new received values in "lp_den" and "lp_num" attributes using Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: PRICE
    PRECONDITIONS: 3) To verify suspension/unsuspension check new received values in "status" attribute using Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: EVENT/EVMKT/SELCT depends on level of triggering the status changes (event/market/outcome)
    """
    keep_browser_open = True

    def test_001_verify_price_change_for_match_betting_market_outcome_for_one_of_the_live_events_from_the_current_page(self):
        """
        DESCRIPTION: Verify price change for 'Match Betting' market outcome for one of the Live events from the current page
        EXPECTED: Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its color to:
        EXPECTED: - blue color if price has decreased
        EXPECTED: - pink color if price has increased
        EXPECTED: The whole button changes color on Coral, only digits change color on Ladbrokes
        """
        pass

    def test_002_verify_suspension_on_eventmarketoutcome_level_for_one_of_the_events_from_the_current_page(self):
        """
        DESCRIPTION: Verify suspension on event/market/outcome level for one of the events from the current page
        EXPECTED: Corresponding 'Price/Odds' buttons are displayed as greyed out and become disabled
        """
        pass

    def test_003_verify_unsuspension_on_eventmarketoutcome_level_for_one_of_the_events_from_the_current_page(self):
        """
        DESCRIPTION: Verify unsuspension on event/market/outcome level for one of the events from the current page
        EXPECTED: Corresponding 'Price/Odds' buttons are displayed as active and clickable
        """
        pass

    def test_004_repeat_steps_1_3_for__homepage___featured_tabsection__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop__sports_landing_page___matches_tab___in_play_widget_desktop__sports_landing_page___matches_tab___live_stream_widget_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - Homepage -> 'Featured' tab/section
        DESCRIPTION: - Homepage -> 'In-Play' tab
        DESCRIPTION: - Homepage -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play' page -> 'Watch Live' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play & Live Stream ' section on Homepage **Desktop**
        DESCRIPTION: - Sports Landing page -> 'Matches' tab -> 'In-Play' widget **Desktop**
        DESCRIPTION: - Sports Landing page -> 'Matches' tab -> 'Live Stream' widget **Desktop**
        EXPECTED: 
        """
        pass
