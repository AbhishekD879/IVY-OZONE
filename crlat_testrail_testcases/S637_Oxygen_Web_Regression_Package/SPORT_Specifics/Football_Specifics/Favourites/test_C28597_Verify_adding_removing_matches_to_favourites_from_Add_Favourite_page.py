import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C28597_Verify_adding_removing_matches_to_favourites_from_Add_Favourite_page(Common):
    """
    TR_ID: C28597
    NAME: Verify adding/removing matches to favourites from ‘Add Favourite' page
    DESCRIPTION: This Test Case verified adding/removing matches to favourites from ‘Add Favourite' page
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: BMA-7790 'Add Favourite Match Button to Main ‘Favourite Matches’ Page'
    PRECONDITIONS: **NOTE**:
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   Test case should be validated for Events with the primary market title "Match Results" and "Match Betting"
    PRECONDITIONS: CMS > System cofiguration > Structure > "Favourites" all checkboxes are checked (displayOnMobile/displayOnTablet/displayOnDesktop)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_football_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        EXPECTED: *   'Football' landing page is opened
        EXPECTED: *   ‘Favourite matches’ functionality is included.
        """
        pass

    def test_003_tap_on_the_favourite_match_page_label_mobiletablet(self):
        """
        DESCRIPTION: Tap on the 'Favourite Match' page label (**Mobile/Tablet**)
        EXPECTED: 'Favourite Match' page is opened
        """
        pass

    def test_004_tap_on_the_go_to_matches_button_mobiletablet(self):
        """
        DESCRIPTION: Tap on the 'Go to Matches' button (**Mobile/Tablet**)
        EXPECTED: *   Football Landing page -> 'Matches' tab is opened
        EXPECTED: *   a list of sub-categories is opened
        """
        pass

    def test_005_tap_on_the_favourite_maches_icon_star_icon_belowevent_team_a_v_team_b(self):
        """
        DESCRIPTION: Tap on the 'Favourite Maches' icon (star icon) below  'Event (Team A v Team B)'
        EXPECTED: *   icon becomes bold
        EXPECTED: *   the event is added to the 'Favourite Matches' page
        """
        pass

    def test_006_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass

    def test_007_tap_on_the_favourite_maches_icon_bold_star_icon_below_the_same_event(self):
        """
        DESCRIPTION: Tap on the 'Favourite Maches' icon (bold star icon) below the same Event
        EXPECTED: *   the icon became not filled (not selected)
        EXPECTED: *   the event is removed from the 'Favourite Matches' page
        """
        pass

    def test_008_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        EXPECTED: 
        """
        pass

    def test_009_tap_on_go_to_in_play_matches_button(self):
        """
        DESCRIPTION: Tap on 'Go to In Play Matches' button
        EXPECTED: *   Football Landing page -> 'In-Play' tab is opened
        EXPECTED: *   'Live Now' & 'Upcoming' sorting buttons are present
        """
        pass

    def test_010_for_both_sorting_button_repeat_steps_5_7(self):
        """
        DESCRIPTION: For both sorting button repeat steps 5-7
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_5_7_for_favourites_widget_desktoptablet(self):
        """
        DESCRIPTION: Repeat steps 5-7 for "Favourites" widget (*Desktop/Tablet*)
        EXPECTED: 
        """
        pass
