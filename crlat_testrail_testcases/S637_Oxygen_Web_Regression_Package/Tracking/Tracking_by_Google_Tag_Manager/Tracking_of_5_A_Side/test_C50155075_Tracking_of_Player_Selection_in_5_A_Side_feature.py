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
class Test_C50155075_Tracking_of_Player_Selection_in_5_A_Side_feature(Common):
    """
    TR_ID: C50155075
    NAME: Tracking of Player Selection in 5-A-Side feature
    DESCRIPTION: This test case verifies GA tracking during Player selection in 5-A-Side feature on Football EDP
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Football event details page that has '5-A-Side' tab
    PRECONDITIONS: 3. Click/Tap on '5-A-Side' tab
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
    """
    keep_browser_open = True

    def test_001_clicktap_on_plus_button_on_pitch_overlay(self):
        """
        DESCRIPTION: Click/tap on '+' button on pitch overlay
        EXPECTED: Player List View is displayed
        """
        pass

    def test_002_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type **'dataLayer'** in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: * event: "trackEvent"
        EXPECTED: * eventCategory: "5-A-Side"
        EXPECTED: * eventAction: "Choose Player"
        EXPECTED: * eventLabel: <Position Name>
        EXPECTED: where <Position Name> (e.g. Finisher) corresponds to the value, set in 'Position' field in CMS > BYB > 5-A-Side > choose formation under test
        """
        pass

    def test_003__select_any_player_from_player_list_clicktap_add_player(self):
        """
        DESCRIPTION: * Select any player from player list
        DESCRIPTION: * Click/tap 'Add player'
        EXPECTED: Selected Player is added on chosen position on Pitch overlay
        """
        pass

    def test_004_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type **'dataLayer'** in browser's console and verify GA tracking record
        EXPECTED: Record from step #2 is NOT sent to GA tracking
        """
        pass

    def test_005_clicktap_on_previously_selected_player(self):
        """
        DESCRIPTION: Click/Tap on previously selected player
        EXPECTED: Player List View is displayed
        """
        pass

    def test_006_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type **'dataLayer'** in browser's console and verify GA tracking record
        EXPECTED: Record from step #2 is sent to GA tracking.
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: * event: "trackEvent"
        EXPECTED: * eventCategory: "5-A-Side"
        EXPECTED: * eventAction: "Choose Player"
        EXPECTED: * eventLabel: <Position Name>
        EXPECTED: where <Position Name> (e.g. Finisher) corresponds to the value, set in 'Position' field in CMS > BYB > 5-A-Side > choose formation under test
        """
        pass
