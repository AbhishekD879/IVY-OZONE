import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C9608484_Verify_Sports_Menu_Ribbon_behaviour_on_IN_PLAY_tab_of_Homepage_with_enabled_disabled_Virtual_Scroll(Common):
    """
    TR_ID: C9608484
    NAME: Verify Sports Menu Ribbon behaviour on IN-PLAY tab of Homepage with enabled/disabled Virtual Scroll
    DESCRIPTION: This test case verifies behaviour of Sports Menu Ribbon on Homepage>'In-play' tab when Virtual Scroll in enabled/disabled in CMS
    PRECONDITIONS: 1) Virtual Scroll should be enabled in CMS > System configuration > Structure > VirtualScrollConfig > enabled=true
    PRECONDITIONS: 2) In-play events should be present for several sports
    PRECONDITIONS: 3) Load Oxygen app
    PRECONDITIONS: 4) Open/Tap on 'In-Play' tab
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_scroll_down_until_reaching_content_of_1st_sport_accordion(self):
        """
        DESCRIPTION: Scroll down until reaching content of 1st sport accordion
        EXPECTED: * Sports Menu Ribbon gets hidden
        EXPECTED: * 1st sport accordion (e.g. Football) becomes sticky
        """
        pass

    def test_002_scroll_up_a_little_bit(self):
        """
        DESCRIPTION: Scroll up a little bit
        EXPECTED: * Sports Menu Ribbon remains hidden
        EXPECTED: * 1st sport accordion (e.g. Football) remains sticky
        """
        pass

    def test_003_scroll_up_until_reaching__live_now_header(self):
        """
        DESCRIPTION: Scroll up until reaching  'Live now' header
        EXPECTED: * Sports Menu Ribbon becomes visible when reaching 'Live now' header
        EXPECTED: * 1st sport accordion (e.g. Football) returns into initial position (below 'Live now' header)
        """
        pass

    def test_004__disable_virtual_scroll_in_cms__system_configuration__structure__virtualscrollconfig_save_changes(self):
        """
        DESCRIPTION: * Disable Virtual Scroll in CMS > System configuration > Structure > VirtualScrollConfig
        DESCRIPTION: * Save changes
        EXPECTED: 
        """
        pass

    def test_005_manually_refresh_the_homepage_with_selected_in_play_tab(self):
        """
        DESCRIPTION: Manually refresh the Homepage with selected 'In-Play' tab
        EXPECTED: 
        """
        pass

    def test_006_scroll_down_until_reaching_content_of_1st_sport_accordion(self):
        """
        DESCRIPTION: Scroll down until reaching content of 1st sport accordion
        EXPECTED: * Sports Menu Ribbon gets hidden
        EXPECTED: * 1st sport accordion (e.g. Football) is NOT sticky
        """
        pass

    def test_007_scroll_up_a_little_bit(self):
        """
        DESCRIPTION: Scroll up a little bit
        EXPECTED: * Sports Menu Ribbon becomes visible
        EXPECTED: * 1st sport accordion (e.g. Football) is NOT sticky
        """
        pass
