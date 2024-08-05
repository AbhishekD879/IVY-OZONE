import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C1234463_Verify_View_Full_Race_Card_Link(Common):
    """
    TR_ID: C1234463
    NAME: Verify 'View Full Race Card' Link
    DESCRIPTION: This test case is checking of 'Full Race Card' link for Next Races module for greyhounds
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: --
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        pass

    def test_003_on_next_races_module_find_full_race_card_link(self):
        """
        DESCRIPTION: On 'Next Races' module find 'Full Race Card' link
        EXPECTED: 1.  'Full Race Card' is displayed for each event in 'Next 4 Races' module
        EXPECTED: 2.  Link is displayed at the bottom of section
        EXPECTED: 3.  Links is aligned right
        EXPECTED: 4.  Text is hyperlinked
        EXPECTED: 5.  Link is internationalised
        """
        pass

    def test_004_tap_full_race_card_link(self):
        """
        DESCRIPTION: Tap 'Full Race Card' link
        EXPECTED: The event's details page is opened.
        """
        pass

    def test_005_tap_back_button(self):
        """
        DESCRIPTION: Tap back button
        EXPECTED: The previously visited page is opened.
        """
        pass

    def test_006_verify_full_race_card_link_for_event_which_has_less_than_4_selection(self):
        """
        DESCRIPTION: Verify 'Full Race Card' link for event which has less than 4 selection
        EXPECTED: 'Full Race Card' link is pinned to the bottom of the 'Next Races' section
        """
        pass
