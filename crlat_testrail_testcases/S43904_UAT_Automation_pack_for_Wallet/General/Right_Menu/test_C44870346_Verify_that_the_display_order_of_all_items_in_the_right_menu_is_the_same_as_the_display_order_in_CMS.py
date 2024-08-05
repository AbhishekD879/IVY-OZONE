import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870346_Verify_that_the_display_order_of_all_items_in_the_right_menu_is_the_same_as_the_display_order_in_CMS(Common):
    """
    TR_ID: C44870346
    NAME: Verify that the display order of all items in the right menu is the same as the display order in CMS.
    DESCRIPTION: 
    PRECONDITIONS: User is logged in the application and in CMS.
    """
    keep_browser_open = True

    def test_001_navigate_to_my_accountright_menu_in_the_application_compare_the_display_order_of_the_options_available_in_the_right_menu_with_the_display_order_configured_in_cms_verify(self):
        """
        DESCRIPTION: Navigate to My Account/Right menu in the application. Compare the display order of the options available in the right menu with the display order configured in CMS. Verify.
        EXPECTED: The display order of the options displayed in the right menu is according to the order configured in CMS.
        """
        pass

    def test_002_change_the_display_order_of_the_options_in_cms_ie_change_the_order_for_logout_and_place_it_above_banking_and_save_the_changes_in_cms_verify_in_the_right_menu_in_the_application(self):
        """
        DESCRIPTION: Change the display order of the options in CMS, i.e. change the order for Logout and place it above Banking and save the changes in CMS. Verify in the right menu in the application.
        EXPECTED: The display order of the options displayed in the right menu is according to the updated display order configured in CMS, i.e. Logout is displayed above Banking.
        """
        pass
