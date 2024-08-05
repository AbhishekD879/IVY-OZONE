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
class Test_C28606_Verify_Favourite_Match_functionality_in_the_Event_Details_Pages(Common):
    """
    TR_ID: C28606
    NAME: Verify 'Favourite Match' functionality in the Event Details Pages
    DESCRIPTION: This Test Case verifies 'Favourite Match' functionality in the Event Details Pages
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
        EXPECTED: Home page is opened
        """
        pass

    def test_002_tap_football_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        EXPECTED: 'Football' landing page is opened
        """
        pass

    def test_003_tap_in_play_tab(self):
        """
        DESCRIPTION: Tap 'In Play' tab
        EXPECTED: 'In Play' tab is opened
        """
        pass

    def test_004_tap_on_any_eventevent1(self):
        """
        DESCRIPTION: Tap on any event(Event1)
        EXPECTED: * Event1 Event details page is opened
        EXPECTED: * 'Favourite Matches' icon (star icon) is displayed:
        EXPECTED: -before event name in header **for Desktop**
        EXPECTED: -within user tabs area (above market tabs) **for Mobile/Tablet**
        """
        pass

    def test_005_tap_on_the_favourite_maches_icon_star_icon_for_event1(self):
        """
        DESCRIPTION: Tap on the 'Favourite Maches' icon (star icon) for Event1
        EXPECTED: * Icon appeared in bold (filled with yellow color)
        EXPECTED: * Event1 is added to the 'Favorite Matches' page.
        """
        pass

    def test_006_tap_on_the_favourite_maches_icon_star_icon_for_event1_again(self):
        """
        DESCRIPTION: Tap on the 'Favourite Maches' icon (star icon) for Event1 again
        EXPECTED: * Icon appeared empty (not filled with yellow color)
        EXPECTED: * Event1 is removed from the 'Favorite Matches' page.
        """
        pass

    def test_007_tap_on_the_back_button_and_verify_favourite_maches_icon_for_event1(self):
        """
        DESCRIPTION: Tap on the 'Back' button and verify 'Favourite Maches' icon for Event1
        EXPECTED: * User is redirected to the tab from Step 3.
        EXPECTED: * 'Favourite Matches’ icons is displayed empty bellow Event1
        EXPECTED: * Event1 is not present on 'Favorite Matches' page.
        """
        pass

    def test_008_tap_on_the_favourite_maches_icon_star_icon_below_matchevent_for_any_other_eventevent2(self):
        """
        DESCRIPTION: Tap on the 'Favourite Maches' icon (star icon) below match/event for any other event(Event2)
        EXPECTED: * Icon appeared in bold (filled with yellow color)
        EXPECTED: * Event2 is added to the 'Favorite Matches' page.
        """
        pass

    def test_009_tap_on_event2_and_verify_favourite_maches_icon_on_event_details_page(self):
        """
        DESCRIPTION: Tap on Event2 and verify 'Favourite Maches' icon on Event Details page
        EXPECTED: 'Favourite Matches’ icon is displayed in bold (filled with yellow color)
        """
        pass

    def test_010_tap_on_the_bold_favourite_maches_icon_star_icon_for_event2(self):
        """
        DESCRIPTION: Tap on the bold 'Favourite Maches' icon (star icon) for Event2
        EXPECTED: * 'Favourite Matches’ icons is displayed empty (becomes unchecked)
        EXPECTED: * Event2 is removed from the 'Favorite Matches' page.
        """
        pass

    def test_011_tap_on_the_back_button_and_verify_favourite_maches_icon_for_event2(self):
        """
        DESCRIPTION: Tap on the 'Back' button and verify 'Favourite Maches' icon for Event2
        EXPECTED: * 'Favourite Matches’ icons is displayed empty bellow Event2
        EXPECTED: * Event2 is not present on 'Favorite Matches' page.
        """
        pass

    def test_012_repeat_steps_1_11_for(self):
        """
        DESCRIPTION: Repeat steps 1-11 for
        EXPECTED: *   'In-Play' tab
        EXPECTED: *   'Matches' tab
        EXPECTED: *   'Competitions' page
        EXPECTED: *   'Coupons' page
        """
        pass
