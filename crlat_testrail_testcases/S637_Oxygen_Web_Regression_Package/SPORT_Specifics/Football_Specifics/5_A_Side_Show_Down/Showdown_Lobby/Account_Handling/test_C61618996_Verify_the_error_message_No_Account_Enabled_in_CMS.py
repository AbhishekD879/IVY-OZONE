import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C61618996_Verify_the_error_message_No_Account_Enabled_in_CMS(Common):
    """
    TR_ID: C61618996
    NAME: Verify the error message_No Account Enabled in CMS
    DESCRIPTION: This Test case verifies the error message displayed when no Account is enabled
    PRECONDITIONS: User should have admin access to CMS
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Item Label: FAQs
    PRECONDITIONS: Path: /five-a-side-showdown/faq
    PRECONDITIONS: Item Label: Terms & Conditions
    PRECONDITIONS: Path: /five-a-side-showdown/terms-and-conditions
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin User
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_5_a_side_show_down_tab_and_click_on_create_contest(self):
        """
        DESCRIPTION: Navigate to 5-A Side show down tab and Click on Create Contest
        EXPECTED: Enter the mandatory fields and click on Save
        """
        pass

    def test_003_scroll_down_and_navigate_to_accounts(self):
        """
        DESCRIPTION: Scroll down and Navigate to Accounts
        EXPECTED: * Real Accounts should be enabled
        """
        pass

    def test_004_disable_the_real_accounts(self):
        """
        DESCRIPTION: Disable the Real Accounts
        EXPECTED: User is displayed error message to enable either of the Accounts
        """
        pass
