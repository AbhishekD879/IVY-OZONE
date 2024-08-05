import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C1143946_Navigation_Tennis(Common):
    """
    TR_ID: C1143946
    NAME: Navigation Tennis
    DESCRIPTION: This test case verifies navigation across Tennis Landing and Details page
    DESCRIPTION: if 'Coupons' Tab is not available see instruction how to generate [Coupon](https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system)
    PRECONDITIONS: Open Oxygen app
    """
    keep_browser_open = True

    def test_001_tapclick_on_tennis_button_from_the_main_menu(self):
        """
        DESCRIPTION: Tap/Click on Tennis button from the Main Menu
        EXPECTED: 1. Tennis Page is loaded
        EXPECTED: 2. The 'Matches' tab is selected by default
        EXPECTED: 3. The first 3 Leagues are expanded by default, and the rest of them are collapsed
        EXPECTED: 4. All events which are available are displayed for the League
        EXPECTED: 5. **For Mobile/Tablet:**
        EXPECTED: Enhanced Multiple events section(if available) is displayed on the top of the list and is expanded
        EXPECTED: **For Desktop:**
        EXPECTED: Enhanced Multiple events section (if available) is displayed as carousel above tabs
        EXPECTED: 6. **For Desktop:**
        EXPECTED: 'In-Play' widget is displayed in 3rd column or below main content (depends on screen resolution) with live events in carousel
        """
        pass

    def test_002_tapclick_on_coupons_tab(self):
        """
        DESCRIPTION: Tap/Click on 'Coupons' tab
        EXPECTED: 1. The 'Coupons' tab is loaded
        EXPECTED: 2. Sections with events are displayed on the page and are all collapsed by default
        EXPECTED: 3. It is possible to collapse/expand all of the sections by clicking the header
        EXPECTED: 4. The first 5 events load within 1 second after clicking on the section and incrementally render more events when user scrolls down
        EXPECTED: 5. **For Desktop:**
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content
        """
        pass

    def test_003_select_one_event_from_the_section(self):
        """
        DESCRIPTION: Select one event from the section
        EXPECTED: The event details page is opened
        """
        pass

    def test_004_tapclick_on_back_button_and_then_tapclick_on_outrights_tab(self):
        """
        DESCRIPTION: Tap/Click on 'Back' button and then tap/click on 'Outrights' tab
        EXPECTED: 1. The 'Outrights' tab is loaded
        EXPECTED: 2. Leagues and Competitions are all collapsed by default
        EXPECTED: 3. **For Desktop:**
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content
        """
        pass

    def test_005_expand_one_event_type(self):
        """
        DESCRIPTION: Expand one event type
        EXPECTED: The list of outrights from that event type is displayed
        """
        pass

    def test_006_tapclick_on_in_play_tab(self):
        """
        DESCRIPTION: Tap/Click on 'In-Play' tab
        EXPECTED: 1. The 'In-Play' tab is loaded with the 'Live Now'/'Upcoming' sections
        EXPECTED: 2. The first N leagues are expanded by default (the rest of them are collapsed), N - CMS configurable value
        EXPECTED: 3. **For Desktop:**
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content
        """
        pass
