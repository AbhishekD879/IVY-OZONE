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
class Test_C29372_CMS_Featured_Tab_Module_displaying_on_mobile_tablet_and_desktop(Common):
    """
    TR_ID: C29372
    NAME: CMS: Featured Tab Module displaying on mobile, tablet and desktop
    DESCRIPTION: This test case verifies displaying of Featured Tab Modules within mobile, tablet and desktop
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-8791 New Publish Channels for Featured Tab Module
    PRECONDITIONS: 1) There are modules for different publishing periods created in CMS (future, present and past) and modules for present time which are disabled from being shown on the front-end
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 3) User is on CMS -> 'Featured Tab Modules' page
    """
    keep_browser_open = True

    def test_001_select_a_module_from_active_grid(self):
        """
        DESCRIPTION: Select a module from Active grid
        EXPECTED: 'Featured Tab Module Editor' Page is opened
        """
        pass

    def test_002_verify_publish_to_channels_is_available_with_list_of_channels(self):
        """
        DESCRIPTION: Verify 'Publish to Channels' is available with list of channels
        EXPECTED: Each channel has checkboxes:
        EXPECTED: *   mobile
        EXPECTED: *   tablet
        EXPECTED: *   desktop
        """
        pass

    def test_003_select_all_3_checkboxes(self):
        """
        DESCRIPTION: Select all 3 checkboxes
        EXPECTED: 
        """
        pass

    def test_004_verify_corresponding_module_on_fe___mobile_tablet_desktop(self):
        """
        DESCRIPTION: Verify corresponding module on FE - mobile, tablet, desktop
        EXPECTED: Featured module is displayed on mobile, tablet and desktop devices
        """
        pass

    def test_005_back_in_cms_select_only_mobile_checkbox(self):
        """
        DESCRIPTION: Back in CMS select only "mobile" checkbox
        EXPECTED: 
        """
        pass

    def test_006_verify_corresponding_featured_module_on_fe___mobile_tablet_desktop(self):
        """
        DESCRIPTION: Verify corresponding Featured module on FE - mobile, tablet, desktop
        EXPECTED: Featured module is displayed on mobiles only
        """
        pass

    def test_007_back_in_cms_select_only_tablet_checkbox(self):
        """
        DESCRIPTION: Back in CMS select only "tablet" checkbox
        EXPECTED: 
        """
        pass

    def test_008_verify_corresponding_featured_module_on_fe___mobile_tablet_desktop(self):
        """
        DESCRIPTION: Verify corresponding Featured module on FE - mobile, tablet, desktop
        EXPECTED: Featured module is displayed on tablets only
        """
        pass

    def test_009_back_in_cms_select_only_desktop_checkbox(self):
        """
        DESCRIPTION: Back in CMS select only "desktop" checkbox
        EXPECTED: 
        """
        pass

    def test_010_verify_corresponding_featured_module_on_fe___mobile_tablet_desktop(self):
        """
        DESCRIPTION: Verify corresponding Featured module on FE - mobile, tablet, desktop
        EXPECTED: Featured module is displayed on desktops only
        """
        pass
