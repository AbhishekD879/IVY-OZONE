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
class Test_C60911184_Verify_the_CMS_configurations_for_Ticket_Management(Common):
    """
    TR_ID: C60911184
    NAME: Verify the CMS configurations for Ticket Management
    DESCRIPTION: This test case verifies the CMS configurations for Ticket Management
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_click_on_5_a_side_showdown_tab(self):
        """
        DESCRIPTION: Click on '5-A Side showdown' tab
        EXPECTED: Ticket Management should be displayed as a section
        """
        pass

    def test_003_click_on_ticket_management(self):
        """
        DESCRIPTION: Click on Ticket Management
        EXPECTED: * Toggle to switch the Ticket Widget ON/OFF
        EXPECTED: * 'Red Tickets' field should be displayed as free text
        EXPECTED: * 'Gold Tickets' field should be displayed as free text
        EXPECTED: * User should be able to enter multiple OB token IDs (comma separated list) in each field
        EXPECTED: * User should be able to enter free text for 'Ticket Summary Text'
        EXPECTED: * User should be able to enter free text for 'No Tickets Summary'
        """
        pass
