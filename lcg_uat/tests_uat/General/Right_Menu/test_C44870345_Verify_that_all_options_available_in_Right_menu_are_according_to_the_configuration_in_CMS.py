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
class Test_C44870345_Verify_that_all_options_available_in_Right_menu_are_according_to_the_configuration_in_CMS(Common):
    """
    TR_ID: C44870345
    NAME: Verify that all options available in Right menu are according to the configuration in CMS.
    DESCRIPTION: 
    PRECONDITIONS: User is logged in the application and in CMS.
    """
    keep_browser_open = True

    def test_001_navigate_to_my_accountright_menu_in_the_application_compare_the_options_available_in_the_right_menu_with_those_configured_in_cms_verify(self):
        """
        DESCRIPTION: Navigate to My Account/Right menu in the application. Compare the options available in the right menu with those configured in CMS. Verify.
        EXPECTED: The options displayed in the right menu are according to the options configured in CMS.
        """
        pass
