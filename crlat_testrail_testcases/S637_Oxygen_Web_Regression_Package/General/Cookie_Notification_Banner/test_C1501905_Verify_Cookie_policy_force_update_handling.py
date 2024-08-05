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
class Test_C1501905_Verify_Cookie_policy_force_update_handling(Common):
    """
    TR_ID: C1501905
    NAME: Verify Cookie policy force update handling
    DESCRIPTION: This test case verifies the handling of Cookie policy banner force update.
    PRECONDITIONS: 1.All cookies and cache are cleared
    PRECONDITIONS: 2.User is logged out
    PRECONDITIONS: **CMS configuration for version numbering of cookie banner**:
    PRECONDITIONS: In System-configuration > Cookie > cookieBannerVersion : must be integer values > 0 .
    PRECONDITIONS: Banner is re-displayed only for version increase (decreasing the value won't re-display the banner)
    PRECONDITIONS: Make sure that Cookie Banner **is NOT DISPLAYED** on Coral iOS wrapper v.5.1.1 build 1157 and higher regardless of the CMS configuration.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        EXPECTED: Cookies Notification Banner is displayed above the Header at the top of the page as per config in respective static block in CMS
        """
        pass

    def test_002_open_dev_tool__network__all_and_check_request_httpsinvictuscoralcoukapibmainitial_datamobile_or_httpsinvictuscoralcoukapibmasystem_configuration_tabletdesktop(self):
        """
        DESCRIPTION: Open Dev tool > Network > All and check request https://invictus.coral.co.uk/api/bma/initial-data/mobile or https://invictus.coral.co.uk/api/bma/system-configuration (tablet/desktop)
        EXPECTED: In Response Preview: systemConfiguration > Cookie >cookieBannerVersion is an integer value
        """
        pass

    def test_003_click__tap_accept_button_on_cookies_notification_banner(self):
        """
        DESCRIPTION: Click / tap 'Accept' button on Cookies Notification Banner
        EXPECTED: Cookies Notification Banner is closed and no more displayed
        """
        pass

    def test_004_in_cms_increase_the_version_number_in_system_configuration_to_the_next_number_up_from_what_is_currently_and_save(self):
        """
        DESCRIPTION: In CMS, increase the version number in system configuration to the next number up from what is currently and save
        EXPECTED: Value is updated in CMS
        """
        pass

    def test_005_refresh_the_app(self):
        """
        DESCRIPTION: Refresh the app
        EXPECTED: Homepage is opened
        EXPECTED: Cookies Notification Banner is displayed again above the Header at the top of the page as per config in respective static block in CMS
        """
        pass

    def test_006_open_dev_tool__network__all_and_check_request_httpsinvictuscoralcoukapibmainitial_datamobile_or_httpsinvictuscoralcoukapibmasystem_configuration_tabletdesktop(self):
        """
        DESCRIPTION: Open Dev tool > Network > All and check request https://invictus.coral.co.uk/api/bma/initial-data/mobile or https://invictus.coral.co.uk/api/bma/system-configuration (tablet/desktop)
        EXPECTED: In Response Preview: systemConfiguration > Cookie >cookieBannerVersion is reflecting the increased value number at Step 4.
        """
        pass

    def test_007_click__tap_accept_button_on_cookies_notification_banner(self):
        """
        DESCRIPTION: Click / tap 'Accept' button on Cookies Notification Banner
        EXPECTED: Cookies Notification Banner is closed and no more displayed
        """
        pass

    def test_008_in_cms_decrease_the_version_number_in_system_configuration_to_the_next_number_down_from_what_is_currently_and_save(self):
        """
        DESCRIPTION: In CMS, decrease the version number in system configuration to the next number down from what is currently and save
        EXPECTED: Value is updated in CMS
        """
        pass

    def test_009_refresh_the_app(self):
        """
        DESCRIPTION: Refresh the app
        EXPECTED: Homepage is opened
        EXPECTED: Cookies Notification Banner is NOT displayed at the top of the page
        """
        pass

    def test_010_open_dev_tool__network__all_and_check_request_httpsinvictuscoralcoukapibmainitial_datamobile_or_httpsinvictuscoralcoukapibmasystem_configuration_tabletdesktop(self):
        """
        DESCRIPTION: Open Dev tool > Network > All and check request https://invictus.coral.co.uk/api/bma/initial-data/mobile or https://invictus.coral.co.uk/api/bma/system-configuration (tablet/desktop)
        EXPECTED: In Response Preview: systemConfiguration > Cookie >cookieBannerVersion is reflecting the decreased value number at Step 8.
        """
        pass

    def test_011_clear_cache_log_in_and_repeat_steps_steps__1_10(self):
        """
        DESCRIPTION: Clear cache, Log in and repeat steps steps # 1-10
        EXPECTED: --
        """
        pass
