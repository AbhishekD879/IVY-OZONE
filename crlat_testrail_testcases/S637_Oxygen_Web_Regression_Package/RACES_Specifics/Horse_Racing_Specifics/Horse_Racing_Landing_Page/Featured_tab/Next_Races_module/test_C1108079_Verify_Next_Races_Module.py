import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C1108079_Verify_Next_Races_Module(Common):
    """
    TR_ID: C1108079
    NAME: Verify 'Next Races' Module
    DESCRIPTION: This test case verifies 'Next Races' module
    PRECONDITIONS: 1. Make sure race events are available for the current day
    PRECONDITIONS: 2. Load Oxygen application
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) In order to control Events displaying in the Next Races Module on the Horse Racing page, go to CMS -> 'System-configuration' -> Structure -> NextRaces
    PRECONDITIONS: 2) To load CMS use the link from 'devlog' function
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        EXPECTED: Horse Racing Landing page is opened by default on 'Featured' tab
        """
        pass

    def test_002_check_next_races_module(self):
        """
        DESCRIPTION: Check 'Next Races' module
        EXPECTED: **For Mobile and Tablet:**
        EXPECTED: 'Next Races' module is displayed below *'Today's enhanced Races'* module (if available)
        EXPECTED: **For Desktop:**
        EXPECTED: Next Races module is shown in line with Races Grids in main display area
        """
        pass

    def test_003_check_horizontal_scrollingnavigation_arrows_through_events(self):
        """
        DESCRIPTION: Check Horizontal scrolling/Navigation arrows through events
        EXPECTED: **For Mobile and Tablet:**
        EXPECTED: * It is possible to move between events using swiping on Mobile/Tablet
        EXPECTED: * Swiping is fulfilled fluently
        EXPECTED: * The previous race is not shown when user swipes across the 'Next Races' module
        EXPECTED: * The next race is shown when user swipes across the 'Next Races' module
        EXPECTED: **For Desktop:**
        EXPECTED: * Clickable Navigation right arrow which appear on hover is displayed when content is more than one slide
        EXPECTED: * Clickable Navigation left arrow (content on both sides) which appear on hover is displayed when viewing slide 2 or more
        EXPECTED: * User can click both arrows to move content left and right
        """
        pass

    def test_004_verify_event_section(self):
        """
        DESCRIPTION: Verify event section
        EXPECTED: * Default number of selections is 3. (*It is a CMS controlled value)*
        EXPECTED: * If number of selections is less than 3 -> display the remaining selections
        """
        pass

    def test_005_verify_more_link(self):
        """
        DESCRIPTION: Verify 'More' link
        EXPECTED: Link is shown at right corner of the card and links to EDP of respective event.
        """
        pass

    def test_006_go_to_the_antepost_tab_and_verify_next_races_module(self):
        """
        DESCRIPTION: Go to the 'Antepost' tab and Verify 'Next Races' module
        EXPECTED: 'Next Races' module is absent.
        """
        pass

    def test_007_repeat_step_6_for_specials_yourcall_tab(self):
        """
        DESCRIPTION: Repeat step #6 for 'Specials', 'YourCall' tab
        EXPECTED: 'Next Races' module is absent
        """
        pass

    def test_008_for_desktopnavigate_to_the_homepage__next_races_section(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to the homepage > 'Next Races' section
        EXPECTED: **For Desktop:**
        EXPECTED: The link is shown under the module on the bottom right side and it redirected the user to the 'Horse Racing' Landing page
        """
        pass

    def test_009_repeat_steps__4_7(self):
        """
        DESCRIPTION: Repeat steps # 4-7
        EXPECTED: All validations pass the same
        """
        pass
