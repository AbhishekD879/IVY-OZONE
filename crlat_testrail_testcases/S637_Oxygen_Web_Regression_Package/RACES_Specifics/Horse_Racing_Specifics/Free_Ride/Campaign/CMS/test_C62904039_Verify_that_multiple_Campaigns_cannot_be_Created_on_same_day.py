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
class Test_C62904039_Verify_that_multiple_Campaigns_cannot_be_Created_on_same_day(Common):
    """
    TR_ID: C62904039
    NAME: Verify that multiple Campaigns cannot be Created on same day
    DESCRIPTION: This test case verifies multiple Campaigns cannot be Created on same day
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: Free Ride menu should be configured in CMS
    PRECONDITIONS: ***How to Configure Menu Item***
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

    def test_002_validate_the_display_of_free_ride_tab_in_left_side_menu_of_cms(self):
        """
        DESCRIPTION: Validate the display of 'Free Ride' tab in left side menu of CMS
        EXPECTED: User should be able to view the 'Free Ride' tab
        """
        pass

    def test_003_click_on_free_ride_tab(self):
        """
        DESCRIPTION: Click on 'Free Ride' tab
        EXPECTED: * User should be able to click on 'Free Ride' tab
        EXPECTED: * Sub Menu list of item/s should be displayed
        """
        pass

    def test_004_click_on_campaign_from_the_sub_menu(self):
        """
        DESCRIPTION: Click on Campaign from the sub menu
        EXPECTED: User should be navigate to Campaign page and the below fields should be displayed
        EXPECTED: ##When no Campaigns are configured##
        EXPECTED: * Create Campaign
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

    def test_005_create_multiple_campaigns(self):
        """
        DESCRIPTION: Create Multiple Campaigns
        EXPECTED: * User should be able to create only one campaign
        EXPECTED: * Warning message should be should be displayed when user tries to create multiple campaigns
        """
        pass
