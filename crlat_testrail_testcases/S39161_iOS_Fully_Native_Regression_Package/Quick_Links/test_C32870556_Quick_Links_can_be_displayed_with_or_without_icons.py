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
class Test_C32870556_Quick_Links_can_be_displayed_with_or_without_icons(Common):
    """
    TR_ID: C32870556
    NAME: Quick Links can be displayed with or without icons
    DESCRIPTION: This test case verifies that users can view Quick Link(s) WITH or WITHOUT icons on the Featured tab depending on the Quick Links configuration in CMS
    DESCRIPTION: This test case should be verified for both brands Coral/Ladbrokes on the following platforms:
    DESCRIPTION: * iOS
    PRECONDITIONS: * The Coral/Ladbrokes app is installed
    PRECONDITIONS: * Quick Links are enabled in CMS
    PRECONDITIONS: * Some Quick Links are configured to be displayed WITH icons (icons have been uploaded during the configuration)
    PRECONDITIONS: * Some Quick Links are configured to be displayed WITHOUT icons (icons haven't been uploaded during the configuration)
    """
    keep_browser_open = True

    def test_001__launch_the_app_verify_the_quick_links_container_on_featured_tab(self):
        """
        DESCRIPTION: * Launch the app
        DESCRIPTION: * Verify the Quick Links container on Featured tab
        EXPECTED: * Icons are displayed in the Quick Links that have been configured with icons in CMS
        EXPECTED: * Icons are not displayed in the Quick Links that haven't been configured with icons in CMS
        EXPECTED: * Quick Links with and without icons are displayed as per design below (the first QL without icon, the second QL with icon):
        EXPECTED: ![](index.php?/attachments/get/10014138)
        """
        pass
