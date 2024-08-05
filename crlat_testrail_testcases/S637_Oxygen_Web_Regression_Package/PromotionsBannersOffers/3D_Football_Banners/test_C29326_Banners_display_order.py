import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29326_Banners_display_order(Common):
    """
    TR_ID: C29326
    NAME: Banners display order
    DESCRIPTION: This test case verifies that Banners are displayed in the same order as they set in CMS
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   [BMA-12460 (CMS: Upload the banner images in/to the CMS Tool)][1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-12460
    PRECONDITIONS: User is logged in to CMS:
    PRECONDITIONS: *    dev:
    PRECONDITIONS: *    tst2:
    PRECONDITIONS: More than one banner is already added
    PRECONDITIONS: NOTE:
    PRECONDITIONS: *   To view football widget within Oxygen application, navigate to Event Details page of live football event with mapped visualizations
    """
    keep_browser_open = True

    def test_001_navigate_to_cms_page_with_banners_for_football_widget(self):
        """
        DESCRIPTION: Navigate to CMS page with banners for Football widget
        EXPECTED: Page with list of banners is opened
        """
        pass

    def test_002_note_the_order_of_added_banners_in_the_list(self):
        """
        DESCRIPTION: Note the order of added banners in the list
        EXPECTED: 
        """
        pass

    def test_003_navigate_to_3d_football_widget_within_oxygen_application_and_verify_banners_display_order(self):
        """
        DESCRIPTION: Navigate to 3D football widget within Oxygen application and verify banners display order
        EXPECTED: Banners are displayed according to their order in CMS
        """
        pass

    def test_004_dragdrop_banners_in_cms_to_change_their_order_and_verify_banners_display_order_on_football_widget(self):
        """
        DESCRIPTION: Drag&Drop banners in CMS to change their order and verify banners display order on football widget
        EXPECTED: Banners are displayed according to new order set in CMS
        """
        pass
