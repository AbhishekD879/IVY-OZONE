import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C380912_Updating_of_CMS_configs_of_Next_Races(Common):
    """
    TR_ID: C380912
    NAME: Updating of CMS configs of Next Races
    DESCRIPTION: This test case verifies updating of CMS configs of Next Races module/widget/tab
    PRECONDITIONS: * Next Races module/widget is created and races data is displayed
    PRECONDITIONS: * Test case should be run on mobile, tablet and desktop
    """
    keep_browser_open = True

    def test_001_load_coral_app(self):
        """
        DESCRIPTION: Load Coral app
        EXPECTED: 
        """
        pass

    def test_002_make_changes_in_cms_configs_for_nextraces_httpsinvictuscoralcoukkeystonestructure(self):
        """
        DESCRIPTION: Make changes in CMS configs for NEXTRACES (https://invictus.coral.co.uk/keystone/structure)
        EXPECTED: 
        """
        pass

    def test_003_navigate_to_next_races_tab_on_home_page(self):
        """
        DESCRIPTION: Navigate to Next Races tab on Home page
        EXPECTED: * 'system-configuration' request is sent and returns up-to-date data
        EXPECTED: * Config changes from step #2 are applied for:
        EXPECTED: * Next Races tab content
        EXPECTED: * Next Races widget (on tablet and desktop)
        """
        pass

    def test_004_move_device_to_sleep_mode(self):
        """
        DESCRIPTION: Move device to sleep mode
        EXPECTED: 
        """
        pass

    def test_005_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step #2
        EXPECTED: 
        """
        pass

    def test_006_wake_device_up(self):
        """
        DESCRIPTION: Wake device up
        EXPECTED: * 'reload components' is triggered in Console
        EXPECTED: * 'system-configuration' request is sent and returns up-to-date data in Network
        EXPECTED: * Config changes from step #2 are applied for:
        EXPECTED: * Next Races tab content
        EXPECTED: * Next Races widget (on tablet and desktop)
        """
        pass

    def test_007_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step #2
        EXPECTED: 
        """
        pass

    def test_008_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to Horse Racing landing page
        EXPECTED: * 'system-configuration' request is sent and returns up-to-date data
        EXPECTED: * Config changes from step #2 are applied for:
        EXPECTED: * Next Races module content on landing page
        EXPECTED: * Next Races widget (on tablet and desktop)
        """
        pass

    def test_009_lose_internet_connection(self):
        """
        DESCRIPTION: Lose internet connection
        EXPECTED: 
        """
        pass

    def test_010_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step #2
        EXPECTED: 
        """
        pass

    def test_011_restore_internet_connection(self):
        """
        DESCRIPTION: Restore internet connection
        EXPECTED: * 'reload components' is triggered in Console
        EXPECTED: * 'system-configuration' request is sent and returns up-to-date data in Network
        EXPECTED: * Config changes from step #2 are applied for:
        EXPECTED: * Next Races module content on landing page
        EXPECTED: * Next Races widget (on tablet and desktop)
        """
        pass

    def test_012_following_steps_are_for_tablet_and_desktop_onlynavigate_to_any_other_page_except_horse_racing_landing_page_or_next_races_tab_on_home_page(self):
        """
        DESCRIPTION: Following steps are for tablet and desktop only
        DESCRIPTION: Navigate to any other page except Horse Racing landing page or Next Races tab on Home page
        EXPECTED: 
        """
        pass

    def test_013_move_device_to_sleep_mode_or_lose_internet_connection(self):
        """
        DESCRIPTION: Move device to sleep mode or lose internet connection
        EXPECTED: 
        """
        pass

    def test_014_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step #2
        EXPECTED: 
        """
        pass

    def test_015_wake_device_up_or_restore_internet_connection_depends_on_step_13(self):
        """
        DESCRIPTION: Wake device up or restore internet connection (depends on step #13)
        EXPECTED: * 'reload components' is triggered in Console
        EXPECTED: * 'system-configuration' request is sent and returns up-to-date data in Network
        EXPECTED: * Config changes from step #2 are applied for Next Races widget
        """
        pass
