import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732159_Verify_the_accessibility_of_all_links_tabs_and_buttons_after_double_tap(Common):
    """
    TR_ID: C57732159
    NAME: Verify the accessibility of all links, tabs and buttons after double tap
    DESCRIPTION: This test case verifies the accessibility of all links, tabs and buttons after double tap
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 2. The link to Correct 4 is available on the website
    """
    keep_browser_open = True

    def test_001_double_tap_on_the_correct_4_link(self):
        """
        DESCRIPTION: Double-tap on the Correct 4 link
        EXPECTED: Correct 4 is opened
        """
        pass

    def test_002_double_tap_on_each_link_tabs_and_buttons_on_splash_page(self):
        """
        DESCRIPTION: Double-tap on each link, tabs and buttons on Splash Page
        EXPECTED: The User is redirected to the Home page / Football page.
        """
        pass

    def test_003_double_tap_on_each_link_tabs_and_buttons_on__page(self):
        """
        DESCRIPTION: Double-tap on each link, tabs and buttons on  Page
        EXPECTED: The 'This week' tab is opened.
        EXPECTED: The Splash page is opened (only on mobile).
        """
        pass

    def test_004_double_tap_on_each_link_tabs_and_buttons_on_splash_page(self):
        """
        DESCRIPTION: Double-tap on each link, tabs and buttons on Splash Page
        EXPECTED: The 'This week' tab is opened (only on mobile).
        """
        pass

    def test_005_double_tap_on_each_link_tabs_and_buttons_on_splash_page(self):
        """
        DESCRIPTION: Double-tap on each link, tabs and buttons on Splash Page
        EXPECTED: The User is redirected to the Home page / Football page.
        """
        pass
