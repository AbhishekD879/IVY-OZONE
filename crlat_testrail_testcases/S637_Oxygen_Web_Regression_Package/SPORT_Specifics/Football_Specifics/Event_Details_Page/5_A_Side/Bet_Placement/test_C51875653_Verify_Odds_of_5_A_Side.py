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
class Test_C51875653_Verify_Odds_of_5_A_Side(Common):
    """
    TR_ID: C51875653
    NAME: Verify Odds of '5-A-Side'
    DESCRIPTION: This test case verifies Odds of '5-A-Side' on 'Add Player' button of Player Stats overlay and on 'Place Bet' button of pitch overlay
    PRECONDITIONS: 1. Load the App
    PRECONDITIONS: 2. Login as a User
    PRECONDITIONS: 3. Setup Fractional format in Settings
    PRECONDITIONS: 4. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 5. Click/Tap on '5-A-Side' tab
    PRECONDITIONS: 6. Click/Tap on 'Build' button
    PRECONDITIONS: **Odds formats:**
    PRECONDITIONS: - fractional: '-/-'
    PRECONDITIONS: - decimal: '-,-'
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: **Price response:**
    PRECONDITIONS: To verify Odds data use DevTools -> Network -> 'price' (buildyourbet-hl.ladbrokes.com/api/v1/price)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: * **priceNum**
    PRECONDITIONS: * **priceDen**
    PRECONDITIONS: ![](index.php?/attachments/get/74115548)
    """
    keep_browser_open = True

    def test_001_verify_odds_value_on_place_bet_button(self):
        """
        DESCRIPTION: Verify Odds value on 'Place Bet' button
        EXPECTED: * Odds value is not displayed
        EXPECTED: * 'ODDS -/-' text is displayed as default
        EXPECTED: OX 103:
        EXPECTED: 'Team Odds -/-' text is displayed as default
        """
        pass

    def test_002__clicktap_plus_add_player_button_for_1st_player_select_some_player_from_the_players_list_verify_odds_value_on_add_player_button(self):
        """
        DESCRIPTION: * Click/Tap '+' Add Player button for **1st Player**
        DESCRIPTION: * Select some Player from the Players list
        DESCRIPTION: * Verify Odds value on 'Add Player' button
        EXPECTED: * Player Stats overlay is displayed
        EXPECTED: * Odds value taken from **price** response (see preconditions) is displayed
        EXPECTED: * Odds are displayed in fractional format defined in Settings
        """
        pass

    def test_003__clicktap___button_if_available_verify_odds_value_on_add_player_button(self):
        """
        DESCRIPTION: * Click/Tap '-' button (if available)
        DESCRIPTION: * Verify Odds value on 'Add Player' button
        EXPECTED: * Step value is decreased
        EXPECTED: * Odds value taken from latest **price** response (see preconditions) is displayed
        EXPECTED: * Odds are displayed in fractional format defined in Settings
        """
        pass

    def test_004__clicktap_plus_button_if_available_verify_odds_value_on_add_player_button(self):
        """
        DESCRIPTION: * Click/Tap '+' button (if available)
        DESCRIPTION: * Verify Odds value on 'Add Player' button
        EXPECTED: * Step value is increased
        EXPECTED: * Odds value taken from latest **price** response (see preconditions) is displayed
        EXPECTED: * Odds are displayed in fractional format defined in Settings
        """
        pass

    def test_005__clicktap_back_button_of_player_stats_overlay_clicktap_back_button_of_player_list_overlay_verify_odds_value_on_place_bet_button(self):
        """
        DESCRIPTION: * Click/Tap 'Back' button of Player Stats overlay
        DESCRIPTION: * Click/Tap 'Back' button of Player List overlay
        DESCRIPTION: * Verify Odds value on 'Place Bet' button
        EXPECTED: * Odds value is not displayed
        EXPECTED: * 'ODDS -/-' text is displayed as default
        """
        pass

    def test_006_repeat_step_2(self):
        """
        DESCRIPTION: Repeat Step 2
        EXPECTED: * Odds value taken from latest **price** response (see preconditions) is displayed
        EXPECTED: * Odds are displayed in fractional format defined in Settings
        """
        pass

    def test_007__clicktap_add_player_button_verify_odds_value_on_place_bet_button(self):
        """
        DESCRIPTION: * Click/Tap 'Add Player' button
        DESCRIPTION: * Verify Odds value on 'Place Bet' button
        EXPECTED: * Pitch view overlay is displayed
        EXPECTED: * Odds value is displayed the same as on Player Stats page (from previous step 6)
        EXPECTED: * Odds are displayed in fractional format defined in Settings
        """
        pass

    def test_008__clicktap_plus_add_player_button_for_2nd_player_select_some_player_from_the_players_list_verify_odds_value_on_add_player_button(self):
        """
        DESCRIPTION: * Click/Tap '+' Add Player button for **2nd Player**
        DESCRIPTION: * Select some Player from the Players list
        DESCRIPTION: * Verify Odds value on 'Add Player' button
        EXPECTED: * Player Stats overlay is displayed
        EXPECTED: * Odds value taken from latest **price** response (see preconditions) is displayed
        EXPECTED: * Odds are displayed in fractional format defined in Settings
        """
        pass

    def test_009__clicktap_add_player_button_verify_odds_value_on_place_bet_button(self):
        """
        DESCRIPTION: * Click/Tap 'Add Player' button
        DESCRIPTION: * Verify Odds value on 'Place Bet' button
        EXPECTED: * Pitch view overlay is displayed
        EXPECTED: * Odds value is displayed the same as on Player Stats page (from previous step 8)
        EXPECTED: * Odds are displayed in fractional format defined in Settings
        """
        pass

    def test_010__add_other_3_players_verify_odds_value_on_place_bet_button(self):
        """
        DESCRIPTION: * Add other 3 players
        DESCRIPTION: * Verify Odds value on 'Place Bet' button
        EXPECTED: * Pitch view overlay is displayed
        EXPECTED: * Odds value is displayed the same as on the previous Player Stats page
        EXPECTED: * Odds are displayed in fractional format defined in Settings
        """
        pass

    def test_011__setup_decimal_format_in_settings_repeat_steps_1_10(self):
        """
        DESCRIPTION: * Setup Decimal format in Settings
        DESCRIPTION: * Repeat Steps 1-10
        EXPECTED: OX 103:
        EXPECTED: 'Team Odds -,-' is displayed as default
        """
        pass
