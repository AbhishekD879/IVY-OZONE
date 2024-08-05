import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C62904036_Verify_Edit_option_for_Campaign_before_pot_creation(Common):
    """
    TR_ID: C62904036
    NAME: Verify Edit option for Campaign before pot creation
    DESCRIPTION: This test case verifies that User can Edit the existing campaigns before pot creation
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: Free Ride menu should be configured in CMS
    PRECONDITIONS: 3: Campaign should be created in Free Ride
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: Free Ride
    PRECONDITIONS: Path: /Free Ride
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: Campaign
    PRECONDITIONS: Path: /Campaign
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_click_on_free_ride_tabin_left_side_menu_of_cms(self):
        """
        DESCRIPTION: Click on 'Free Ride' tab in left side menu of CMS
        EXPECTED: * User should be able to click on 'Free Ride' tab
        EXPECTED: * Sub Menu list of item/s should be displayed
        """
        pass

    def test_003_click_on_campaign_from_the_sub_menu(self):
        """
        DESCRIPTION: Click on Campaign from the sub menu
        EXPECTED: User should be navigate to Campaign page and the below fields should be displayed
        EXPECTED: ##When at least one Campaign is configured##
        EXPECTED: * Create campaign
        EXPECTED: * Table with below column Headers
        EXPECTED: * Campaign Name
        EXPECTED: * Start Date
        EXPECTED: * End Date
        EXPECTED: * Remove
        EXPECTED: * Edit
        EXPECTED: * Search bar should be available
        """
        pass

    def test_004_click_on_edit_button(self):
        """
        DESCRIPTION: Click on Edit button
        EXPECTED: User should be redirected to Edit Campaign Details page
        """
        pass

    def test_005_verify_after_making_changes_in_the_campaign_tab(self):
        """
        DESCRIPTION: Verify after making changes in the Campaign Tab
        EXPECTED: User should be able to save the changes successfully
        """
        pass

    def test_006_verify_after_making_changes_in_the_questions_tab(self):
        """
        DESCRIPTION: Verify after making changes in the Questions Tab
        EXPECTED: User should be able to save the changes successfully
        """
        pass
