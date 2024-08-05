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
class Test_C869415_Breadcrumbs_functionality_for_general_pages(Common):
    """
    TR_ID: C869415
    NAME: Breadcrumbs functionality for general pages
    DESCRIPTION: This test case verifies Breadcrumbs functionality for general pages for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Oxygen app is loaded
    """
    keep_browser_open = True

    def test_001_navigate_to_promotions_page(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page
        EXPECTED: Promotions page is loaded
        """
        pass

    def test_002_verify_breadcrumbs_displaying_at_the_promotions_page(self):
        """
        DESCRIPTION: Verify Breadcrumbs displaying at the 'Promotions' page
        EXPECTED: * Breadcrumbs are located below the 'Promotions' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the 'Promotions' page: 'Home' > 'Promotions'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_003_click_on_back_button_on_the_promotions_page(self):
        """
        DESCRIPTION: Click on 'Back' button on the 'Promotions' page
        EXPECTED: Previously selected page is opened
        """
        pass

    def test_004_back_to_promotions_page_and_click_on_home_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Back to 'Promotions' page and click on 'Home' hyperlink from the breadcrumbs
        EXPECTED: Homepage is loaded
        """
        pass

    def test_005_navigate_to_player_bets_page_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Navigate to 'Player Bets' page and repeat steps 2-4
        EXPECTED: * Breadcrumbs are located below the 'Player Bets' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the 'Player Bets' page: 'Home' > 'Player Bets'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_006_navigate_to_yourcall_page_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Navigate to 'YourCall' page and repeat steps 2-4
        EXPECTED: * Breadcrumbs are located below the 'YourCall' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the 'YourCall' page: 'Home' > 'YourCall'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_007_navigate_to_virtuals_page_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Navigate to 'Virtuals' page and repeat steps 2-4
        EXPECTED: * Breadcrumbs are located below the 'Virtuals' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Virtuals page: 'Home' > 'Virtuals'
        EXPECTED: * Appropriate item from breadcrumbs is highlighted according to selected page (e.g. Virtuals) and not displayed as hyperlink when hovering on it
        """
        pass

    def test_008_navigate_to_lotto_page_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Navigate to 'Lotto' page and repeat steps 2-4
        EXPECTED: * Breadcrumbs are located below the 'Lotto' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Lotto page: 'Home' > 'Lotto'
        EXPECTED: * Appropriate item from breadcrumbs is highlighted according to selected page (e.g. Lotto) and not displayed as hyperlink when hovering on it
        """
        pass
