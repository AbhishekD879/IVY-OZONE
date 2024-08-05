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
class Test_C59104019_Verify_editing_market_for_player(Common):
    """
    TR_ID: C59104019
    NAME: Verify editing market for player
    DESCRIPTION: This test case verifies the ability to edit of player's previously selected market on 'Player Card' view on '5-A-Side' tab
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Choose on '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on 'Build' button
    PRECONDITIONS: 5. Click/Tap '+' (add) button > Select any player
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    """
    keep_browser_open = True

    def test_001_verify_player_card_view(self):
        """
        DESCRIPTION: Verify 'Player Card' view
        EXPECTED: * Selected player is displayed with appropriate statistics info for that player (if available)
        EXPECTED: * Drop-down with the list of the markets applicable for the player is displayed
        EXPECTED: * 'Add player' button
        EXPECTED: ![](index.php?/attachments/get/114764015)
        """
        pass

    def test_002_clicktap_add_player(self):
        """
        DESCRIPTION: Click/Tap 'Add player'
        EXPECTED: 'Pitch View' section is displayed with the selected player(s)
        """
        pass

    def test_003_clicktap_on_previously_selected_player(self):
        """
        DESCRIPTION: Click/Tap on previously selected player
        EXPECTED: * 'Player Card' view of previously selected player is displayed with appropriate statistics info for that player (if available)
        EXPECTED: * Drop-down with the list of the markets applicable for the player is displayed (Markets are not limited with current formation and are taken from 'player-statistics?obEventId=978373&playerId=52' request)
        EXPECTED: * 'Update player' button
        EXPECTED: ![](index.php?/attachments/get/114764017)
        """
        pass

    def test_004_clicktap_on_back_button_on_player_card_view(self):
        """
        DESCRIPTION: Click/Tap on 'Back' button on 'Player Card' view
        EXPECTED: * 'Pitch View' section is displayed
        EXPECTED: * Player, player's market and odds remain unchanged
        """
        pass

    def test_005_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step #3
        EXPECTED: 
        """
        pass

    def test_006_clicktap_drop_down___select_any_market_from_available(self):
        """
        DESCRIPTION: Click/Tap drop-down -> Select any market from available
        EXPECTED: * Market for player is changed
        EXPECTED: * Market specific options are changed accordingly
        EXPECTED: * Player stats are changed accordingly
        EXPECTED: * Odds are changed accordingly
        """
        pass

    def test_007_repeat_step_6_few_times(self):
        """
        DESCRIPTION: Repeat step #6 few times
        EXPECTED: 
        """
        pass

    def test_008_click_update_player(self):
        """
        DESCRIPTION: Click 'Update Player'
        EXPECTED: * 'Pitch View' section is displayed
        EXPECTED: * Player is not changing it's position on the pitch
        EXPECTED: * The last selected market from step #7 is displayed
        EXPECTED: * Changed odds are displayed
        """
        pass
