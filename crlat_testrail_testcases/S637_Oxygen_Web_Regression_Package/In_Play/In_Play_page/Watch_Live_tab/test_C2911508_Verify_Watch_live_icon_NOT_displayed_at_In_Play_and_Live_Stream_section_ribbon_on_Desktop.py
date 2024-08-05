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
class Test_C2911508_Verify_Watch_live_icon_NOT_displayed_at_In_Play_and_Live_Stream_section_ribbon_on_Desktop(Common):
    """
    TR_ID: C2911508
    NAME: Verify 'Watch live' icon NOT displayed at 'In-Play and Live Stream' section ribbon on Desktop
    DESCRIPTION: This test case verifies that "Watch live" icon is NOT displayed at "In-Play and Live Stream" section ribbon on Desktop
    DESCRIPTION: Note: cannot automate, can't configure streams
    PRECONDITIONS: 1. 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 2. Live events with and without mapped streams should be configured in Open Bet TI system
    PRECONDITIONS: 3. For event configuration use Open Bet TI system, see details following the link below: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: Load Oxygen app on Desktop > Homepage
    """
    keep_browser_open = True

    def test_001_verify_watch_live_icon_displaying_at_in_play_and_live_stream_section_ribbon_when_in_play_switcher_is_selected(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon displaying at 'In-Play and Live Stream' section ribbon when 'In-play' switcher is selected
        EXPECTED: 'Watch Live' icon is NOT displayed at 'In-Play and Live Stream' section ribbon when 'In-play' switcher is selected
        """
        pass

    def test_002_click_on_live_stream_switcher_and_verify_watch_live_icon_displaying(self):
        """
        DESCRIPTION: Click on 'Live Stream' switcher and verify "Watch Live" icon displaying
        EXPECTED: 'Watch Live' icon is NOT displayed at 'In-Play and Live Stream' section ribbon when 'Live Stream' switcher is selected
        """
        pass
