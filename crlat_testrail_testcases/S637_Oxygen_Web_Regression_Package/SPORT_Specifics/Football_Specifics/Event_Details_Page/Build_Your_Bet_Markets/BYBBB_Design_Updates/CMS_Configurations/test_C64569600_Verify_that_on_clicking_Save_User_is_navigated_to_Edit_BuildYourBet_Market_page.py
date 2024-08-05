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
class Test_C64569600_Verify_that_on_clicking_Save_User_is_navigated_to_Edit_BuildYourBet_Market_page(Common):
    """
    TR_ID: C64569600
    NAME: Verify that on clicking Save User is navigated to Edit BuildYourBet Market page
    DESCRIPTION: 
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

    def test_008_validate_the__save_button_display(self):
        """
        DESCRIPTION: Validate the  Save button display
        EXPECTED: * When click on the save the enter Buildyour Market data should be saved
        """
        pass

    def test_009_validate_user_navigation_to_edit_buildyourmarket_pageclick_on_save_button_in_the_overlay(self):
        """
        DESCRIPTION: Validate User Navigation to Edit BuildYourMarket page
        DESCRIPTION: Click on Save button in the Overlay
        EXPECTED: User should be navigated to Edit BuildYourMarket page
        """
        pass
