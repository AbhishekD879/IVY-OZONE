import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28607_Verify_adding_removing_matches_to_favourites_from_the_Event_details_page(Common):
    """
    TR_ID: C28607
    NAME: Verify adding/removing matches to favourites from the Event details page
    DESCRIPTION: This Test Case verified adding/removing matches to favourites from the Event details page
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: BMA-7802 'Add 'Favourite Match' functionality to Event Details Pages'
    PRECONDITIONS: **NOTE **:
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   Test case should be validated for Events with primary market title "Match Results" and "Match Betting"
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_football_icon_from_the_sports_menu(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu:
        EXPECTED: -'Football' landing page is opened
        EXPECTED: -‘Favourite matches’ functionality is included
        """
        pass

    def test_003_tap_event_team_a_v_team_b(self):
        """
        DESCRIPTION: Tap 'Event (Team A v Team B)'
        EXPECTED: * 'Event (Team A v Team B) details page is opened
        EXPECTED: * 'Favourite Matches' icon (star icon) is displayed:
        EXPECTED: -before event name in header **for Desktop**
        EXPECTED: -within user tabs area (above market tabs) **for Mobile/Tablet**
        """
        pass

    def test_004_tap_on_the_favourite_maches_icon(self):
        """
        DESCRIPTION: Tap on the 'Favourite Maches' icon
        EXPECTED: -Icon appeared in bold
        EXPECTED: -Event added to the 'Favourite Matches' page
        """
        pass

    def test_005_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        EXPECTED: 
        """
        pass

    def test_006_tap_on_the_favourite_maches_icon_bold_star_icon_in_the_same_event_details_page(self):
        """
        DESCRIPTION: Tap on the 'Favourite Maches' icon (bold star icon) in the same Event details page
        EXPECTED: -Icon became not filled (not selected)
        EXPECTED: -Event removed from the 'Favourite Matches' page
        """
        pass
