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
class Test_C28426_Verify_number_of_available_markets_MORE_link_on_In_Play_pages(Common):
    """
    TR_ID: C28426
    NAME: Verify '<number of available markets> MORE'  link on 'In-Play' pages
    DESCRIPTION: This test case verifies '<number of available markets> MORE'  link on 'In-Play' pages
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach Upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To configure In-Play module on Sports Landing page: https://ladbrokescoral.testrail.com/index.php?/cases/view/8146654
    PRECONDITIONS: * To configure In-Play module on Home page: https://ladbrokescoral.testrail.com/index.php?/cases/view/3019589
    PRECONDITIONS: * 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: * To get SiteServer info about event use the following url: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX"
    PRECONDITIONS: where:
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40951)
    """
    keep_browser_open = True

    def test_001_verify_number_of_available_markets_moremarkets_link_for_event_with_several_markets(self):
        """
        DESCRIPTION: Verify '<number of available markets> MORE/Markets' link for event with several markets
        EXPECTED: '<number of available markets> MORE' is shown below odds buttons for Coral and above them for Ladbrokes
        EXPECTED: **For Coral Desktop:**
        EXPECTED: '+<number of available markets> Markets' is shown next to odds buttons
        """
        pass

    def test_002_verify_number_of_extra_markets(self):
        """
        DESCRIPTION: Verify number of extra markets
        EXPECTED: *   For 'Upcoming' events number of markets correspond to:
        EXPECTED: 'Number of all markets - 1'
        EXPECTED: *   For 'Live Now' events number of markets correspond to:
        EXPECTED: 'Number of markets with 'isMarketBetInRun="true"' attribute - 1'
        """
        pass

    def test_003_clicktap_number_of_available_markets_moremarkets_link(self):
        """
        DESCRIPTION: Click/Tap '<number of available markets> MORE/Markets' link
        EXPECTED: Redirection to Event Details page occurs
        """
        pass

    def test_004_verify_number_of_available_markets_moremarkets_link_for_event_with_only_one_market(self):
        """
        DESCRIPTION: Verify '<number of available markets> MORE/Markets' link for event with ONLY one market
        EXPECTED: '<number of available markets> MORE/Markets' link is NOT shown on the Event section
        """
        pass

    def test_005_verify_number_of_available_markets_moremarkets_link_for_outright_event(self):
        """
        DESCRIPTION: Verify '<number of available markets> MORE/Markets' link for Outright event
        EXPECTED: '<number of available markets> MORE/Markets' link is NOT shown for Outrights events
        """
        pass

    def test_006_navigate_to_upcoming_events_and_repeat_steps_1_5(self):
        """
        DESCRIPTION: Navigate to upcoming events and repeat steps 1-5
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_1_5_on_sports_landing_page__matches_tab__in_play_module_for_mobiletablet_homepage__featured_tab__in_play_module_for_mobiletablet_sports_landing_page__in_play_widget_for_desktop_homepage__in_play__live_stream_section__in_play_and_live_stream_switchers_for_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-5 on:
        DESCRIPTION: * Sports Landing page > 'Matches' tab > 'In-play' module **For Mobile/Tablet**
        DESCRIPTION: * Homepage > 'Featured' tab > 'In-play' module **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing page > 'In-play' widget **For Desktop**
        DESCRIPTION: * Homepage > 'In-Play & Live Stream ' section > 'In-Play' and 'Live Stream' switchers **For Desktop**
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_1_6_on_homepage__in_play_tab_for_mobiletablet_sports_landing_page__in_play_tab_in_play_page__watch_live_tab(self):
        """
        DESCRIPTION: Repeat steps 1-6 on:
        DESCRIPTION: * Homepage > 'In-Play' tab **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        DESCRIPTION: * 'In-play' page > 'Watch live' tab
        EXPECTED: 
        """
        pass
