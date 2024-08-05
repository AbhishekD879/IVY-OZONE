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
class Test_C50044876_Verify_layout_of_the_Player_Card_view(Common):
    """
    TR_ID: C50044876
    NAME: Verify layout of the 'Player Card' view
    DESCRIPTION: This test case verifies the 'Player Card' view
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football Event Details Page
    PRECONDITIONS: 3. Choose the '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on 'Build' button
    PRECONDITIONS: 5. Click '+' (add) button on 'Pitch' view for selecting some player position with the configured statistic name via CMS
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Statistic is mapped for the particular event. Use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91089483#OPTA/BWINScoreboardmappingtoanOBevent-Appendix_A
    PRECONDITIONS: - Player's statisctic takes from local storage 'scoreBoards_dev_prematch_eventId'(receivs from Bnah) and from response 'players?obEventId=773006'
    PRECONDITIONS: ![](index.php?/attachments/get/61571599)
    PRECONDITIONS: - Players are taken from Banach provider and received in the following response:
    PRECONDITIONS: https://buildyourbet-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/v1/players?obEventId=XXXXX
    PRECONDITIONS: where
    PRECONDITIONS: XXXXX - Event ID
    PRECONDITIONS: ![](index.php?/attachments/get/62325587)
    PRECONDITIONS: - Market value is received in 'statistic-value-range?obEventId=780048&playerId=48&statId=10' request
    """
    keep_browser_open = True

    def test_001_verify_the_player_card_default_view(self):
        """
        DESCRIPTION: Verify the 'Player Card' default view
        EXPECTED: - Page loads with header (clickable 'Back' button/Player name/Team name/player position (if received from Opta), eg. 'A. Webster/Brighton/Forward')
        EXPECTED: - Market selected (eg. 'Goals Inside The Box')
        EXPECTED: - Market value (eg. 1+)
        EXPECTED: - Default step value is displayed as average stat value with clickable +/- buttons on the sides
        EXPECTED: - Player statistics (eg. Goals/Assists)
        EXPECTED: - 'Add Player' button at the bottom with dynamic odds
        EXPECTED: ![](index.php?/attachments/get/62325636)
        EXPECTED: OX 103:
        EXPECTED: - Drop-down with the list of the markets applicable for the player
        EXPECTED: ![](index.php?/attachments/get/114764001)
        """
        pass

    def test_002_verify_the_market_displayed(self):
        """
        DESCRIPTION: Verify the 'Market' displayed
        EXPECTED: - Market is taken from the CMS (BYB -> 5-A-Side -> Stat value)
        """
        pass

    def test_003_verify_the_market_value_eg_1plus(self):
        """
        DESCRIPTION: Verify the market value (eg. 1+)
        EXPECTED: - Market value is received from Banach feed ('statistic-value-range?obEventId=780048&playerId=48&statId=10' request, 'average' value) and is the same as the step value (with +/- buttons)
        """
        pass

    def test_004_verify_player_statistics(self):
        """
        DESCRIPTION: Verify player statistics
        EXPECTED: - Statistic is displayed together with icons (which are hardcoded)
        """
        pass

    def test_005_clicktap_on_market_drop_down(self):
        """
        DESCRIPTION: Click/Tap on Market drop-down
        EXPECTED: - Drop-down is expanded
        EXPECTED: - List of the markets applicable for the player displayed
        """
        pass

    def test_006_select_market_with_static_options_eg_to_be_carded_to_keep_a_clean_sheet(self):
        """
        DESCRIPTION: Select Market with static options (e.g. To Be Carded, To Keep A Clean Sheet)
        EXPECTED: - Market name is changed
        EXPECTED: - Market specific options are changed accordingly
        EXPECTED: - Market stats are changed accordingly
        EXPECTED: - Odds are recalculated
        EXPECTED: - 'Update Player' button is shown instead of 'Add Player'
        EXPECTED: ![](index.php?/attachments/get/114764002)
        """
        pass
