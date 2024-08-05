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
class Test_C1274040_Verify_WATCH_button(Common):
    """
    TR_ID: C1274040
    NAME: Verify WATCH button
    DESCRIPTION: This test case verifies video stream on Media Area
    DESCRIPTION: Test case is applicable for 'Horse racing' and 'Greyhounds' details events page
    DESCRIPTION: 'PRE-PARADE' is not available for 'Greyhounds'
    DESCRIPTION: 'Live Commentary' is not available on mobile and tablet, only on desktop
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: BMA-6585 - Racecard Layout Update - Media Area
    DESCRIPTION: BMA-17781 - Live Sim/Watch Free Display Change for Special Open Collapse Button
    DESCRIPTION: BMA-39820 - Desktop HR+ GH Redesign : Race Page - Streaming redesign
    DESCRIPTION: Note: Cannot automate streaming
    PRECONDITIONS: *   Event is started (scheduled race-off time is reached)
    PRECONDITIONS: *   Make sure there is streaming mapped
    PRECONDITIONS: *   User is logged in and placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: *   SiteServer event should be configured to support streaming
    PRECONDITIONS: *   Quantum Leap/Live Sim product is displayed only when it's available based on CMS configs (Log in to CMS and navigate to 'System-configuration' -> 'Config'/'Structure' tab (Coral and Ladbrokes) -> 'QuantumLeapTimeRange')
    PRECONDITIONS: *   URLs for 'Live Commentary' should be set in CMS:
    PRECONDITIONS: GH= https://sport.mediaondemand.net/player/ladbrokes?sport=greyhounds&showmenu=false
    PRECONDITIONS: HR= https://sport.mediaondemand.net/player/ladbrokes?sport=horses&showmenu=false
    PRECONDITIONS: To set links do the following steps:
    PRECONDITIONS: 1) Go to CMS -> System Configuration -> Structure
    PRECONDITIONS: 2) Type in Search field 'LiveCommentary'
    PRECONDITIONS: 3) Paste links in 'Field Value' per each 'Field Name'
    PRECONDITIONS: 4) Click on 'Save changes'
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Horse Racing> icon from the Sports Menu Ribbon
        EXPECTED: Horse Racing landing page is opened
        """
        pass

    def test_003_go_to_event_details_page_and_navigate_to_media_area(self):
        """
        DESCRIPTION: Go to event details page and navigate to media area
        EXPECTED: *For Coral:*
        EXPECTED: **For mobile&tablet:**
        EXPECTED: *   Twо buttons 'PRE-PARADE' and 'WATCH' are displayed and inactive
        EXPECTED: **For desktop:**:
        EXPECTED: *  Twо switchers 'PRE-PARADE' and 'WATCH' are displayed and inactive
        EXPECTED: *For Ladbrokes:*
        EXPECTED: **For mobile&tablet:**
        EXPECTED: *   Twо buttons 'WATCH' and 'PRE-PARADE' are displayed and inactive
        EXPECTED: **For desktop:**:
        EXPECTED: *  Twо switchers 'WATCH' and 'PRE-PARADE' are displayed and inactive
        EXPECTED: *  'Live Commentary' link is displayed
        EXPECTED: *   Microphone icon is shown next to the 'Live Commentary' link
        """
        pass

    def test_004_tap_inactive_watchbutton(self):
        """
        DESCRIPTION: Tap inactive 'WATCH'button
        EXPECTED: Note: different devices will launch stream differently
        EXPECTED: *   The area below 'WATCH' button is expanded
        EXPECTED: *   'WATCH' button becomes active
        EXPECTED: *   'WATCH' label on button is changed to 'DONE'
        EXPECTED: *   Stream is shown
        """
        pass

    def test_005_rotate_device_from_portrait_to_landscape_mode_and_vice_versa(self):
        """
        DESCRIPTION: Rotate device from Portrait to Landscape mode and vice versa
        EXPECTED: Video streaming is rotated accordingly
        """
        pass
