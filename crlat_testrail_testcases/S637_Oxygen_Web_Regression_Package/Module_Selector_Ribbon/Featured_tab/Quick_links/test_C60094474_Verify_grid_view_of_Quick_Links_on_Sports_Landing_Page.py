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
class Test_C60094474_Verify_grid_view_of_Quick_Links_on_Sports_Landing_Page(Common):
    """
    TR_ID: C60094474
    NAME: Verify grid view of Quick Links on Sports Landing Page
    DESCRIPTION: This test case verifies grid view of Quick links to Sports Landing Page
    DESCRIPTION: **VALID AFTER BMA-57288**
    PRECONDITIONS: 1) There should be **2** active Quick links for any Sport Landing Page in CMS
    PRECONDITIONS: 2) Go to Oxygen app and navigate to Homepage.
    PRECONDITIONS: **After BMA-57288** QL designs will be using grid layout:
    PRECONDITIONS: https://app.zeplin.io/project/5d35b6cdddc2c6b23c97d022?seid=5f6b29fe592de41478c4667b
    PRECONDITIONS: https://app.zeplin.io/project/5b2bb55ca6aa69a10d44e4e9/dashboard?seid=5e5d0dd9898f0b6861bce496
    """
    keep_browser_open = True

    def test_001__go_to_oxygen_application_and_navigate_to_sport_landing_page_with_configured_quick_links_from_preconditions_verify_that_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: * Go to Oxygen application and navigate to Sport Landing page with configured Quick Links from Preconditions
        DESCRIPTION: * Verify that configured Quick links are displayed.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick links are displayed on Featured tab on Homepage.
        EXPECTED: * Quick links are shown in grid (in the same line, divided in half)
        EXPECTED: ![](index.php?/attachments/get/122312550)
        """
        pass

    def test_002__configure_one_more_active_quick_link_in_cms_to_have_3_active_links_verify_that_configured_quick_links_are_displayed_on_sport_landing_page(self):
        """
        DESCRIPTION: * Configure one more active quick link in CMS (to have 3 active links)
        DESCRIPTION: * Verify that configured Quick links are displayed on Sport Landing page
        EXPECTED: If there are odd number of Quick Links (1,3,5 etc.) in Grid view:
        EXPECTED: * First Quick link is stretched to fit the width of the screen
        EXPECTED: * Other Quick links are displayed in grid view
        EXPECTED: ![](index.php?/attachments/get/122312551)
        """
        pass

    def test_003__configure_more_active_quick_link_in_cms_to_have_even_number_of_active_links_eg_468_etc_verify_that_configured_quick_links_are_displayed_on_sport_landing_page(self):
        """
        DESCRIPTION: * Configure more active quick link in CMS to have even number of active links (e.g 4,6,8 etc.)
        DESCRIPTION: * Verify that configured Quick links are displayed on Sport Landing page
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick links are displayed on Sport Landing page
        EXPECTED: * Quick links are shown in grid (2 links in the same line, divided in halves)
        EXPECTED: ![](index.php?/attachments/get/122312552)
        """
        pass

    def test_004__remove_all_active_quick_links_except_one_in_cms_to_have_1_active_quick_link_verify_that_configured_quick_link_is_displayed_on_sport_landing_page(self):
        """
        DESCRIPTION: * Remove all active quick links except one in CMS to have **1** active quick link
        DESCRIPTION: * Verify that configured Quick link is displayed on Sport Landing page
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Quick link is stretched to fit the width of the screen
        EXPECTED: ![](index.php?/attachments/get/122312554)
        """
        pass
