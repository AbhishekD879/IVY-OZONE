import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C60709303_Match_day_rewards_Page__table_structure_for_rewards_configuration__Edit_table_and_delete_tier_info(Common):
    """
    TR_ID: C60709303
    NAME: Match day rewards Page - table structure for rewards configuration - Edit table and delete tier info
    DESCRIPTION: This test case is to validate Edit table and delete row functionality of table structure for rewards configuration in match day rewards Page
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  configuration for  Euro Loyalty Page should done
    """
    keep_browser_open = True

    def test_001_hit_the_cms_url(self):
        """
        DESCRIPTION: Hit the CMS URL
        EXPECTED: User is on CMS application
        """
        pass

    def test_002_navigate_to_special_pages___match_day_rewards_page_table_creation_section(self):
        """
        DESCRIPTION: Navigate to special pages - Match day rewards page table creation section
        EXPECTED: Match day rewards page should display
        """
        pass

    def test_003_verify_ui_of_table_creation_section(self):
        """
        DESCRIPTION: Verify UI of table creation section
        EXPECTED: UI should have following details
        EXPECTED: Titile : RewardsConfiguration
        EXPECTED: right corner tow buttons Edit table and add property should present
        EXPECTED: Table with following columns should present
        EXPECTED: Tier No : mandatory
        EXPECTED: Freebet Locations : mandatory
        EXPECTED: OfferID/Sequence : mandatory
        EXPECTED: Action : Delete
        """
        pass

    def test_004_click_on_edit_table_button_and_verify(self):
        """
        DESCRIPTION: Click on edit table button and verify
        EXPECTED: All the rows in table should display in edit mode
        EXPECTED: end edit table button should display
        """
        pass

    def test_005_update_table_with_required_details_and_save_changes(self):
        """
        DESCRIPTION: Update table with required details and save changes
        EXPECTED: Detailed should be saved and respective values should populate in FE
        """
        pass

    def test_006_update_multiple_rows_and_cells_in_table_with_required_details_and_save_changes(self):
        """
        DESCRIPTION: Update multiple rows and cells in table with required details and save changes
        EXPECTED: Details should update accordingly
        """
        pass

    def test_007_update_tier_info_after_user_is_allocation_some_badges(self):
        """
        DESCRIPTION: Update tier info after user is allocation some badges
        EXPECTED: Details should update accordingly
        """
        pass

    def test_008_click_on_delete_button_of_any_specific_tier_and_verify(self):
        """
        DESCRIPTION: click on delete button of any specific tier and verify
        EXPECTED: if respective tier user has got rewards earlier all the details should deleted and badges should display in disabled mode
        """
        pass

    def test_009_reenter_all_the_details_which_are_deleted_in_above_step_and_verify(self):
        """
        DESCRIPTION: reenter all the details which are deleted in above step and verify
        EXPECTED: all the tier details should reload with proper values
        """
        pass
