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
class Test_C44870340_Verify_that_the_display_order_of_all_items_in_the_My_Account_menu_is_the_same_as_the_display_order_in_CMS(Common):
    """
    TR_ID: C44870340
    NAME: Verify that the display order of all items in the My Account menu is the same as the display order in CMS.
    DESCRIPTION: 
    PRECONDITIONS: User is logged in the application and in CMS.
    """
    keep_browser_open = True

    def test_001_navigate_to_my_account_menu_in_the_application_compare_the_display_order_of_the_items_available_in_the_my_account_menu_with_the_display_order_configured_in_cms_verify(self):
        """
        DESCRIPTION: Navigate to My Account menu in the application. Compare the display order of the items available in the My Account menu with the display order configured in CMS. Verify.
        EXPECTED: The display order of the items displayed in the My Account menu is according to the order configured in CMS.
        """
        pass

    def test_002_change_the_display_order_of_the_items_in_cms_ie_change_the_order_for_view_balances_and_place_it_above_deposit_and_save_the_changes_in_cms_verify_in_the_my_account_menu_in_the_application(self):
        """
        DESCRIPTION: Change the display order of the items in CMS, i.e. change the order for View Balances and place it above Deposit and save the changes in CMS. Verify in the My Account menu in the application.
        EXPECTED: The display order of the items displayed in the My Account menu is according to the updated display order configured in CMS, i.e. View Balances is displayed above Deposit.
        """
        pass
