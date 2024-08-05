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
class Test_C28590_Verify_Event_in_Half_Time(Common):
    """
    TR_ID: C28590
    NAME: Verify Event in Half Time
    DESCRIPTION: This test case verifies half time of BIP events.
    PRECONDITIONS: 1) In order to see half time Football event should be BIP event
    PRECONDITIONS: 2) In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **periodCode **with an attribute **state="S" **(this means that the clock is "stopped")
    PRECONDITIONS: *   **periodCode="HALF_TIME" - **Half time in a match/game
    PRECONDITIONS: NOTE: UAT assistance is needed in order to generate half time for BIP event.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
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
        DESCRIPTION: Tap 'In-Play' tab
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_004_verify_football_event_with_half_time_available(self):
        """
        DESCRIPTION: Verify Football event with Half Time available
        EXPECTED: Event with attributes **state="S"** and **periodCode="HALF_TIME"** is shown
        """
        pass

    def test_005_verify_halftime_displaying(self):
        """
        DESCRIPTION: Verify Half Time displaying
        EXPECTED: **'HT' **label is shown instead of Match Time/Start Time
        """
        pass

    def test_006_find_event_from_step_4_and_repeat_step_5(self):
        """
        DESCRIPTION: Find event from step №4 and repeat step №5
        EXPECTED: 
        """
        pass

    def test_007_go_to_the_homepage(self):
        """
        DESCRIPTION: Go to the homepage
        EXPECTED: Homepage is opened
        """
        pass

    def test_008_tap_live_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'LIVE' icon from the Sports Menu Ribbon
        EXPECTED: 'In-Play' tab is shown with 'All Sport' selected
        """
        pass

    def test_009_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 
        """
        pass

    def test_010_tap_football_icon_from_the_sports_menu_ribbon_on_in_play_page(self):
        """
        DESCRIPTION: Tap 'Football' icon from the sports menu ribbon on 'In-Play' page
        EXPECTED: 'Football' page is opened
        """
        pass

    def test_011_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 
        """
        pass

    def test_012_tap_live_stream_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Live Stream' icon from the Sports Menu Ribbon
        EXPECTED: 'Live Stream' page is opened
        """
        pass

    def test_013_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 
        """
        pass

    def test_014_tap_live_stream_tab_on_the_module_selector_ribbon(self):
        """
        DESCRIPTION: Tap 'Live Stream' tab on the Module Selector Ribbon
        EXPECTED: 'Live Stream' tab is opened
        """
        pass

    def test_015_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 
        """
        pass

    def test_016_tap_in_play_tab_on_the_module_selector_ribbon(self):
        """
        DESCRIPTION: Tap 'In-Play' tab on the Module Selector Ribbon
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_017_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 
        """
        pass
