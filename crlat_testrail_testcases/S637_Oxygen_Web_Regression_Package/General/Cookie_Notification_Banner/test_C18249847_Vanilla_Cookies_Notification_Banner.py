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
class Test_C18249847_Vanilla_Cookies_Notification_Banner(Common):
    """
    TR_ID: C18249847
    NAME: [Vanilla] Cookies Notification Banner
    DESCRIPTION: Cookie banner is managed by GVC marketing team.
    PRECONDITIONS: Browser/device with no Coral related Cookies.
    """
    keep_browser_open = True

    def test_001_open_the_application(self):
        """
        DESCRIPTION: Open the application.
        EXPECTED: Cookies banner is displayed.
        """
        pass

    def test_002_verify_cookies_banner_content(self):
        """
        DESCRIPTION: Verify cookies banner content.
        EXPECTED: - "We use cookies to provide you with a great user experience. By using Coral, you agree to our use of cookies." text
        EXPECTED: - "cookies" word is also a link to coral cookies policy
        EXPECTED: - Green 'OK' button
        """
        pass

    def test_003_click_ok_button(self):
        """
        DESCRIPTION: Click 'OK' button.
        EXPECTED: Cookies banner is closed.
        """
        pass

    def test_004_open_the_application_in_the_same_browser_again(self):
        """
        DESCRIPTION: Open the application in the same browser again.
        EXPECTED: Cookies banner is not displayed.
        """
        pass
