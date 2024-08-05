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
class Test_C62867374_Verify_the_CMS_configurations_for_creating_Campaign_in_Free_Ride(Common):
    """
    TR_ID: C62867374
    NAME: Verify the CMS configurations for creating Campaign in Free Ride
    DESCRIPTION: This test case verifies CMS configurations for creating Campaign in Free Ride.
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

    def test_004_validate_the_display_of_campaign_in_sub_menu_list_of_items(self):
        """
        DESCRIPTION: Validate the display of 'Campaign' in Sub Menu list of item/s
        EXPECTED: User should be able to view Campaign
        """
        pass

    def test_005_click_on_campaign_from_the_sub_menu(self):
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

    def test_006_click_on_create_campaign_button(self):
        """
        DESCRIPTION: Click on 'Create Campaign' button
        EXPECTED: Campaign page should be displayed with the below fields
        EXPECTED: * *Name
        EXPECTED: * Start date
        EXPECTED: * End date
        EXPECTED: * *Open Bet Campaign Id
        EXPECTED: * *Opti move Id
        """
        pass

    def test_007_enter_data_in_the_above_fields(self):
        """
        DESCRIPTION: Enter data in the above fields
        EXPECTED: User should be able to enter the details
        """
        pass

    def test_008_click_on_create_campaign(self):
        """
        DESCRIPTION: Click on Create Campaign
        EXPECTED: * Campaign should be created successfully
        EXPECTED: * User should be in campaign details page with all the entered data
        EXPECTED: * Campaign ID should be displayed in the URL
        EXPECTED: * Save, Revert changes and Remove CTAs should be displayed
        EXPECTED: * Save option should be in disabled mode
        """
        pass
