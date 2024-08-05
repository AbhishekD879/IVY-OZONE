import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C28407_Verify_Compliance_Footer(Common):
    """
    TR_ID: C28407
    NAME: Verify Compliance Footer
    DESCRIPTION: This test case verifies Compliance Footer
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   BMA-8622 Desktop Footer Redesign
    PRECONDITIONS: To open CMS use link:
    PRECONDITIONS: https://CMS_endpoint/keystone/static-blocks/ Footer Markup Top/Bottom
    PRECONDITIONS: where CMS_endpoint is taken from **devlog**
    PRECONDITIONS: **Postconditions**
    PRECONDITIONS: Make sure all changes in Compliance Footer is reverted back after the testing
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is shown
        """
        pass

    def test_002_verify_presence_of_compliance_footer(self):
        """
        DESCRIPTION: Verify presence of Compliance Footer
        EXPECTED: Compliance Footer is present on every page across the application as a part of Global Footer
        """
        pass

    def test_003_verify_content_of_compliance_footer(self):
        """
        DESCRIPTION: Verify content of Compliance Footer
        EXPECTED: *   Content of Compliance Footer corresponds to the html text set up in CMS->Static Blocks->Footer Markup Top/Bottom
        EXPECTED: *   Hyperlinks and images are clickable and after tapping them user is redirected to the corresponding pages
        """
        pass

    def test_004_verify_compliance_footer_displaying(self):
        """
        DESCRIPTION: Verify Compliance Footer displaying
        EXPECTED: *   Content is displayed stretched and centralized according to screen resolution;
        EXPECTED: *   Responsible gambling icons are on the white background;
        EXPECTED: *   All data is displayed on dark blue (for Coral) or grey (for Ladbrokes) background.
        """
        pass

    def test_005_open_cms_static_blocks_footer_markup(self):
        """
        DESCRIPTION: Open CMS->Static Blocks->Footer Markup
        EXPECTED: Compliance Footer configuration is opened
        """
        pass

    def test_006_make_any_changesconfigurations_and_save_them(self):
        """
        DESCRIPTION: Make any changes/configurations and save them
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_007_go_to_invictus_app_and_verify_changes(self):
        """
        DESCRIPTION: Go to Invictus app and verify changes
        EXPECTED: All changes are displayed correctly
        """
        pass
