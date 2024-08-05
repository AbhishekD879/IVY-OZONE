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
class Test_C59551015_Verify_user_is_able_to_view_Betradar_Scoreboard_Toggle_ON_OFF_feature_in_CMS(Common):
    """
    TR_ID: C59551015
    NAME: Verify user is able to view Betradar Scoreboard Toggle ON/OFF feature in CMS
    DESCRIPTION: Test case Verifies that User is able to view Toggle ON/OFF feature for Betradar Scoreboards section in CMS
    PRECONDITIONS: 1. User should have access to CMS
    PRECONDITIONS: 2. Betradar scoreboard section should present in CMS - system configuration - config
    """
    keep_browser_open = True

    def test_001_login_to_cms_and_navigate_to_betradar_section_from_cms___system_configuration___config___betradar_scoreboard(self):
        """
        DESCRIPTION: Login to CMS and navigate to betradar section from CMS - system configuration - config - betradar scoreboard
        EXPECTED: Betradar scoreboard config section should display
        """
        pass

    def test_002_verify_ui_of_betradar_config_section(self):
        """
        DESCRIPTION: Verify UI of betradar config section
        EXPECTED: UI should have following details
        EXPECTED: Title : Betradar Scoreboard
        EXPECTED: Right corner buttons : Edit table, Add property and remove group
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
        EXPECTED: details should save by enabling betradar scoreboard
        """
        pass

    def test_004_click_on_edit_table_and_disable_scoreboard(self):
        """
        DESCRIPTION: click on edit table and disable scoreboard
        EXPECTED: details should save
        """
        pass
