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
class Test_C32870548_Users_do_not_view_Quick_Links_on_Featured_tab_when_they_are_disabled_not_configured_in_CMS(Common):
    """
    TR_ID: C32870548
    NAME: Users do not view Quick Link(s) on Featured tab when they are disabled/not configured in CMS
    DESCRIPTION: This test case verifies that users do not view Quick Link(s) container on the Featured tab if the Quick Links are disabled OR not configured in CMS
    DESCRIPTION: This test case should be verified for both brands Coral/Ladbrokes on the following platforms:
    DESCRIPTION: * iOS
    PRECONDITIONS: * The Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: * Quick Links are enabled in CMS and configured
    PRECONDITIONS: * Quick Links container is displayed on Featured tab
    """
    keep_browser_open = True

    def test_001__go_to_cms_and_disable_all_quick_links_kill_the_app_and_launch_it_again_verify_the_presence_if_quick_links_container_on_featured_tab(self):
        """
        DESCRIPTION: * Go to CMS and disable all Quick Links
        DESCRIPTION: * Kill the app and launch it again
        DESCRIPTION: * Verify the presence if Quick Links container on Featured tab
        EXPECTED: Quick Links are not displayed on Featured tab
        """
        pass
