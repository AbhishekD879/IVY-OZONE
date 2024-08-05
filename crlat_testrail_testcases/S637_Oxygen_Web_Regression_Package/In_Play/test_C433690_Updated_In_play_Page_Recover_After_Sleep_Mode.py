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
class Test_C433690_Updated_In_play_Page_Recover_After_Sleep_Mode(Common):
    """
    TR_ID: C433690
    NAME: Updated In-play Page Recover After Sleep Mode
    DESCRIPTION: Test Case verifies in-play page recovers after sleep mode  and all event are present and updated.
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To configure In-Play module on Sports Landing page: https://ladbrokescoral.testrail.com/index.php?/cases/view/8146654
    PRECONDITIONS: * To configure In-Play module on Home page: https://ladbrokescoral.testrail.com/index.php?/cases/view/3019589
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * In-play page updates:
    PRECONDITIONS: - Live Price
    PRECONDITIONS: - Undisplay
    PRECONDITIONS: - Suspend
    PRECONDITIONS: - Event Match Time/ Live / HT
    PRECONDITIONS: - Event Scores
    """
    keep_browser_open = True

    def test_001_lock_device_or_autolock(self):
        """
        DESCRIPTION: Lock Device or Autolock
        EXPECTED: 
        """
        pass

    def test_002_wait__30_sec__1_min__3_mins__30_mins__1_h__3_h__24_h(self):
        """
        DESCRIPTION: Wait:
        DESCRIPTION: - 30 sec
        DESCRIPTION: - 1 min
        DESCRIPTION: - 3 mins
        DESCRIPTION: - 30 mins
        DESCRIPTION: - 1 h
        DESCRIPTION: - 3 h
        DESCRIPTION: - 24 h
        EXPECTED: 
        """
        pass

    def test_003_make_in_play_events_updates_see_preconditions(self):
        """
        DESCRIPTION: Make In-play events updates (see preconditions)
        EXPECTED: 
        """
        pass

    def test_004_unlock_device(self):
        """
        DESCRIPTION: Unlock device
        EXPECTED: - Page is loaded and contains In-play events
        EXPECTED: - In-play events are updated
        EXPECTED: - NO endless spinner
        """
        pass

    def test_005_repeat_steps_1_4_but_with__before_lock_moving_appbrowser_to_background__after_unlock_moving_appbrowser_to_the_foreground(self):
        """
        DESCRIPTION: Repeat steps 1-4 but with:
        DESCRIPTION: - before lock: moving app/browser to background
        DESCRIPTION: - after unlock: moving app/browser to the foreground
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_1_5_on_home_page__in_play_tab_for_mobiletablet_sports_landing_page__in_play_tab_sports_landing_page__matches_tab__in_play_module_for_mobiletablet_homepage__featured_tab__in_play__module_for_mobiletablet_homepage__in_play__live_stream_section_for_desktop_sports_landing_page__in_play_widget_for_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-5 on:
        DESCRIPTION: * Home page > 'In-Play' tab **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        DESCRIPTION: * Sports Landing page > 'Matches' tab > 'In-play' module **For Mobile/Tablet**
        DESCRIPTION: * Homepage > 'Featured' tab > 'In-play'  module **For Mobile/Tablet**
        DESCRIPTION: * Homepage > 'In-Play & Live Stream ' section **For Desktop**
        DESCRIPTION: * Sports Landing page > 'In-play' widget **For Desktop**
        EXPECTED: 
        """
        pass
