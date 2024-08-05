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
class Test_C44870339_Verify_that_all_options_available_in_the_header_and_sub_header_section_in_My_Account_menu_are_according_to_the_configuration_in_CMS(Common):
    """
    TR_ID: C44870339
    NAME: Verify that all options available in the header and sub header section in My Account menu are according to the configuration in CMS.
    DESCRIPTION: 
    PRECONDITIONS: User is logged in the application and in CMS.
    """
    keep_browser_open = True

    def test_001_navigate_to_my_account_menu_in_the_application_compare_the_options_available_in_the_my_account_menu_with_those_configured_in_cms_verify(self):
        """
        DESCRIPTION: Navigate to My Account menu in the application. Compare the options available in the My Account menu with those configured in CMS. Verify.
        EXPECTED: The options displayed in the My Account menu are according to the items configured in CMS.
        """
        pass

    def test_002_compare_the_items_available_in_the_sub_header_section_in_my_account_menu_with_those_configured_in_cms_verify(self):
        """
        DESCRIPTION: Compare the items available in the sub header section in My Account menu with those configured in CMS. Verify.
        EXPECTED: The items displayed in the sub header section in My Account menu are according to the items configured in CMS.
        """
        pass
