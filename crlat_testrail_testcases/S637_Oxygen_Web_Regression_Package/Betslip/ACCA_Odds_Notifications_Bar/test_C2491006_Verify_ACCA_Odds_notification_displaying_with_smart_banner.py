import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2491006_Verify_ACCA_Odds_notification_displaying_with_smart_banner(Common):
    """
    TR_ID: C2491006
    NAME: Verify ACCA Odds notification displaying with smart banner
    DESCRIPTION: This test case verifies ACCA Odds notification displaying with smart banner
    PRECONDITIONS: - Smart banner is configured in CMS (System Configuration > Structure)
    PRECONDITIONS: - Application is loaded & home page is displayed
    PRECONDITIONS: - Cache is cleared in the app
    PRECONDITIONS: - Smart banner is displayed
    """
    keep_browser_open = True

    def test_001_add_at_least_2_selections_from_different_sportraces_with_lp_prices_events_to_the_betslip_(self):
        """
        DESCRIPTION: Add at least 2 selections from different <Sport>/<Races> with LP prices events to the Betslip (
        EXPECTED: - Selections are added to the Betslip
        EXPECTED: - ACCA Odds Notification message appears (yellow bar)
        """
        pass

    def test_002_verify_displaying_of_of_acca_odds_notification_message_together_with_smart_banner(self):
        """
        DESCRIPTION: Verify displaying of of ACCA Odds Notification message together with Smart Banner
        EXPECTED: Smart Banner is displayed above ACCA Odds Notification message
        """
        pass

    def test_003_scroll_the_page_up_and_down(self):
        """
        DESCRIPTION: Scroll the page up and down
        EXPECTED: - ACCA Odds Notification message is sticky
        EXPECTED: - ACCA Odds Notification message remains displayed below smart banner
        """
        pass
