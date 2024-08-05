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
class Test_C2745985_Verify_CMS_configuration_for_Watch_Live_tab(Common):
    """
    TR_ID: C2745985
    NAME: Verify CMS configuration for 'Watch Live' tab
    DESCRIPTION: This test case verifies CMS configuration for 'Watch Live' tab
    PRECONDITIONS: 1. 'InPlayWatchLive' should be disabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 2. Load Oxygen app and navigate to 'In-Play' page
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_watch_live_tabicon_at_in_play_sports_ribbon(self):
        """
        DESCRIPTION: Verify displaying of 'Watch Live' tab/icon at 'In-Play' sports ribbon
        EXPECTED: * 'Watch Live' tab/icon is NOT displayed at'In-Play' sports ribbon
        EXPECTED: * User is landed on the FIRST sport in the ribbon by default e.g. Football
        """
        pass

    def test_002_go_to_cms_gt_system_configuration_gt_enable_inplaywatchlive_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS &gt; System Configuration &gt; enable 'InPlayWatchLive' and save changes
        EXPECTED: 
        """
        pass

    def test_003___go_to_oxygen_app__refresh_in_play_page__verify_displaying_of_watch_live_tabicon(self):
        """
        DESCRIPTION: - Go to Oxygen app
        DESCRIPTION: - Refresh 'In-Play page'
        DESCRIPTION: - Verify displaying of 'Watch Live' tab/icon
        EXPECTED: * 'Watch Live' tab/icon is displayed at 'In-Play' sports ribbon as the first icon
        EXPECTED: * Order of other sport icons remains unchanged
        EXPECTED: * User is landed on the FIRST sport in the ribbon by default e.g. Football
        """
        pass

    def test_004_go_to_cms_gt_system_configuration_gt_disable_inplaywatchlive_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS &gt; System Configuration &gt; disable 'InPlayWatchLive' and save changes
        EXPECTED: 
        """
        pass

    def test_005___go_to_oxygen_app__refresh_in_play_page__verify_displaying_of_watch_live_tabicon(self):
        """
        DESCRIPTION: - Go to Oxygen app
        DESCRIPTION: - Refresh 'In-Play page'
        DESCRIPTION: - Verify displaying of 'Watch Live' tab/icon
        EXPECTED: * 'Watch Live' tab/icon is NOT displayed at'In-Play' sports ribbon
        EXPECTED: * User is landed on the FIRST sport in the ribbon by default e.g. Football
        """
        pass
