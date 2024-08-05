import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C62912734_Verify_the_CMS_configurations_for_pop_up_message_Find_Out_More_Link(Common):
    """
    TR_ID: C62912734
    NAME: Verify the CMS configurations for pop-up message_Find Out More Link
    DESCRIPTION: This test case verifies the CMS configurations for message pop-up
    PRECONDITIONS: * User should have admin access to CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin User
        EXPECTED: User should be logged in to CMS
        """
        pass

    def test_002_navigate_to_cms_gt_static_blocks(self):
        """
        DESCRIPTION: Navigate to CMS &gt; Static Blocks
        EXPECTED: * Configure the message pop-up and Save the changes
        """
        pass
