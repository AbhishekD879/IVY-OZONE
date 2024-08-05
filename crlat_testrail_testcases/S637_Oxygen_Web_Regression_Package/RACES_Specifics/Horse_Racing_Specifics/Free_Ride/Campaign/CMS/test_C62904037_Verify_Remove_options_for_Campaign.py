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
class Test_C62904037_Verify_Remove_options_for_Campaign(Common):
    """
    TR_ID: C62904037
    NAME: Verify Remove options for Campaign
    DESCRIPTION: This test case verifies that User can Remove the existing Campaigns
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: Free Ride menu should be configured in CMS
    PRECONDITIONS: 3: campaigns should be created and displayed in Free ride -&gt; Campaigns
    PRECONDITIONS: 4: make sure campaign is not running currently
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

    def test_005_single_removalclick_on_remove_button(self):
        """
        DESCRIPTION: **Single Removal**
        DESCRIPTION: Click on Remove button
        EXPECTED: Confirmation Pop-up will be displayed with Yes and No options
        """
        pass

    def test_006_click_on_no_and_verify(self):
        """
        DESCRIPTION: Click on No and Verify
        EXPECTED: User should be redirected to the same page with the campaigns still displayed
        """
        pass

    def test_007_repeat_step_5_click_on_yes_and_verify(self):
        """
        DESCRIPTION: Repeat step 5 click on Yes and Verify
        EXPECTED: User should be redirected to the same page with the campaign removed
        EXPECTED: **If there is only one campaign**
        EXPECTED: Table should no longer be displayed
        """
        pass

    def test_008_make_sure_campaign_is_running_currently(self):
        """
        DESCRIPTION: Make sure campaign is running currently
        EXPECTED: 
        """
        pass

    def test_009_single_removalclick_on_remove_button(self):
        """
        DESCRIPTION: **Single Removal**
        DESCRIPTION: Click on Remove button
        EXPECTED: 'Campaign is live and running, shouldn't delete the campaign' pop up message should be displayed
        """
        pass
