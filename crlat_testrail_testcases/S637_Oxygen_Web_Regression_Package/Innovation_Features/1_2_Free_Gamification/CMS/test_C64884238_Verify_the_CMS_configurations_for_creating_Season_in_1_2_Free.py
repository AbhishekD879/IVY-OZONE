import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C64884238_Verify_the_CMS_configurations_for_creating_Season_in_1_2_Free(Common):
    """
    TR_ID: C64884238
    NAME: Verify the CMS configurations for creating Season in 1-2 Free
    DESCRIPTION: This test case verifies CMS configurations for creating Season in 1-2 Free
    PRECONDITIONS: 1: Login to CMS
    PRECONDITIONS: 2: Seasons sub menu should be configured in CMS
    PRECONDITIONS: ***How to Configure Sub Menu Item***
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: Seasons
    PRECONDITIONS: Path: /Seasons
    """
    keep_browser_open = True

    def test_001_validate_the_display_of_seasons_in_sub_menu_list_of_items_in_1_2_free(self):
        """
        DESCRIPTION: Validate the display of 'Seasons' in Sub Menu list of item/s in 1-2 Free
        EXPECTED: User should be able to view Seasons
        """
        pass

    def test_002_click_on_seasons_from_the_sub_menu(self):
        """
        DESCRIPTION: Click on Seasons from the sub menu
        EXPECTED: User should be navigate to Seasons page and the below fields should be displayed
        EXPECTED: ##When no Seasons are configured##
        EXPECTED: * Create Season
        EXPECTED: ##When at least one Season is configured##
        EXPECTED: * Create Season
        EXPECTED: * Table with below column Headers
        EXPECTED: * Season Name
        EXPECTED: * Start Date
        EXPECTED: * End Date
        EXPECTED: * Remove
        EXPECTED: * Edit
        EXPECTED: * Search bar should be available
        """
        pass

    def test_003_click_on_create_season_button(self):
        """
        DESCRIPTION: Click on 'Create Season' button
        EXPECTED: Season page should be displayed with the below fields
        EXPECTED: * Season Name
        EXPECTED: * Season related info
        EXPECTED: * Start date
        EXPECTED: * End date
        EXPECTED: * Add Team
        """
        pass

    def test_004_click_on_add_team(self):
        """
        DESCRIPTION: Click on Add Team
        EXPECTED: Add Team should be clickable and Table with below fields are displayed
        EXPECTED: * Team Name (Dropdown)
        EXPECTED: * Image URL (Image upload/URL/Sitecore)
        EXPECTED: * Edit
        EXPECTED: * Delete
        """
        pass

    def test_005_verify_edit_and_delete_options(self):
        """
        DESCRIPTION: Verify Edit and Delete options
        EXPECTED: User should be able to Edit and Delete the added teams
        """
        pass

    def test_006_verify_display_of_badges_rewarding_section(self):
        """
        DESCRIPTION: Verify display of Badges Rewarding Section
        EXPECTED: Badges Rewarding section should be displayed below to Teams Table
        """
        pass

    def test_007_verify_the_display_of_fields_in_badges_rewarding_section(self):
        """
        DESCRIPTION: Verify the display of fields in Badges Rewarding section
        EXPECTED: Below fields should be displayed
        EXPECTED: * Primary Badges : &lt;&lt;&gt;Number&gt;
        EXPECTED: * Rewards: Cash/Prize Toggle and Amount:£
        EXPECTED: * Primary Predictions Congratulations Message
        EXPECTED: * Secondary Badges : &lt;&lt;&gt;Number&gt;
        EXPECTED: * Rewards: Cash/Prize Toggle and Amount:£
        EXPECTED: * Secondary Predictions Congratulations Message
        """
        pass

    def test_008_enter_the_required_details_and_click_on_save(self):
        """
        DESCRIPTION: Enter the required details and click on save
        EXPECTED: * Season should be created successfully with the provided details
        """
        pass
