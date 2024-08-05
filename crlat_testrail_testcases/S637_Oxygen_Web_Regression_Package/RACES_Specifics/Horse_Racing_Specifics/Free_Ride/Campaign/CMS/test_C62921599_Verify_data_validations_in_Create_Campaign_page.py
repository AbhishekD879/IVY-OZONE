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
class Test_C62921599_Verify_data_validations_in_Create_Campaign_page(Common):
    """
    TR_ID: C62921599
    NAME: Verify data validations in Create Campaign page
    DESCRIPTION: This test case verifies data validations in Create Campaign page
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

    def test_005_click_on_create_campaign_button(self):
        """
        DESCRIPTION: Click on 'Create Campaign' button
        EXPECTED: Campaign page should be displayed with the below fields
        EXPECTED: * *Name
        EXPECTED: * Start date
        EXPECTED: * End date
        EXPECTED: * *Open Bet Campaign Id
        EXPECTED: * Opti move ID
        """
        pass

    def test_006_verify_the_data_validations_of_the_fields(self):
        """
        DESCRIPTION: Verify the data validations of the fields
        EXPECTED: * *Name : Free text box
        EXPECTED: * Start date : Date picker
        EXPECTED: * End date : Date picker
        EXPECTED: * *Open Bet Campaign Id : Free text box
        EXPECTED: * Opti move ID : Free text box
        """
        pass
