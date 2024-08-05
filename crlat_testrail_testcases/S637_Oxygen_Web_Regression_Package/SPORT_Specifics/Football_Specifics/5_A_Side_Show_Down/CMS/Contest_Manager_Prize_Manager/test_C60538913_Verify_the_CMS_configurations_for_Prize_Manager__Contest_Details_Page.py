import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.5_a_side
@vtest
class Test_C60538913_Verify_the_CMS_configurations_for_Prize_Manager__Contest_Details_Page(Common):
    """
    TR_ID: C60538913
    NAME: Verify the CMS configurations for Prize Manager - Contest Details Page
    DESCRIPTION: This test case verifies all the fields displayed under Prize Manager - Contest Details page in CMS > 5 A Side showdown tab
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_click_on_5_a_side_showdown_tab(self):
        """
        DESCRIPTION: Click on '5-A Side showdown' tab
        EXPECTED: User should be navigate to Contest page and the below should be displayed
        EXPECTED: ##When no Contests are configured##
        EXPECTED: * Add New Contest
        EXPECTED: ##When at least one Contest is configured##
        EXPECTED: * Add New Contest
        EXPECTED: * Table with below column Headers
        EXPECTED: * Contest Name
        EXPECTED: * Date - Event Start Date
        EXPECTED: * Active
        EXPECTED: * Remove
        EXPECTED: * Edit
        EXPECTED: * Table should include a drag and drop before the Contest name
        EXPECTED: * Search bar should be available
        """
        pass

    def test_003__click_on_add_new_contest_button_and_enter_all_mandatory_fields_name_start_date_entry_stake_click_on_saveentry_stake_can_have_decimal_value_also(self):
        """
        DESCRIPTION: * Click on 'Add New Contest' button and Enter all mandatory fields
        DESCRIPTION: * Name
        DESCRIPTION: * Start Date
        DESCRIPTION: * Entry Stake
        DESCRIPTION: * Click on Save
        DESCRIPTION: **Entry Stake can have Decimal Value also**
        EXPECTED: * User should be able to enter all the details
        EXPECTED: * User should be able to save the details
        EXPECTED: * User should be navigated to Contest edit details page
        """
        pass

    def test_004_scroll_down_and_verify_prize_pool__add_a_prize_section(self):
        """
        DESCRIPTION: Scroll down and Verify Prize Pool & Add A Prize Section
        EXPECTED: User should be able to view the Prize Pool & Add A Prize Section
        """
        pass

    def test_005_validate_the_configurations_in_prize_pool(self):
        """
        DESCRIPTION: Validate the Configurations in Prize Pool
        EXPECTED: * Below fields should be displayed
        EXPECTED: * Cash
        EXPECTED: * First Place
        EXPECTED: * Tickets
        EXPECTED: * Free Bets
        EXPECTED: * Vouchers
        EXPECTED: * Total Prizes
        EXPECTED: * Summary
        EXPECTED: * *Note:All the above fields are Not Mandatory*
        """
        pass

    def test_006_click_on_add_a_prize_button_below_prize_pool_section(self):
        """
        DESCRIPTION: Click on 'Add A Prize' button below Prize Pool Section
        EXPECTED: * Below fields are displayed
        EXPECTED: * *Prize Type
        EXPECTED: * Prize Value
        EXPECTED: * Prize Text
        EXPECTED: * Prize Icon
        EXPECTED: * Prize Signposting
        EXPECTED: * *% of Field
        EXPECTED: * *# of Entries
        EXPECTED: * **Note: Only Prize Type And % of Field *OR* # of Entries are required fields**
        EXPECTED: * When Prize Type is Cash or Free bet User can enter decimal value in Prize Value
        EXPECTED: * User can enter more than 100 rows - No restriction or limitation for the rows
        """
        pass

    def test_007_verify_by_entering_prize_type_both__of_field_and__of_entries_in_add_a_prize_section(self):
        """
        DESCRIPTION: Verify by entering Prize Type, both % of Field and # of Entries in Add a Prize section
        EXPECTED: * User should be able to enter in prize Type and both % of Field and # of Entries
        EXPECTED: * User should be able to save successfully
        """
        pass

    def test_008_verify_that_user_is_able_to_enter_____in__of_entries_and__of_field(self):
        """
        DESCRIPTION: Verify that User is able to enter (,) (*) (-) in # of Entries and % of field
        EXPECTED: * User should be able to enter (,) (*) (-) in # of Entries and % of field
        """
        pass

    def test_009_verify_save_button_when_mandatory_fields_are_not_filled_in_add_a_prizemandatory_fields___prize_type____of_field_or__of_entries(self):
        """
        DESCRIPTION: Verify Save button when mandatory fields are not filled in Add a Prize
        DESCRIPTION: **Mandatory Fields**
        DESCRIPTION: --> Prize Type
        DESCRIPTION: --> % of Field [OR] # of Entries
        EXPECTED: * Save button should not be enabled
        """
        pass

    def test_010_verify_by_entering_prize_type_only__of_field_and_not__of_entriesorprize_type_only__of_entries_and_not__of_field_in_add_a_prize_section(self):
        """
        DESCRIPTION: Verify by entering Prize Type, only % of Field and NOT # of Entries
        DESCRIPTION: [OR]
        DESCRIPTION: Prize Type, only # of Entries and NOT % of Field in Add a Prize section
        EXPECTED: * Save button should be enabled in either case and changes should be saved successfully
        """
        pass
