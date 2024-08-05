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
class Test_C64569601_Verify_that_Save_option_is_enabled_only_when_all_the_madatory_fields_are_filled(Common):
    """
    TR_ID: C64569601
    NAME: Verify that Save option is enabled only when all the madatory fields are filled
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

    def test_005_validate_save_button_enabled(self):
        """
        DESCRIPTION: Validate Save button enabled
        EXPECTED: * After entering  the mandatory fields Save button should be enable
        EXPECTED: * Click on save button
        """
        pass

    def test_006_validate_user_navigation_to_edit_buildyourmarket_pageclick_on_save_button_in_the_overlay(self):
        """
        DESCRIPTION: Validate User Navigation to Edit BuildYourMarket page
        DESCRIPTION: Click on Save button in the Overlay
        EXPECTED: * User should be navigated to Edit BuildYourMarket page
        """
        pass
