import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C64884614_Verify_data_validations_in_Season_page(Common):
    """
    TR_ID: C64884614
    NAME: Verify data validations in Season page
    DESCRIPTION: This test case verifies data validations in Season page
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: Season should be created and displayed in 1-2 Free
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_validate_the_display_of_seasons_in_sub_menu_list_of_items_in_1_2_free(self):
        """
        DESCRIPTION: Validate the display of 'Seasons' in Sub Menu list of item/s in 1-2 Free
        EXPECTED: User should be able to view Seasons
        """
        pass

    def test_003_click_on_seasons_from_the_sub_menu(self):
        """
        DESCRIPTION: Click on Seasons from the sub menu
        EXPECTED: User should be navigate to Seasons page and the below fields should be displayed
        EXPECTED: ##When at least one Season is configured##
        EXPECTED: * Create Season
        EXPECTED: * Table with below column Headers
        EXPECTED: * Season Name
        EXPECTED: * Start Date
        EXPECTED: * End Date
        EXPECTED: * Remove
        EXPECTED: * Edit
        EXPECTED: * Search bar should be available
        """
        pass

    def test_004_enter_data_validations_in_seasons_page(self):
        """
        DESCRIPTION: Enter data validations in seasons page
        EXPECTED: * Season Name - Allow to enter 50 characters
        EXPECTED: * Season related info -  Allow to enter 200 characters
        EXPECTED: * Primary Badge - Allow to enter 50 characters
        EXPECTED: * Secondary Badge - Allow to enter 50 characters
        EXPECTED: * Primary threshold value - Allow to enter 3 characters
        EXPECTED: * Secondary threshold value - Allow to enter 3 characters
        EXPECTED: * Reward - Allow to enter 3 characters (Primary and secondary)
        EXPECTED: * Reward: Cash/Freebet - Toggle (On/Off)
        EXPECTED: * Primary Congratulations Message - Allow to enter 100 characters
        EXPECTED: * Secondary Congratulations Message - Allow to enter 100 characters
        """
        pass
