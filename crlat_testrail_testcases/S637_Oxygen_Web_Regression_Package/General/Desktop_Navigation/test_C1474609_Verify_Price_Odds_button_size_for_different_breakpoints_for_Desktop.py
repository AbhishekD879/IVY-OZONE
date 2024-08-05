import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C1474609_Verify_Price_Odds_button_size_for_different_breakpoints_for_Desktop(Common):
    """
    TR_ID: C1474609
    NAME: Verify 'Price/Odds' button size for different breakpoints for Desktop
    DESCRIPTION: This test case verifies 'Price/Odds' button size for different breakpoints.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Oxygen app is loaded
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: 'Price/Odds' buttons for all Races, Enhanced Multiples cards in the carousel, Specials/Enhanced offers in 'Featured' section, 'In-Play'/'Live Stream' and 'Favorites' widgets are not changed when resizing the page. Sizes for 'Price/Odds' buttons are static.
    """
    keep_browser_open = True

    def test_001_navigate_to_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sports> Landing page
        EXPECTED: * <Sports> Landing page is opened
        EXPECTED: * 'Today' tab is selected by default
        EXPECTED: * List of available events is displayed
        """
        pass

    def test_002_resize_page_from_1600px_to_1920px_width_and_verify_dimensions_of_priceodds_button(self):
        """
        DESCRIPTION: Resize page from 1600px to 1920px width and verify dimensions of 'Price/Odds' button
        EXPECTED: 'Price/Odds' button has 110x40px size
        """
        pass

    def test_003_resize_page_from_970px_to_1599px_width_and_verify_dimensions_of_priceodds_button(self):
        """
        DESCRIPTION: Resize page from 970px to 1599px width and verify dimensions of 'Price/Odds' button
        EXPECTED: 'Price/Odds' button has 50x40px size
        """
        pass

    def test_004_resize_page_to_less_than_970px_width_and_verify_dimensions_of_priceodds_button(self):
        """
        DESCRIPTION: Resize page to less than 970px width and verify dimensions of 'Price/Odds' button
        EXPECTED: 'Price/Odds' button has 50x40px size
        """
        pass

    def test_005_navigate_to_sports_event_details_page(self):
        """
        DESCRIPTION: Navigate to <Sports> Event Details page
        EXPECTED: * <Sports> Event Details page is opened
        EXPECTED: * List of available markets is displayed
        """
        pass

    def test_006_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps 2-4
        EXPECTED: 
        """
        pass

    def test_007_navigate_to_sports_competition_outrights_page_football_only(self):
        """
        DESCRIPTION: Navigate to <Sports> Competition Outrights page (Football only)
        EXPECTED: * <Sports> Competition Outrights page is opened
        EXPECTED: * List of available Outright events/markets is displayed
        """
        pass

    def test_008_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps 2-4
        EXPECTED: 
        """
        pass

    def test_009_navigate_to_sports_coupons_page(self):
        """
        DESCRIPTION: Navigate to <Sports> Coupons page
        EXPECTED: * <Sports> Coupons page is opened
        EXPECTED: * List of available events is displayed
        """
        pass

    def test_010_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps 2-4
        EXPECTED: 
        """
        pass

    def test_011_navigate_to_sports_jackpot_page_football_only(self):
        """
        DESCRIPTION: Navigate to <Sports> Jackpot page (Football only)
        EXPECTED: <Sports> Jackpot page is opened
        """
        pass

    def test_012_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps 2-4
        EXPECTED: 
        """
        pass

    def test_013_navigate_to_featured_section_on_the_homepage(self):
        """
        DESCRIPTION: Navigate to 'Featured' section on the Homepage
        EXPECTED: * Homepage is loaded
        EXPECTED: * 'Featured' section is present with the set of created modules by Type ID, Enhanced Multiples ID, etc.
        """
        pass

    def test_014_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps 2-4
        EXPECTED: 
        """
        pass
