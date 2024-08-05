import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.5_a_side
@vtest
class Test_C59103541_Tracking_of_Editing_of_Player_in_5_A_Side_feature(Common):
    """
    TR_ID: C59103541
    NAME: Tracking of Editing of Player in 5-A-Side feature
    DESCRIPTION: This test case verifies GA tracking during editing of Market in 5-A-Side feature on Football EDP
    PRECONDITIONS: **5-A-Side configuration:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: **Configure a formation if it is not already present:**
    PRECONDITIONS: - Fill ALL fields in CMS -> BYB -> 5-A-Side -> click 'Add New Formation' button -> 'New 5 A Side Formation' popup
    PRECONDITIONS: - Click 'Save' button
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Football event details page that has '5-A-Side' tab
    PRECONDITIONS: 3. Click/Tap on '5-A-Side' tab
    PRECONDITIONS: 4. Market for Player is selected
    """
    keep_browser_open = True

    def test_001_clicktap_on_player_on_pitch_overlay(self):
        """
        DESCRIPTION: Click/tap on 'Player' on pitch overlay
        EXPECTED: 'Player Card' view is displayed
        """
        pass

    def test_002_select_any_other_market_from_drop_down___clicktap_update_player_button(self):
        """
        DESCRIPTION: Select any other Market from drop down -> Click/tap 'Update Player' button
        EXPECTED: - 'Pitch' view is displayed
        EXPECTED: - Changed Market for Player is displayed
        """
        pass

    def test_003_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type **'dataLayer'** in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: * event: "trackEvent"
        EXPECTED: * eventCategory: "5-A-Side"
        EXPECTED: * eventAction: "Edit Market"
        EXPECTED: * eventLabel: <Market Name>
        EXPECTED: Where <Market Name> is Market name of Player set in step #2
        """
        pass

    def test_004_repeat_steps_2_3_with_the_same_player(self):
        """
        DESCRIPTION: Repeat steps #2-3 with the same 'Player'
        EXPECTED: <Market Name> is Market name set in step #2 changed to new one
        """
        pass
