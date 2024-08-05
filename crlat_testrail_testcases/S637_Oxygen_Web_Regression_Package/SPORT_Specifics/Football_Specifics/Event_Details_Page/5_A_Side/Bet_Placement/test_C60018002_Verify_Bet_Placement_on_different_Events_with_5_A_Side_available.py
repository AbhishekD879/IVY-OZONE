import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C60018002_Verify_Bet_Placement_on_different_Events_with_5_A_Side_available(Common):
    """
    TR_ID: C60018002
    NAME: Verify Bet Placement on different Events with '5-A-Side' available
    DESCRIPTION: This test case verifies Bet Placement on different Events with '5-A-Side' available
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Two Events under test(EventA, EventB) are mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Events are prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: 1) User is logged in.
    PRECONDITIONS: 2) User navigates to EventA Event Details Page -> '5 A Side' tab
    PRECONDITIONS: Example of BYB Players request:
    PRECONDITIONS: https://buildyourbet.{ladbrokes/coral domain}/api/v1/players?obEventId={EventID}
    """
    keep_browser_open = True

    def test_001_open_5_a_side_widgetverify_event_name_displayed_on_5_a_side_overlay(self):
        """
        DESCRIPTION: Open '5 A Side' widget
        DESCRIPTION: Verify Event name displayed on '5 A Side' overlay.
        EXPECTED: - '5 A Side' overlay is displayed
        EXPECTED: - Event Name is equal to one that is shown on EDP for EventA
        """
        pass

    def test_002_pick_any_formation_and_add_any_players_to_fill_the_formationverify_that_user_is_able_to_add_players_from_eventa_to_selected_formation(self):
        """
        DESCRIPTION: Pick any formation and add any Players to fill the formation.
        DESCRIPTION: Verify that User is able to add Players from EventA to selected formation.
        EXPECTED: - User is able to add Players to selected formation
        EXPECTED: - List of Users that are available for adding are taken from Users received in BYB Players request(https://buildyourbet.{ladbrokes/coral domain}/api/v1/players?obEventId={eventID})
        """
        pass

    def test_003_place_a_bet_for_filled_5_a_side_formationverify_that_user_is_able_to_place_5_a_side_formation_bet(self):
        """
        DESCRIPTION: Place a bet for filled '5 A Side' formation.
        DESCRIPTION: Verify that User is able to place '5 A Side' formation bet.
        EXPECTED: - '5 A Side' QuickBet widget is displayed
        EXPECTED: - '5 A Side' QuickBet widget contains Players and markets taken from Formation from Step 2.
        EXPECTED: - User is able to successfully place a bet for Formation from Step 2
        """
        pass

    def test_004_navigate_to_eventb_event_details_page___5_a_side_tab_and_open_5_a_side_widgetverify_event_name_displayed_on_5_a_side_overlay(self):
        """
        DESCRIPTION: Navigate to EventB Event Details Page -> '5 A Side' tab and Open '5 A Side' widget.
        DESCRIPTION: Verify Event name displayed on '5 A Side' overlay.
        EXPECTED: - '5 A Side' overlay is displayed
        EXPECTED: - Event Name is equal to one that is shown on EDP for EventB
        """
        pass

    def test_005_pick_any_formation_and_add_any_players_to_fill_the_formationverify_that_user_is_able_to_add_players_from_eventa_to_selected_formation(self):
        """
        DESCRIPTION: Pick any formation and add any Players to fill the formation.
        DESCRIPTION: Verify that User is able to add Players from EventA to selected formation.
        EXPECTED: - User is able to add Players to selected formation
        EXPECTED: - List of Users that are available for adding are taken from Users received in BYB Players request(https://buildyourbet.{ladbrokes/coral domain}/api/v1/players?obEventId={eventID})
        """
        pass

    def test_006_place_a_bet_for_filled_5_a_side_formationverify_that_user_is_able_to_place_5_a_side_formation_bet(self):
        """
        DESCRIPTION: Place a bet for filled '5 A Side' formation.
        DESCRIPTION: Verify that User is able to place '5 A Side' formation bet.
        EXPECTED: - '5 A Side' QuickBet widget is displayed
        EXPECTED: - '5 A Side' QuickBet widget contains Players and markets taken from Formation from Step 5.
        EXPECTED: - User is able to successfully place a bet for Formation from Step 5
        """
        pass
