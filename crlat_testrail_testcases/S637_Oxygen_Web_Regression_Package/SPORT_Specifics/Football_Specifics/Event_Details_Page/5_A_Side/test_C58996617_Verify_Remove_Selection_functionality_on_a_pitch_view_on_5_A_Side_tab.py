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
class Test_C58996617_Verify_Remove_Selection_functionality_on_a_pitch_view_on_5_A_Side_tab(Common):
    """
    TR_ID: C58996617
    NAME: Verify 'Remove Selection' functionality on a pitch view on '5-A-Side' tab
    DESCRIPTION: This test case verified 'Remove Selection' functionality on a pitch view on '5-A-Side' tab on Football EDP.
    PRECONDITIONS: 1. Event has configured 5-A-Side and BYB markets.
    PRECONDITIONS: 2. 5-A-Side config:
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (TI) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Opta statistics is mapped to the event (ask Natalia Shalay to help)
    PRECONDITIONS: - Formations are created and set up in CMS/BYB/5 A Side
    PRECONDITIONS: - Event is prematch (not live)
    """
    keep_browser_open = True

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application.
        EXPECTED: Application is opened.
        """
        pass

    def test_002_navigate_to_football_event_details_page_that_has_5_a_side_data_configured(self):
        """
        DESCRIPTION: Navigate to Football event details page that has 5-A-Side data configured.
        EXPECTED: Football EDP is opened.
        """
        pass

    def test_003_clicktap_on_5_a_side_tab(self):
        """
        DESCRIPTION: Click/Tap on '5-A-Side' tab.
        EXPECTED: '5-A-Side' tab with appropriate data is shown.
        """
        pass

    def test_004_clicktap_build_your_team_button_ladbrokes_build_button_coral(self):
        """
        DESCRIPTION: Click/Tap 'Build Your Team' button (Ladbrokes) 'Build' button (Coral).
        EXPECTED: Pitch view with created formations is shown.
        """
        pass

    def test_005_clicktap_on_plus_button_for_any_position_on_any_formation(self):
        """
        DESCRIPTION: Click/Tap on '+' button for any position on any formation.
        EXPECTED: The list of players is shown for both teams for the opened market.
        """
        pass

    def test_006_clicktap_on_some_player_and_then_clicktap_add_player_button(self):
        """
        DESCRIPTION: Click/Tap on some player and then click/tap 'Add Player' button.
        EXPECTED: Selected Player is shown on the position, opened on the previous step.
        """
        pass

    def test_007_clicktap_on_just_filled_position(self):
        """
        DESCRIPTION: Click/Tap on just filled position.
        EXPECTED: 'Edit Player' card/overlay is shown with 'Remove Selection' button and other info.
        """
        pass

    def test_008_clicktap_remove_selection_button(self):
        """
        DESCRIPTION: Click/Tap 'Remove Selection' button.
        EXPECTED: 'Remove Player' pop-up appeared with 'Are you sure you want to remove this player from your team? message and 'Cancel'/'Remove' buttons.
        """
        pass

    def test_009_clicktap_cancel_button(self):
        """
        DESCRIPTION: Click/Tap 'Cancel' button
        EXPECTED: 'Remove Player' pop-up is closed and user stays on 'Edit Player' card/overlay.
        """
        pass

    def test_010_clicktap_remove_selection_button_and_then_confirm_removal_action(self):
        """
        DESCRIPTION: Click/Tap 'Remove Selection' button and then confirm removal action.
        EXPECTED: Pitch view is loaded and the removed player is not displayed on it.
        EXPECTED: Odds are updated accordingly to not include removed Player.
        """
        pass
