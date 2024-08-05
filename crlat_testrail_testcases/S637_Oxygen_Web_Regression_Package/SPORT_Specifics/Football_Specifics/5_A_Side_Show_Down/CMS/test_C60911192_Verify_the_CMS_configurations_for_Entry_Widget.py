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
class Test_C60911192_Verify_the_CMS_configurations_for_Entry_Widget(Common):
    """
    TR_ID: C60911192
    NAME: Verify the CMS configurations for Entry Widget
    DESCRIPTION: This test case verifies the CMS configurations for Entry Widget
    PRECONDITIONS: 1: User should have admin access to CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin User
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_home_page_section_of_cms(self):
        """
        DESCRIPTION: Navigate to Home page section of CMS
        EXPECTED: User should be able to view Module Order tab
        """
        pass

    def test_003_click_on_module_order_tab(self):
        """
        DESCRIPTION: Click on Module Order tab
        EXPECTED: * User should be able to view new component **Showdown Widget**
        EXPECTED: * User can either enable/disable the module
        """
        pass

    def test_004_click_on_showdown_widget(self):
        """
        DESCRIPTION: Click on **Showdown Widget**
        EXPECTED: * Contest ID - This is the ID of the Showdown Contest
        EXPECTED: * Button Text - This is the text displayed on the button
        EXPECTED: * EDP Position - Defines the position the widget on the All Markets Tab
        EXPECTED: * Sports - Define what sports pages it is shown on
        EXPECTED: * EDP - Configure on /off on EDP All Markets Tab
        EXPECTED: * Scheduling - Ability to schedule the display of the widget
        EXPECTED: * User should have separate toggle ON/OFF for Home page, Football Landing Page(All Matches Tab), EDP page
        """
        pass
