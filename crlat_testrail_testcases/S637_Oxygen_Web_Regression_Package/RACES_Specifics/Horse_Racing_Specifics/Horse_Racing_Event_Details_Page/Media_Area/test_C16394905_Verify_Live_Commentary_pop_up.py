import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C16394905_Verify_Live_Commentary_pop_up(Common):
    """
    TR_ID: C16394905
    NAME: Verify Live Commentary pop-up
    DESCRIPTION: This test case verifies 'Live Commentary' functionality
    DESCRIPTION: Test case is applicable for 'Horse racing' and 'Greyhounds' details events page
    DESCRIPTION: 'LIVESIM' is not available for 'Greyhounds'
    DESCRIPTION: 'Live Commentary' is not available on mobile and tablet, only on desktop
    PRECONDITIONS: URLs for 'Live Commentary' should be set in CMS:
    PRECONDITIONS: GH= https://sport.mediaondemand.net/player/ladbrokes?sport=greyhounds&showmenu=false
    PRECONDITIONS: HR= https://sport.mediaondemand.net/player/ladbrokes?sport=horses&showmenu=false
    PRECONDITIONS: To set links do the following steps:
    PRECONDITIONS: 1) Go to CMS -> System Configuration -> Structure
    PRECONDITIONS: 2) Type in Search field 'LiveCommentary'
    PRECONDITIONS: 3) Paste links in 'Field Value' per each 'Field Name'
    PRECONDITIONS: 4) Click on 'Save changes'
    PRECONDITIONS: Please note that Quantum Leap/Live Sim product is displayed only when it's available based on CMS configs (Log in to CMS and navigate to 'System-configuration' -> 'Config'/'Structure' tab (Coral and Ladbrokes) -> 'QuantumLeapTimeRange')
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_click_on_horse_racing_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Click on 'Horse Racing' from the Sports Menu Ribbon
        EXPECTED: 'Horse Racing' landing page is opened
        """
        pass

    def test_003_go_to_event_details_page_and_navigate_to_media_area(self):
        """
        DESCRIPTION: Go to event details page and navigate to Media area
        EXPECTED: Following elements are displayed in Media area section:
        EXPECTED: - 'WATCH' button
        EXPECTED: - 'PRE-PARADE' button
        EXPECTED: - 'Live Commentary' link with Microphone icon on the left side
        """
        pass

    def test_004_click_on_live_commentary_link_in_media_area(self):
        """
        DESCRIPTION: Click on 'Live Commentary' link in Media area
        EXPECTED: 'Live Commentary' pop up is opened
        """
        pass

    def test_005_check_the_elements_on_live_commentary_pop_up(self):
        """
        DESCRIPTION: Check the elements on 'Live Commentary' pop up
        EXPECTED: - Pop-up contains a Close (X) button
        EXPECTED: - Pop-up contains a Ladbrokes logo in the header
        EXPECTED: - Pop-up contains a header with text 'Horse Racing'/'Greyhounds' under logo with expand/collapse button
        EXPECTED: - Pop-up contains an area under header with list of Races (upcoming races are greyed out). List is expanded by default.
        EXPECTED: - Pop-up contains a 'Pause' button with timer in format 'HH:MM' (e.g. "00:03") near it (button icon changes to 'Play' after clicking on it)
        EXPECTED: - Pop-up contains adjustable 'Volume' bar with 'Live' text on the left side
        EXPECTED: 'Please click the play button' message is shown right after the pop up is opened
        EXPECTED: 'Live Commentary' UI for 'Horse Racing':
        EXPECTED: ![](index.php?/attachments/get/34235)
        EXPECTED: 'Live Commentary' UI for 'Greyhounds':
        EXPECTED: ![](index.php?/attachments/get/34236)
        """
        pass

    def test_006_click_on_click_here_for_a_preview_of_upcoming_racing_or_any_available_race(self):
        """
        DESCRIPTION: Click on 'Click here for a preview of upcoming racing' or any available Race
        EXPECTED: 'Live Commentary' playback is started
        """
        pass

    def test_007_click_on_pause_button(self):
        """
        DESCRIPTION: Click on 'Pause' button
        EXPECTED: 'Pause' button changes to 'Play' button
        EXPECTED: 'Live Commentary' playback is paused
        """
        pass

    def test_008_click_on_play_button(self):
        """
        DESCRIPTION: Click on 'Play' button
        EXPECTED: 'Play' button changes to 'Pause' button
        EXPECTED: 'Live Commentary' playback is renewed
        """
        pass

    def test_009_click_on_sound_bar_and_move_it_from_right_to_left(self):
        """
        DESCRIPTION: Click on sound bar and move it from right to left
        EXPECTED: 'Live Commentaries' sound is changed depending on sound bar position
        """
        pass

    def test_010_click_on_x_close_button(self):
        """
        DESCRIPTION: Click on (X) 'Close' button
        EXPECTED: 'Live Commentaries' pop-up is closed
        """
        pass
