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
class Test_C874391_Lottery_Main_Page(Common):
    """
    TR_ID: C874391
    NAME: Lottery Main Page
    DESCRIPTION: This Test Case verifies Lottery Main Page.
    DESCRIPTION: Note: 'More Market's expandible/collapsible section is not implemented functionality
    PRECONDITIONS: 1. Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    PRECONDITIONS: 2. Launch Oxygen application
    """
    keep_browser_open = True

    def test_001_tap_lotto_icon_from_sportsmenu_ribbonor_a_z_page_or_header_menu_for_desktop(self):
        """
        DESCRIPTION: Tap 'Lotto' icon (from Sports Menu Ribbon or A-Z page or Header menu for desktop)
        EXPECTED: 'Lotto' page is opened with following elements:
        EXPECTED: *   'Lotto' header
        EXPECTED: *   Back button
        EXPECTED: *   Banner section
        EXPECTED: *   Lottery Selector carousel
        EXPECTED: *   Lottery title
        EXPECTED: *   'Lucky' buttons
        EXPECTED: *   Number Selector module
        EXPECTED: *   The Bonus Ball toggle (if available)
        EXPECTED: *   'Options' expandible/collapsible section
        EXPECTED: *   'Place Bet' button is shown by default
        EXPECTED: **For Desktop:**
        EXPECTED: * Breadcrumbs are displayed below 'Lotto' header
        EXPECTED: * Breadcrumbs are displayed in the following format : 'Home' > 'Lotto'
        """
        pass

    def test_002_verify_lottery_selector_carousel(self):
        """
        DESCRIPTION: Verify Lottery Selector Carousel
        EXPECTED: Each Lottery in the Carousel has it's own icon and title
        """
        pass

    def test_003_verify_lottery_name(self):
        """
        DESCRIPTION: Verify Lottery name
        EXPECTED: Lottery name corresponds to "**description**" attribute on the lottery level
        """
        pass

    def test_004_tap_any_lottery_icon(self):
        """
        DESCRIPTION: Tap any Lottery icon
        EXPECTED: *   Each Lottery has a title in between the lottery selector and Numbers Selector Module
        EXPECTED: *   The title shows the name of the Lottery and time left for the next draw
        """
        pass

    def test_005_verify_default_state_of_numbers_selector_module(self):
        """
        DESCRIPTION: Verify default state of Numbers Selector Module
        EXPECTED: *   Numbers Selector Module is placed under Lottery Title
        EXPECTED: *   Numbers Selector Module consists of **5** wheels which hold the numbers
        EXPECTED: *   **"-" **is displayed in each of the Wheels by default (although further user selection is saved in local storage)
        EXPECTED: *   The range of the Numbers available in each Wheel is 1 to the Max number of the Lottery e.g. 49 (The max number depends on the Lottery selected)
        """
        pass

    def test_006_set_up_5_different_numbers_within_wheels(self):
        """
        DESCRIPTION: Set up 5 different numbers within Wheels
        EXPECTED: Numbers are set up correctly
        """
        pass
