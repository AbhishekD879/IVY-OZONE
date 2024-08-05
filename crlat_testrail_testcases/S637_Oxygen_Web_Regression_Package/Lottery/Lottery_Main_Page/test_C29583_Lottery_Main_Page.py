import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.lotto
@vtest
class Test_C29583_Lottery_Main_Page(Common):
    """
    TR_ID: C29583
    NAME: Lottery Main Page
    DESCRIPTION: This Test Case virifies Lottery Main Page elements.
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-2307 - Lottery Main page and navigation
    DESCRIPTION: BMA-8873 - Lotto - design changes
    DESCRIPTION: AUTOTEST [C9690246]
    PRECONDITIONS: 1. Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    PRECONDITIONS: 2. Launch application
    """
    keep_browser_open = True

    def test_001_navigate_to_lotto_page(self):
        """
        DESCRIPTION: Navigate to 'Lotto' page
        EXPECTED: 'Lotto' page is opened with following elements:
        EXPECTED: *   'Lotto' header
        EXPECTED: *   Back button
        EXPECTED: *   Breadcrumbs trail (Home > Lotto) (Desktop only) under 'LOTTO' header
        EXPECTED: *   Banner section
        EXPECTED: *   Lottery Selector carousel
        EXPECTED: *   Lottery title and help icon
        EXPECTED: *   'Reset Numbers' button
        EXPECTED: *   Selected Numbers line
        EXPECTED: *   'Lucky' buttons
        EXPECTED: *   'Include Bonus Ball?' checkbox
        EXPECTED: *   Odds
        EXPECTED: *   Field for bet value entering
        EXPECTED: *   'Options' expandable/collapsible section
        EXPECTED: *   'Draw' checkboxes
        EXPECTED: *   'Place Bet' button is shown by default
        """
        pass

    def test_002_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: 'Back' button takes user to the previous page he/she navigated from
        """
        pass

    def test_003_verify_main_applications_header_and_footer_presense(self):
        """
        DESCRIPTION: Verify main application's header and footer presense
        EXPECTED: Main application's header and footer are present on the page
        """
        pass
