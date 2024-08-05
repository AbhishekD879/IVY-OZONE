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
class Test_C29327_Enabled_Disabled_Banners(Common):
    """
    TR_ID: C29327
    NAME: Enabled/Disabled Banners
    DESCRIPTION: This test case verifies Banner setting 'Disabled'
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   [BMA-12460 (CMS: Upload the banner images in/to the CMS Tool)][1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-12460
    PRECONDITIONS: User is logged in to CMS:
    PRECONDITIONS: *   dev:
    PRECONDITIONS: *   tst2:
    PRECONDITIONS: At least one banner is added
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

    def test_002_open_settings_page_for_any_banner_by_clicking_on_its_name_tick_disabled_checkbox_and_save_change(self):
        """
        DESCRIPTION: Open settings page for any banner by clicking on its name, tick 'Disabled' checkbox and save change
        EXPECTED: 
        """
        pass

    def test_003_navigate_to_3d_football_widget_within_oxygen_application_and_verify_displaying_of_previously_changed_banner(self):
        """
        DESCRIPTION: Navigate to 3D football widget within Oxygen application and verify displaying of previously changed banner
        EXPECTED: Banner is not displayed
        """
        pass

    def test_004_navigate_to_settings_page_for_previously_changed_banner_untick_disabled_checkbox_and_save_change(self):
        """
        DESCRIPTION: Navigate to settings page for previously changed banner, untick 'Disabled' checkbox and save change
        EXPECTED: 
        """
        pass

    def test_005_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step #3
        EXPECTED: Banner is displayed
        """
        pass
