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
class Test_C29325_Add_new_Banner(Common):
    """
    TR_ID: C29325
    NAME: Add new Banner
    DESCRIPTION: This test case verifies adding and displaying banners on football widget
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   [BMA-12460 (CMS: Upload the banner images in/to the CMS Tool)][1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-12460
    PRECONDITIONS: User is logged in to CMS:
    PRECONDITIONS: *   dev:
    PRECONDITIONS: *   tst2:
    PRECONDITIONS: NOTE:
    PRECONDITIONS: *   To view football widget within Oxygen application, navigate to Event Details page of live football event with mapped visualizations
    """
    keep_browser_open = True

    def test_001_navigate_to_cms_page_with_banners_for_football_widget(self):
        """
        DESCRIPTION: Navigate to CMS page with banners for Football widget
        EXPECTED: Page with list of banners (if present) is opened
        """
        pass

    def test_002_add_new_banner_via_clicking_on_plus_create_3d_football_banner_button_enter_all_required_data_upload_banner_image_and_save_it(self):
        """
        DESCRIPTION: Add new banner via clicking on  '+ Create 3D Football Banner' button, enter all required data, upload banner image and save it
        EXPECTED: Banner appears in the banners list
        """
        pass

    def test_003_navigate_to_3d_football_widget_within_oxygen_application(self):
        """
        DESCRIPTION: Navigate to 3D football widget within Oxygen application
        EXPECTED: Banner is displayed on football widget alternating with already added before banners
        """
        pass
