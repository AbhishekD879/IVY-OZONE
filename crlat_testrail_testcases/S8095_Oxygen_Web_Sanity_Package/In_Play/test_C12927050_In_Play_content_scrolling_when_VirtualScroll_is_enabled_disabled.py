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
class Test_C12927050_In_Play_content_scrolling_when_VirtualScroll_is_enabled_disabled(Common):
    """
    TR_ID: C12927050
    NAME: In-Play content scrolling when VirtualScroll is enabled/disabled
    DESCRIPTION: This test case verifies scrolling of In-Play content on 'In-play' tab (Home page) and 'Watch live' tab (In-play page) when VirtualScroll is enabled in CMS
    DESCRIPTION: Note: Cannot automate it - the test case contains a lot of UI verification that cannot be done/or hardly done by script
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Open/Tap on 'In-Play' tab on the Homepage
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 1) 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 2) Virtual Scroll should be enabled in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_scroll_down_until_reaching_content_of_1st_sport_accordion(self):
        """
        DESCRIPTION: Scroll down until reaching content of 1st sport accordion
        EXPECTED: * 1st sport accordion becomes sticky below 'Coral/Ladbrokes' header
        EXPECTED: * The rest of the elements (i.e. banners, sports ribbon, etc) are hidden
        EXPECTED: ![](index.php?/attachments/get/30559)
        """
        pass

    def test_002__scroll_down_until_reaching_the_next_sport_accordion_collapsed_one(self):
        """
        DESCRIPTION: * Scroll down until reaching the next sport accordion (collapsed one)
        EXPECTED: * 1st sport accordion is NOT sticky any more
        EXPECTED: ![](index.php?/attachments/get/30561)
        """
        pass

    def test_003__expand_2nd_sport_accordion_scroll_down(self):
        """
        DESCRIPTION: * Expand 2nd sport accordion
        DESCRIPTION: * Scroll down
        EXPECTED: * 2nd sport accordion becomes sticky
        """
        pass

    def test_004_collapse_2nd_sport_accordion_while_its_sticky(self):
        """
        DESCRIPTION: Collapse 2nd sport accordion while it's sticky
        EXPECTED: * 2nd sport accordion becomes collapsed
        EXPECTED: * Remains below 'Coral/Ladbrokes' header
        EXPECTED: ![](index.php?/attachments/get/30562)
        """
        pass

    def test_005_scroll_up_a_bit(self):
        """
        DESCRIPTION: Scroll up a bit
        EXPECTED: 1st sport accordion is shown sticky
        """
        pass

    def test_006_scroll_up_till_the_top_of_the_page(self):
        """
        DESCRIPTION: Scroll up till the top of the page
        EXPECTED: * 1st sport accordion returns into its initial position (below 'Live now' header)
        """
        pass

    def test_007__scroll_down_until_reaching_upcoming_events_section_expand_1st_sport_accordion_repeat_steps_1_6(self):
        """
        DESCRIPTION: * Scroll down until reaching 'Upcoming events' section
        DESCRIPTION: * Expand 1st sport accordion
        DESCRIPTION: * Repeat steps 1-6
        EXPECTED: 
        """
        pass

    def test_008__navigate_to_in_play_page__watch_live_tab_repeat_steps_1_6_for_both_live_now_and_upcoming_sections(self):
        """
        DESCRIPTION: * Navigate to 'In-play' page > 'Watch live' tab
        DESCRIPTION: * Repeat steps 1-6 for both 'Live now' and 'Upcoming' sections
        EXPECTED: * 1st sport accordion becomes sticky below 'Coral/Ladbrokes' header and 'In-play' header with 'Back' button
        EXPECTED: * The rest of the elements (i.e. banners, sports ribbon, etc) are hidden
        """
        pass

    def test_009__disable_virtualscroll_in_cms___system_configuration__structure__virtualscrollconfig_on_fe_refresh_the_home_page__in_play_tab(self):
        """
        DESCRIPTION: * Disable VirtualScroll in CMS > > System configuration > Structure > VirtualScrollConfig
        DESCRIPTION: * On FE refresh the home page > 'In-play' tab
        EXPECTED: 
        """
        pass

    def test_010__scroll_down_until_reaching_content_of_1st_sport_accordion_scroll_down_until_reaching_upcoming_events_section(self):
        """
        DESCRIPTION: * Scroll down until reaching content of 1st sport accordion
        DESCRIPTION: * Scroll down until reaching 'Upcoming events' section
        EXPECTED: * No elements (i.e. sport accordion/league header) are sticky
        EXPECTED: * 'Coral/Ladbrokes' header together with 'Login/Join now' buttons remain visible
        """
        pass
