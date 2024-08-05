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
class Test_C1924268_Verify_CMS_configuration_for_In_Play_Player_Markets(Common):
    """
    TR_ID: C1924268
    NAME: Verify CMS configuration for In-Play Player Markets
    DESCRIPTION: This test case verifies CMS configuration for In-Play Player Markets
    PRECONDITIONS: 1.
    PRECONDITIONS: CMS configuration: System configuration - Config:
    PRECONDITIONS: 'yourCallPlayerStatsName' config with following parameters:
    PRECONDITIONS: |||:Field name:|:Filed Type:|:Possible value:|:Default value:
    PRECONDITIONS: || Name |Input  | Any Text |  #YourCall - Player Markets
    PRECONDITIONS: || Enabled|  Checkbox| True/False |  Enabled
    PRECONDITIONS: || Row 3 .. |  |  |
    PRECONDITIONS: 2. Event with In-Play Player Stats markets is configured in TI tool
    """
    keep_browser_open = True

    def test_001_in_cms___system_configuration___your_call_player_stats_name_section_change_name_for_the_main_in_play_player_stats_accordion_and_save_changesopen_event_with_available_player_marketsverify_name_of_the_main_accordion_displaying_according_to_cms_configuration(self):
        """
        DESCRIPTION: In CMS - System Configuration - Your Call Player Stats Name section change name for the main In-Play Player Stats accordion and save changes.
        DESCRIPTION: Open event with available Player Markets.
        DESCRIPTION: Verify name of the main accordion displaying according to CMS configuration
        EXPECTED: Configured in 'CMS - System Configuration - Your Call Player Stats Name' name is displayed in application
        """
        pass

    def test_002_in_cms_change_name_for_the_main_accordion_and_save_changesrefresh_the_page_in_application_and_verify_name_displaying(self):
        """
        DESCRIPTION: In CMS change name for the main accordion and save changes.
        DESCRIPTION: Refresh the page in application and verify name displaying.
        EXPECTED: Updated in CMS name is displayed
        """
        pass

    def test_003_in_cms_uncheck_enabled_checkbox_and_save_changesrefresh_the_page_in_application_and_verify_player_markets_displaying(self):
        """
        DESCRIPTION: In CMS uncheck 'Enabled' checkbox and save changes.
        DESCRIPTION: Refresh the page in application and verify Player Markets displaying
        EXPECTED: Player Markets are not displayed for the event
        """
        pass

    def test_004_in_cms_check_enabled_checkbox_and_save_changesrefresh_the_page_in_application_and_verify_player_markets_displaying(self):
        """
        DESCRIPTION: In CMS check 'Enabled' checkbox and save changes.
        DESCRIPTION: Refresh the page in application and verify Player Markets displaying
        EXPECTED: Player Markets are displayed for the event
        """
        pass
