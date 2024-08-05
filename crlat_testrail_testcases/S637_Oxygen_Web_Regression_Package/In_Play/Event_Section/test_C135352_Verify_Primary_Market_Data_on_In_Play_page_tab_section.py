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
class Test_C135352_Verify_Primary_Market_Data_on_In_Play_page_tab_section(Common):
    """
    TR_ID: C135352
    NAME: Verify Primary Market Data on 'In-Play' page/tab/section
    DESCRIPTION: This test case verifies Primary Market Data on 'In-Play Sports' page/tab/section
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach Upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To configure In-Play module on Sports Landing page: https://ladbrokescoral.testrail.com/index.php?/cases/view/8146654
    PRECONDITIONS: * To configure In-Play module on Home page: https://ladbrokescoral.testrail.com/index.php?/cases/view/3019589
    PRECONDITIONS: * 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: * For 'Outrights' events NO market is shown on the page
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX"
    PRECONDITIONS: where:
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40740)
    """
    keep_browser_open = True

    def test_001_verify_live_vent_with_available_selections(self):
        """
        DESCRIPTION: Verify live vent with available selections
        EXPECTED: Only selections that belong to the Market with the following attributes are shown on the In-Play page:
        EXPECTED: *   Market's attribute 'siteCannels' contains 'M'
        EXPECTED: *   Attribute 'isMarketBetInRun="true"' is present
        EXPECTED: *   All selections in such market have 'outcomeMeaningMajorCode="MR"/"HH"'
        EXPECTED: *   All selections in such market have attribute 'siteCannels' contains 'M'
        EXPECTED: If event has several markets that contain the above attributes - selections from the market **with the lowest 'displayOrder'** are shown on the page
        """
        pass

    def test_002_navigate_to_upcoming_events_and_repeat_step_1(self):
        """
        DESCRIPTION: Navigate to upcoming events and repeat step 1
        EXPECTED: Only selections that belong to the Market with the following attributes are shown on the In-Play page:
        EXPECTED: *   Market's attribute 'siteCannels' contains 'M'
        EXPECTED: *   Attribute 'isMarketBetInRun="true"' is present
        EXPECTED: *   All selections in such market have 'outcomeMeaningMajorCode="MR"/"HH"'
        EXPECTED: *   All selections in such market have attribute 'siteCannels' contains 'M'
        EXPECTED: If event has several markets that contain the above attributes - selections from the market **with the lowest 'displayOrder'** are shown on the page
        """
        pass

    def test_003_repeat_step_1_on_sports_landing_page_gt_matches_tab_gt_in_play_module_for_mobiletablet_homepage_gt_featured_tab_gt_in_play__module_for_mobiletablet_sports_landing_page_gt_in_play_widget_for_desktop_homepage_gt_in_play__live_stream_section_gt_in_play_switcher_for_desktop(self):
        """
        DESCRIPTION: Repeat step 1 on:
        DESCRIPTION: * Sports Landing page &gt; 'Matches' tab &gt; 'In-play' module **For Mobile/Tablet**
        DESCRIPTION: * Homepage &gt; 'Featured' tab &gt; 'In-play'  module **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing page &gt; 'In-play' widget **For Desktop**
        DESCRIPTION: * Homepage &gt; 'In-Play & Live Stream ' section &gt; 'In-Play' switcher **For Desktop**
        EXPECTED: 
        """
        pass

    def test_004_repeat_steps_1_2_on_home_page_gt_in_play_tab_for_mobiletablet_sports_landing_page_gt_in_play_tab_in_play_page_gt_watch_live_tab(self):
        """
        DESCRIPTION: Repeat steps 1-2 on:
        DESCRIPTION: * Home page &gt; 'In-Play' tab **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page &gt; 'In-Play' tab
        DESCRIPTION: * 'In-play' page &gt; 'Watch live' tab
        EXPECTED: 
        """
        pass
