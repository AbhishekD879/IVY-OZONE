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
class Test_C8141260_Back_button_navigation_after_opening_promotion_via_promotion_signposting_pop_up(Common):
    """
    TR_ID: C8141260
    NAME: Back button navigation after opening promotion via promotion signposting pop-up
    DESCRIPTION: This test case verifies back button functionality after opening promotion via promotion signposting pop-up
    PRECONDITIONS: - You should have a promotion with enabled promo signposting
    PRECONDITIONS: - Promotion should have a link with URL to the respective promotion in application
    PRECONDITIONS: - You should have an event with enabled promotion flag on market level
    PRECONDITIONS: - You should be on the event details page that has promotion linked
    """
    keep_browser_open = True

    def test_001___tap_on_promo_icon_and_then_tap_on_a_configured_link__verify_navigation(self):
        """
        DESCRIPTION: - Tap on promo icon and then tap on a configured link
        DESCRIPTION: - Verify navigation
        EXPECTED: User is navigated to the promotion page by the provided URL
        """
        pass

    def test_002___tap_back_button__verify_navigation(self):
        """
        DESCRIPTION: - Tap "Back" button
        DESCRIPTION: - Verify navigation
        EXPECTED: User is navigated to the previous page and promo pop-up is closed
        """
        pass
