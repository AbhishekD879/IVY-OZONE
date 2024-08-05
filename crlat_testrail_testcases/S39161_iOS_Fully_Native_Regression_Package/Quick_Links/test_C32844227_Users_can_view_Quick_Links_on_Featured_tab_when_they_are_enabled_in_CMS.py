import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C32844227_Users_can_view_Quick_Links_on_Featured_tab_when_they_are_enabled_in_CMS(Common):
    """
    TR_ID: C32844227
    NAME: Users can view Quick Link(s) on Featured tab when they are enabled in CMS
    DESCRIPTION: This test case verifies that users can view Quick Link(s) container on the Featured tab if the Quick Links are enabled in CMS
    DESCRIPTION: This test case should be verified for both brands Coral/Ladbrokes on the following platforms:
    DESCRIPTION: * iOS
    PRECONDITIONS: * The Coral/Ladbrokes app is installed
    PRECONDITIONS: * Quick Links are enabled in CMS and configured
    """
    keep_browser_open = True

    def test_001__launch_the_app_verify_the_presence_of_quick_links_container_on_featured_tab(self):
        """
        DESCRIPTION: * Launch the app
        DESCRIPTION: * Verify the presence of Quick Links container on Featured tab
        EXPECTED: * Featured tab is displayed
        EXPECTED: * Quick Links are displayed on Featured tab in the same order they are configured in CMS
        EXPECTED: * The number of Quick Links displayed on Featured tab is equal to the number of Quick Links configured in CMS
        EXPECTED: * Quick Links are displayed as per design below:
        EXPECTED: ![](index.php?/attachments/get/9988296)
        """
        pass

    def test_002__configure_and_enable_only_one_quick_link_in_cms_verify_the_appearance_of_quick_link_on_featured_tab(self):
        """
        DESCRIPTION: * Configure and enable only one Quick Link in CMS
        DESCRIPTION: * Verify the appearance of Quick link on Featured tab
        EXPECTED: * Only one Quick Link is displayed on Featured tab
        EXPECTED: * Quick Link is displayed as per design below:
        EXPECTED: ![](index.php?/attachments/get/10014124)
        """
        pass

    def test_003__delete_all_quick_link_in_cms_and_restart_the_app(self):
        """
        DESCRIPTION: * Delete all Quick Link in CMS and restart the app
        EXPECTED: Section disappear
        """
        pass
