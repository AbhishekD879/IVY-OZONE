import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C49131478_Verify_formations_carousel_on_5_A_Side_overlay(Common):
    """
    TR_ID: C49131478
    NAME: Verify formations carousel on '5-A-Side' overlay
    DESCRIPTION: This test case verifies formations carousel on '5-A-Side' overlay of 5-A-Side tab
    PRECONDITIONS: **Create different formations (create all existing formations):**
    PRECONDITIONS: 1. Fill all fields in CMS -> BYB -> 5-A-Side -> click 'Add New Formation' button -> 'New 5 A Side Formation' popup
    PRECONDITIONS: 2. Click/Tap 'Save' button
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs and created formations
    PRECONDITIONS: 2. Click on '5-A-Side' tab
    PRECONDITIONS: 3. Click 'Build A Team' button
    PRECONDITIONS: **Configure 5-A-Side feature in CMS:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    """
    keep_browser_open = True

    def test_001_verify_formations_carousel(self):
        """
        DESCRIPTION: Verify formations carousel
        EXPECTED: * All created formations are displayed in formations carousel
        EXPECTED: * Formations ordering is the same as in CMS
        """
        pass

    def test_002_swipe_carousel_to_view_all_list_of_available_formations(self):
        """
        DESCRIPTION: Swipe carousel to view all list of available formations
        EXPECTED: * Formations in the carousel is scrollable
        EXPECTED: * All formations can be viewed fully when swapping the carousel
        """
        pass

    def test_003__change_formations_ordering_in_cms_using_drag_and_drop_functionality_cms___byb___5_a_side_back_to_the_app_and_refresh_the_page_verify_formations_carousel(self):
        """
        DESCRIPTION: * Change formations ordering in CMS using "Drag and Drop" functionality (CMS -> BYB -> 5-A-Side).
        DESCRIPTION: * Back to the app and refresh the page.
        DESCRIPTION: * Verify formations carousel.
        EXPECTED: Formations ordering is changed corresponds to CMS
        """
        pass

    def test_004__delete_one_formation_in_cms_cms___byb___5_a_side_back_to_the_app_and_refresh_the_page_verify_formations_carousel(self):
        """
        DESCRIPTION: * Delete one formation in CMS (CMS -> BYB -> 5-A-Side).
        DESCRIPTION: * Back to the app and refresh the page.
        DESCRIPTION: * Verify formations carousel.
        EXPECTED: Deleted formation is not displayed in formations carousel
        """
        pass

    def test_005__leave_only_one_formation_in_cms_and_delete_all_other_cms___byb___5_a_side_back_to_the_app_and_refresh_the_page_verify_formations_carousel(self):
        """
        DESCRIPTION: * Leave only one formation in CMS and delete all other (CMS -> BYB -> 5-A-Side).
        DESCRIPTION: * Back to the app and refresh the page.
        DESCRIPTION: * Verify formations carousel.
        EXPECTED: * Only one formation is displayed in formations carousel
        EXPECTED: * Formation is left aligned
        EXPECTED: * User can't swipe carousel
        """
        pass

    def test_006__delete_last_formation_in_cms_cms___byb___5_a_side_back_to_the_app_and_refresh_the_page_verify_formations_carousel(self):
        """
        DESCRIPTION: * Delete last formation in CMS (CMS -> BYB -> 5-A-Side).
        DESCRIPTION: * Back to the app and refresh the page.
        DESCRIPTION: * Verify formations carousel.
        EXPECTED: * '5-A-Side' overlay is displayed
        EXPECTED: * Formations carousel is empty
        """
        pass
