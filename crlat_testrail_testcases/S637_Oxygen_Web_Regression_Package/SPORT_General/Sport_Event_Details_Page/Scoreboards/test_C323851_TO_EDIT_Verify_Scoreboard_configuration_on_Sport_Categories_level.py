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
class Test_C323851_TO_EDIT_Verify_Scoreboard_configuration_on_Sport_Categories_level(Common):
    """
    TR_ID: C323851
    NAME: TO EDIT Verify Scoreboard configuration on Sport Categories level
    DESCRIPTION: This test case verifies Scoreboard configuration in CMS on Sport Categories level
    PRECONDITIONS: CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 'Show ScoreBoard' (YES) and 'ScoreBoard Url' are set in Scoreboard section in System Configuration tab
    """
    keep_browser_open = True

    def test_001_in_cms_navigate_to_menus___sport_categories___select_sport_without_configured_scoreboard(self):
        """
        DESCRIPTION: In CMS navigate to Menus -> Sport Categories -> select <sport> without configured scoreboard
        EXPECTED: 
        """
        pass

    def test_002_tick_show_scoreboardenter_scoreboard_url_value_different_than_in_scoreboard_section_in_system_configuration_tabsave_changes(self):
        """
        DESCRIPTION: Tick 'Show Scoreboard'.
        DESCRIPTION: Enter 'ScoreBoard Url' value, different than in Scoreboard section in System Configuration tab.
        DESCRIPTION: Save changes
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_003__navigate_to_refreshed_coral_application_open_details_page_of_live_event_from_sport_edited_in_previous_steps_check_link_for_scoreboard_request_in_network_tab(self):
        """
        DESCRIPTION: * Navigate to refreshed Coral application
        DESCRIPTION: * Open Details Page of Live event from <sport> edited in previous steps
        DESCRIPTION: * Check link for scoreboard request in Network tab
        EXPECTED: * Scoreboard is shown, if present in **scoreboard** response
        EXPECTED: * Link is the same as set is step #3 plus /getWidget/0/<OpenBet_Id>/scoreboard
        """
        pass

    def test_004_in_cms_change_scoreboard_url_value_and_save_changes(self):
        """
        DESCRIPTION: In CMS change 'ScoreBoard Url' value and save changes
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_005__navigate_to_refreshed_coral_application_open_details_page_of_live_event_from_sport_edited_in_previous_steps_check_link_for_scoreboard_request_in_network_tab(self):
        """
        DESCRIPTION: * Navigate to refreshed Coral application
        DESCRIPTION: * Open Details Page of Live event from <sport> edited in previous steps
        DESCRIPTION: * Check link for scoreboard request in Network tab
        EXPECTED: * Scoreboard is shown, if present in **scoreboard** response
        EXPECTED: * Link in Network tab is the same as set is step #6 plus /getWidget/0/<OpenBet_Id>/scoreboard
        """
        pass

    def test_006_in_cms_untick_show_scoreboard_and_save_changes(self):
        """
        DESCRIPTION: in CMS untick 'Show Scoreboard' and save changes
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_007__navigate_to_refreshed_coral_application_open_details_page_of_live_event_from_sport_edited_in_previous_steps_check_link_for_scoreboard_request_in_network_tab(self):
        """
        DESCRIPTION: * Navigate to refreshed Coral application
        DESCRIPTION: * Open Details Page of Live event from <sport> edited in previous steps
        DESCRIPTION: * Check link for scoreboard request in Network tab
        EXPECTED: * Scoreboard is shown, if present in **scoreboard** response
        EXPECTED: * Scoreboard Url is taken from System Configuration settings
        """
        pass

    def test_008_in_cms_tick_show_scoreboard_and_save_changes(self):
        """
        DESCRIPTION: In CMS tick 'Show Scoreboard' and save changes
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_009_in_cms_set_show_scoreboard_as_no_in_system_configurationclick_submit_button(self):
        """
        DESCRIPTION: In CMS set 'Show ScoreBoard' as 'NO' in System Configuration.
        DESCRIPTION: Click 'Submit' button.
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_010__navigate_to_refreshed_coral_application_open_details_page_of_live_event_from_sport_edited_in_previous_step_check_link_for_scoreboard_request_in_network_tab(self):
        """
        DESCRIPTION: * Navigate to refreshed Coral application
        DESCRIPTION: * Open Details Page of Live event from <sport> edited in previous step
        DESCRIPTION: * Check link for scoreboard request in Network tab
        EXPECTED: * Scoreboard request is NOT sent for all sports
        """
        pass
