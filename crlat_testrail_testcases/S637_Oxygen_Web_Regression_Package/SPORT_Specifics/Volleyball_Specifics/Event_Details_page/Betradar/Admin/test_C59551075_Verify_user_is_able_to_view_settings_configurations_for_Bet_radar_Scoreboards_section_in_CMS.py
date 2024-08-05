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
class Test_C59551075_Verify_user_is_able_to_view_settings_configurations_for_Bet_radar_Scoreboards_section_in_CMS(Common):
    """
    TR_ID: C59551075
    NAME: Verify user is able to view settings configurations for Bet radar Scoreboards section in CMS
    DESCRIPTION: Verify that User is able to view settings configurations for Bet radar Scoreboards section in CMS
    PRECONDITIONS: 1: User should have access to CMS
    PRECONDITIONS: 2: Betradar scoreboard section should be available in CMS
    PRECONDITIONS: CMS navigation:
    PRECONDITIONS: CMS> System Configuration > Config
    """
    keep_browser_open = True

    def test_001_login_to_cms_and_navigate_to_bet_radar_section_from_cms___system_configuration___config___bet_radar_scoreboard(self):
        """
        DESCRIPTION: Login to CMS and navigate to bet radar section from CMS - system configuration - config - bet radar scoreboard
        EXPECTED: Betradar scoreboard config section should display
        """
        pass

    def test_002_verify_ui_of_betradar_config_section(self):
        """
        DESCRIPTION: Verify UI of betradar config section
        EXPECTED: UI should have following details
        EXPECTED: Title : Bet radar Scoreboard
        EXPECTED: Right corner buttons L Edit table, Add property and remove group
        EXPECTED: Table with following columns should display
        EXPECTED: Field Name
        EXPECTED: Field Type
        EXPECTED: Possible
        EXPECTED: value
        EXPECTED: Default value
        EXPECTED: Action
        """
        pass

    def test_003_click_on_edit_table_and_add_a_fields_or_row_with_following_detailsfield_name__enabledfield_type__check_boxpossible_values__truefalsedefault_value__check_box_checkand_click_on_save_changes_button(self):
        """
        DESCRIPTION: Click on edit table and add a fields or row with following details
        DESCRIPTION: Field name = Enabled
        DESCRIPTION: Field type = Check box
        DESCRIPTION: Possible values = true/False
        DESCRIPTION: Default value = check box (check)
        DESCRIPTION: and click on save changes button
        EXPECTED: Details should be saved
        """
        pass

    def test_004_click_on_edit_table_and_disable_scoreboard(self):
        """
        DESCRIPTION: Click on edit table and disable scoreboard
        EXPECTED: Details should be saved
        """
        pass
