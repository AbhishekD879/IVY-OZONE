import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C46541_Verify_Cookies_Notification_Banner_GDPR_is_OFF(Common):
    """
    TR_ID: C46541
    NAME: Verify Cookies Notification Banner (GDPR is OFF)
    DESCRIPTION: This test case verifies Cookies Notification Banner displaying
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-14778 Cookie Notifications On All Platforms
    DESCRIPTION: BMA-46701 Coral IOS app - please remove the cookie banner
    PRECONDITIONS: 1. All cookies and cache are cleared
    PRECONDITIONS: 2. Make sure that Cookie Banner **is NOT DISPLAYED** on Coral iOS wrapper v.5.1.1 build 1157 and higher regardless of the CMS configuration.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_verify_cookies_notification_banner_displaying(self):
        """
        DESCRIPTION: Verify Cookies Notification Banner displaying
        EXPECTED: - Cookies Notification Banner is displayed above the Header at the top of the page on Homepage
        EXPECTED: - Cookies Notification Banner is displayed above all elements within app (e.g. Right Menu, Slide-out Betslip, Home and Football tutorial overlays, pop-ups)
        EXPECTED: - Cookies Notification Banner is displayed on every page of application until user accepts terms
        """
        pass

    def test_003_verify_cookies_notification_banner_content(self):
        """
        DESCRIPTION: Verify Cookies Notification Banner content
        EXPECTED: Cookies Notification Banner consists of:
        EXPECTED: - CMS-configured text message with 'cookie policy' hyperlink
        EXPECTED: - 'Accept&close' button
        EXPECTED: - 'More Info' hyperlink
        """
        pass

    def test_004_verify_cookie_policy_hyperlink(self):
        """
        DESCRIPTION: Verify 'cookie policy' hyperlink
        EXPECTED: - User is navigated to https://coral-eng.custhelp.com/app/answers/detail/a_id/2132#cookies web-site after clicking / tapping hyperlink
        EXPECTED: - Hyperlink is opened in new tab
        """
        pass

    def test_005_verify_acceptclose_button(self):
        """
        DESCRIPTION: Verify 'Accept&close' button
        EXPECTED: Cookies Notification Banner is closed and NOT displayed after clicking / tapping 'Accept&close' button
        """
        pass

    def test_006_verify_more_info_hyperlink(self):
        """
        DESCRIPTION: Verify 'More Info' hyperlink
        EXPECTED: - User is navigated to https://coral-eng.custhelp.com/app/answers/detail/a_id/8331 web-site after clicking / tapping hyperlink
        EXPECTED: - Hyperlink is opened in new tab
        """
        pass
