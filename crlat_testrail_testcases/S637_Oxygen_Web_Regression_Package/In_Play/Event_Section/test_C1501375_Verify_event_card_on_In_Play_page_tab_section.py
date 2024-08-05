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
class Test_C1501375_Verify_event_card_on_In_Play_page_tab_section(Common):
    """
    TR_ID: C1501375
    NAME: Verify event card on 'In-Play' page/tab/section
    DESCRIPTION: This test case verifies event card on 'In-Play' page/tab/section
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach Upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To configure In-Play module on Sports Landing page: https://ladbrokescoral.testrail.com/index.php?/cases/view/8146654
    PRECONDITIONS: * To configure In-Play module on Home page: https://ladbrokescoral.testrail.com/index.php?/cases/view/3019589
    PRECONDITIONS: * 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: * To get SiteServer info about event use the following url: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL,
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    """
    keep_browser_open = True

    def test_001_verify_event_name(self):
        """
        DESCRIPTION: Verify Event Name
        EXPECTED: *   Event name corresponds to 'name' attribute
        EXPECTED: *   Event name is displayed in format:
        EXPECTED: &lt;Team1/Player1&gt;
        EXPECTED: &lt;Team2/Player2&gt;
        EXPECTED: *   Name of outright event is displayed in format: '&lt;Event name&gt;'
        """
        pass

    def test_002_verify_match_timesetslive_label(self):
        """
        DESCRIPTION: Verify 'Match Time'/'Sets'/'LIVE' label
        EXPECTED: *   Event **'Match Time'/'Sets'/'LIVE' label** is shown if available instead of event Start Time
        EXPECTED: *   **'Match Time'/'Sets'/'LIVE label** is displayed below Event name (for Coral) and above Event name (for Ladbrokes)
        """
        pass

    def test_003_verify_watch_live_icon(self):
        """
        DESCRIPTION: Verify 'WATCH LIVE' icon
        EXPECTED: * 'WATCH' icon is displayed for **Ladbrokes**, 'WATCH LIVE' inscription and icon for **Coral**
        EXPECTED: * 'WATCH LIVE' icon/inscription is shown if ‘drilldownTagNames’ attribute is available (one or more of following flags):
        EXPECTED: - EVFLAG_AVA
        EXPECTED: - EVFLAG_IVM
        EXPECTED: - EVFLAG_PVM
        EXPECTED: - EVFLAG_RVA
        EXPECTED: - EVFLAG_RPM
        EXPECTED: - EVFLAG_GVM
        EXPECTED: * 'WATCH LIVE' inscription/icon is displayed next to 'Match Time'/'Sets'/'LIVE' label/'Event Start Time'
        """
        pass

    def test_004_for_coralverify_favorites_icon(self):
        """
        DESCRIPTION: **For Coral:**
        DESCRIPTION: Verify 'Favorites' icon
        EXPECTED: 'Favorites' icon is displayed before 'Match Time'/'Sets'/'LIVE' label/'Event Start Time' on Football events only
        """
        pass

    def test_005_clicktapanywhere_on_event_section(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event section
        EXPECTED: Event Details Page is opened
        """
        pass

    def test_006_navigate_to_upcoming_events(self):
        """
        DESCRIPTION: Navigate to upcoming events
        EXPECTED: The list of upcoming events is displayed on the page
        """
        pass

    def test_007_verify_event_name(self):
        """
        DESCRIPTION: Verify Event Name
        EXPECTED: *   Event name corresponds to 'name' attribute
        EXPECTED: *   Event name is displayed in format **for Coral Mobile/Tablet** and **Ladbrokes all platforms**:
        EXPECTED: &lt;Team1/Player1&gt;
        EXPECTED: &lt;Team2/Player2&gt;
        EXPECTED: *   Event name is displayed in format **for Coral Desktop**:
        EXPECTED: &lt;Team1/Player1&gt; vs &lt;Team2/Player2&gt;
        EXPECTED: *   Name of outright event is displayed in format: '&lt;Event name&gt;'
        """
        pass

    def test_008_verify_event_start_time(self):
        """
        DESCRIPTION: Verify 'Event Start Time'
        EXPECTED: 'Event start time' corresponds to 'startTime' attribute and is displayed in the format '24 hours, Day (e.g. 21:45, Today OR 02:00, 23 Oct)'
        """
        pass

    def test_009_clicktapanywhere_on_event_section(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event section
        EXPECTED: Event Details Page is opened
        """
        pass

    def test_010_repeat_steps_1_5_on_sports_landing_page_gt_matches_tab_gt_in_play_module_for_mobiletablet_homepage_gt_featured_tab_gt_in_play__module_for_mobiletablet_homepage_gt_in_play__live_stream_section_gt_in_play_switcher_for_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-5 on:
        DESCRIPTION: * Sports Landing page &gt; 'Matches' tab &gt; 'In-play' module **For Mobile/Tablet**
        DESCRIPTION: * Homepage &gt; 'Featured' tab &gt; 'In-play'  module **For Mobile/Tablet**
        DESCRIPTION: * Homepage &gt; 'In-Play & Live Stream ' section &gt; 'In-Play' switcher **For Desktop**
        EXPECTED: 
        """
        pass
