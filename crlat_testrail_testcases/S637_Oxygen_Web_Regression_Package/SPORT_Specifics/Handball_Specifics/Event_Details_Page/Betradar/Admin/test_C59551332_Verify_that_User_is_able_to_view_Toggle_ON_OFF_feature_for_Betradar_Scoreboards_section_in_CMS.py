import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C59551332_Verify_that_User_is_able_to_view_Toggle_ON_OFF_feature_for_Betradar_Scoreboards_section_in_CMS(Common):
    """
    TR_ID: C59551332
    NAME: Verify that User is able to view Toggle ON/OFF feature for Betradar Scoreboards section in CMS
    DESCRIPTION: This test case verifies the possibility to enable/disable Bet radar Scoreboard on:
    DESCRIPTION: Mobile devices;
    DESCRIPTION: Tablet devices;
    DESCRIPTION: Desktop browsers;
    PRECONDITIONS: 1: Navigate to Sports Menu(Handball)/From A-Z all Sports->Handball
    PRECONDITIONS: 2: Event should be Pre-Play.
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    PRECONDITIONS: CMS > System Configuration > Structure > Betradar Scoreboard
    """
    keep_browser_open = True

    def test_001_make_following_settingsdesktop_enabled_uncheckedmobile_enabled_checkedtablet_enabled_checkedclick_submit_button(self):
        """
        DESCRIPTION: Make following settings:
        DESCRIPTION: desktop Enabled unchecked
        DESCRIPTION: mobile Enabled checked
        DESCRIPTION: tablet Enabled checked
        DESCRIPTION: Click Submit button
        EXPECTED: Changes Should saved
        """
        pass

    def test_002_load_oxygen_application_on_the_mobile_device__navigate_to_handball_edp_with_mapped_bet_radar_scoreboard(self):
        """
        DESCRIPTION: Load Oxygen application on the mobile device > Navigate to Handball EDP with mapped Bet radar Scoreboard
        EXPECTED: Bet Radar Scoreboard is available
        """
        pass

    def test_003_load_oxygen_application_on_the_desktop_device__navigate_to_handball_edp_with_mapped_bet_radar_scoreboard(self):
        """
        DESCRIPTION: Load Oxygen application on the Desktop device > Navigate to Handball EDP with mapped Bet radar Scoreboard
        EXPECTED: Bet Radar Scoreboard should not available
        """
        pass

    def test_004_load_oxygen_application_on_the_tablet_device__navigate_to_handball_edp_with_mapped_bet_radar_scoreboard(self):
        """
        DESCRIPTION: Load Oxygen application on the tablet device > Navigate to Handball EDP with mapped Bet radar Scoreboard
        EXPECTED: Bet Radar Scoreboard is available
        """
        pass

    def test_005_in_cms__system_configuration__bet_radar_scoreboard_and_make_following_settingmake_following_settingsdesktop_enabled_checkedmobile_enabled_uncheckedtablet_enabled_uncheckedclick_submit_button(self):
        """
        DESCRIPTION: In CMS > System-configuration > Bet radar Scoreboard and make following setting:
        DESCRIPTION: Make following settings:
        DESCRIPTION: desktop Enabled checked
        DESCRIPTION: mobile Enabled unchecked
        DESCRIPTION: tablet Enabled unchecked
        DESCRIPTION: Click Submit button
        EXPECTED: Changes are saved
        """
        pass

    def test_006_load_oxygen_application_on_the_mobile_device__navigate_to_handball_edp_with_mapped_bet_radar_scoreboard(self):
        """
        DESCRIPTION: Load Oxygen application on the mobile device > Navigate to Handball EDP with mapped Bet radar Scoreboard
        EXPECTED: Bet Radar Scoreboard is available
        """
        pass

    def test_007_load_oxygen_application_on_the_desktop_device__navigate_to_handball_edp_with_mapped_bet_radar_scoreboard(self):
        """
        DESCRIPTION: Load Oxygen application on the Desktop device > Navigate to Handball EDP with mapped Bet radar Scoreboard
        EXPECTED: Bet Radar Scoreboard should not available
        """
        pass

    def test_008_load_oxygen_application_on_the_tablet_device__navigate_to_handball_edp_with_mapped_bet_radar_scoreboard(self):
        """
        DESCRIPTION: Load Oxygen application on the tablet device > Navigate to Handball EDP with mapped Bet radar Scoreboard
        EXPECTED: Bet Radar Scoreboard is available
        """
        pass
