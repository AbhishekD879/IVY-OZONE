import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C64569605_Verify_that_User_can_Search_the_Market_and_edit_the_Market_or_remove_market(Common):
    """
    TR_ID: C64569605
    NAME: Verify that User can Search the Market and edit the Market or remove market
    DESCRIPTION: Verify that User can Search the Market and edit the Market or remove market
    PRECONDITIONS: 1: User should have access to CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin User
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_byb_gt_byb_markets(self):
        """
        DESCRIPTION: Navigate to BYB &gt; BYB Markets
        EXPECTED: Verify that User is able to view Create BuildYourMarket button
        EXPECTED: Table Headers
        EXPECTED: 1: Market Title
        EXPECTED: 2: Market Group Name
        EXPECTED: 3: Market Grouping
        EXPECTED: 4: Incident Grouping
        EXPECTED: 5: Market Type
        EXPECTED: 6: Popular Market
        EXPECTED: 7: Market Description
        EXPECTED: 8: Remove
        EXPECTED: 9: Edit
        """
        pass

    def test_003_click_on_create_buildyourmarket_button(self):
        """
        DESCRIPTION: Click on Create BuildYourMarket button
        EXPECTED: * Overlay should be displayed
        EXPECTED: * Below fields should be displayed in the Overlay
        EXPECTED: 1: Market Title
        EXPECTED: 2: Market Group Name
        EXPECTED: 3: Market Grouping
        EXPECTED: 4: Incident Grouping
        EXPECTED: 5: Market Type
        EXPECTED: 6: Market Description
        EXPECTED: 7: Popular Market Check Box
        EXPECTED: * Save and Cancel button should be displayed
        """
        pass

    def test_004_validate_the_mandatory_fields(self):
        """
        DESCRIPTION: Validate the Mandatory fields
        EXPECTED: * Market Title and Market Group Name should be the ONLY mandatory fields
        EXPECTED: * Save button is enabled ONLY when Market Title and Market Group Name fields are filled
        """
        pass

    def test_005_validate_that_user_is_able_to_enter_incident_grouping_market_grouping_market_description(self):
        """
        DESCRIPTION: Validate that User is able to enter Incident Grouping, Market Grouping, Market Description
        EXPECTED: * User should be able to enter Incident Grouping, Market
        """
        pass

    def test_006_validate_market_type_dropdown_field(self):
        """
        DESCRIPTION: Validate Market Type Dropdown field
        EXPECTED: * User should be able to view the below options N/A, Player Bet, Team Bet
        EXPECTED: * Dropdown should be a single select and NOT multi select
        """
        pass

    def test_007_validate_the_popular_markets_checkbox(self):
        """
        DESCRIPTION: Validate the Popular Markets Checkbox
        EXPECTED: * User should be able to enable the Popular Market check box
        """
        pass

    def test_008_validate_user_navigation_to_edit_buildyourmarket_pageclick_on_save_button_in_the_overlay(self):
        """
        DESCRIPTION: Validate User Navigation to Edit BuildYourMarket page
        DESCRIPTION: Click on Save button in the Overlay
        EXPECTED: * User should be navigated to Edit BuildYourMarket page
        """
        pass

    def test_009_click_on_edit_button_for_the_market_created(self):
        """
        DESCRIPTION: Click on edit button for the market created
        EXPECTED: * Edit BuildYourBet Market screen appers do some changes for any of the fields and click on save
        EXPECTED: * Pop up appers with Yes/No click on yes
        EXPECTED: ![](index.php?/attachments/get/cefdaace-33cd-44e0-b594-9121165c6c2e)
        EXPECTED: * Pop up appears with BuildYourBet Market is Saved
        EXPECTED: ![](index.php?/attachments/get/377c7c89-9846-41d2-b296-0c3fda54e502)
        """
        pass

    def test_010_check_the_edited_market_fields(self):
        """
        DESCRIPTION: Check the Edited Market fields
        EXPECTED: User edited date should be save
        """
        pass

    def test_011_navigate_to_any_of_the_market_created_and_check_the_remove_button_available(self):
        """
        DESCRIPTION: Navigate to any of the market created and check the remove button available
        EXPECTED: * Click on Remove button
        EXPECTED: * Remove BuildYourBet Market pop screen will display with Yes/No
        EXPECTED: ![](index.php?/attachments/get/8823c2dd-4afa-4f0c-b519-daf2c05fcd13)
        """
        pass

    def test_012_validate_remove_completed_pop_up_appears(self):
        """
        DESCRIPTION: Validate Remove Completed pop up appears
        EXPECTED: * Remove Pop up with Ok button
        EXPECTED: * Cick on Ok will remove the market
        EXPECTED: ![](index.php?/attachments/get/9a30e7c9-7ef0-49ec-9367-16359949abc5)
        """
        pass

    def test_013_verify_admin_is_able_to_search_for_any_market(self):
        """
        DESCRIPTION: Verify Admin is able to Search for any Market
        EXPECTED: Should be able to search
        EXPECTED: ![](index.php?/attachments/get/4a4b4cf6-4aa5-4b46-9064-785417a4147b)
        """
        pass
