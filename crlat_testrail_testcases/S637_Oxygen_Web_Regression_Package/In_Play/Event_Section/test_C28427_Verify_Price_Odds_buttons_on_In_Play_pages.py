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
class Test_C28427_Verify_Price_Odds_buttons_on_In_Play_pages(Common):
    """
    TR_ID: C28427
    NAME: Verify 'Price/Odds' buttons on 'In-Play' pages
    DESCRIPTION: This test case verifies 'Price/Odds' buttons on 'In-Play' pages
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach Upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To configure In-Play module on Sports Landing page: https://ladbrokescoral.testrail.com/index.php?/cases/view/8146654
    PRECONDITIONS: * To configure In-Play module on Home page: https://ladbrokescoral.testrail.com/index.php?/cases/view/3019589
    PRECONDITIONS: * 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: * For DESKTOP: 'Price/Odds' button size depends on screen resolution (see https://ladbrokescoral.testrail.com/index.php?/cases/view/1474609 test case).
    PRECONDITIONS: * To get SiteServer info about event use the following url: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX"
    PRECONDITIONS: where:
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40949)
    """
    keep_browser_open = True

    def test_001_verify_data_of_priceodds_buttons_for_verified_event(self):
        """
        DESCRIPTION: Verify data of 'Price/Odds' buttons for verified event
        EXPECTED: *   'Price/Odds' corresponds to the 'priceNum/priceDen' if eventStatusCode="A" in fraction format
        EXPECTED: *   'Price/Odds' corresponds to the 'priceDec' if eventStatusCode="A" in decimal format
        EXPECTED: *   Disabled 'Priсe/Odds' button is displayed with 'priceNum/priceDen' (for fractional format) or 'priceDec' (for Decimal format) if eventStatusCode="S"
        """
        pass

    def test_002_verify_priceodds_buttons_for_2_way_market(self):
        """
        DESCRIPTION: Verify 'Price/Odds' buttons for 2-Way Market
        EXPECTED: For 2-way primary market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away
        """
        pass

    def test_003_verify_priceodds_buttons_for_3_way_market(self):
        """
        DESCRIPTION: Verify 'Price/Odds' buttons for 3-Way Market
        EXPECTED: For 3-way primary market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home
        EXPECTED: *   outcomeMeaningMinorCode="D" is a Draw
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away
        """
        pass

    def test_004_verify_priceodds_buttons_for_outright_event(self):
        """
        DESCRIPTION: Verify 'Price/Odds' buttons for Outright event
        EXPECTED: Price/Odds buttons are NOT available for Outright events
        """
        pass

    def test_005_navigate_to_upcoming_events_and_repeat_steps_1_4(self):
        """
        DESCRIPTION: Navigate to upcoming events and repeat steps 1-4
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_1_4_on_sports_landing_page__matches_tab__in_play_module_for_mobiletablet_homepage__featured_tab__in_play_module_for_mobiletablet_sports_landing_page__in_play_widget_for_desktop_homepage__in_play__live_stream_section__in_play_and_live_stream_switchers_for_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-4 on:
        DESCRIPTION: * Sports Landing page > 'Matches' tab > 'In-play' module **For Mobile/Tablet**
        DESCRIPTION: * Homepage > 'Featured' tab > 'In-play' module **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing page > 'In-play' widget **For Desktop**
        DESCRIPTION: * Homepage > 'In-Play & Live Stream ' section > 'In-Play' and 'Live Stream' switchers **For Desktop**
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_1_5_on_homepage__in_play_tab_for_mobiletablet_sports_landing_page__in_play_tab_in_play_page__watch_live_tab(self):
        """
        DESCRIPTION: Repeat steps 1-5 on:
        DESCRIPTION: * Homepage > 'In-Play' tab **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        DESCRIPTION: * 'In-play' page > 'Watch live' tab
        EXPECTED: 
        """
        pass
