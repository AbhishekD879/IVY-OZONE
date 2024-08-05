import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C60013399_Verify_the_displaying_of_markets_with_Range_template(Common):
    """
    TR_ID: C60013399
    NAME: Verify the displaying of markets with Range template
    DESCRIPTION: Test case verifies the status indicators and progress bar for markets with Range template
    PRECONDITIONS: * Make sure that Bet Tracking feature is enabled in CMS: System-configuration -> Structure -> BetTracking config -> enabled = true
    PRECONDITIONS: * Create a Football event in OpenBet (T.I.)
    PRECONDITIONS: * Request Banach side to map data including Player Bets markets
    PRECONDITIONS: * Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: * Place a Build Your Bet/5-a-side bet on selection with template = Range e.g. |BUILD YOUR BET| |PLAYER TOTAL ASSISTS|/|PLAYER TOTAL GOALS|(full list of markets with Range template is in https://docs.google.com/spreadsheets/d/1IfObAqOR-1YWthXpimEKSCTfqdAj0D6beP2xU03VQUk/edit?usp=sharing)
    PRECONDITIONS: * Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: * Start recorded event (In TI set 'Іs Off' = yes)
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Go to Open Bets page/tab -> event subscription for Opta updates should be made in Live Serv MS: 42["scoreboard","eventID"] and initial response must be received
    PRECONDITIONS: * To check Opta live updates open Dev Tools -> Network tab -> WS -> select request to Live Serv MS
    PRECONDITIONS: * Endpoints to Live Serv MS:
    PRECONDITIONS: wss://liveserve-publisher-dev1.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - dev1
    PRECONDITIONS: NOTE In order to have valid Opta statistic updates data across 3 providers (OpenBet, Banach, Opta) should be the same. Event, selections names should be the same on OpenBet TI, Banach, Opta endpoints. This is the ideal case and due to lack of data on TST2 env may be checked on PROD env.
    PRECONDITIONS: e.g. Event with name |Liverpool| |vs| |Arsenal| in OpenBet should have selections with: |Liverpool|,|Draw|,|Arsenal|. Banach and Opta statistic should be mapped to the event with the same info: Liverpool vs Arsenal.
    PRECONDITIONS: NOTE Four Possible Status values exist: 'Won|Lose|Winning|Losing', but not all are applicable for all Range markets
    PRECONDITIONS: All market rules are described in https://coralracing-my.sharepoint.com/:x:/r/personal/david_hainey_gvcgroup_com/_layouts/15/Doc.aspx?sourcedoc=%7B1d88fbe3-9ad1-4da2-af29-081335486de3%7D&action=edit&activeCell=%27MARKET_RULES_DH%27!F86&wdrcid=f44ed3e4-646b-4b4b-80a5-4620215bcf8b&wdrldc=1&cid=d6f6467d-0c03-419e-8bbb-f9fd63d19350
    """
    keep_browser_open = True

    def test_001_go_to_open_bets_tabpage_and_find_build_your_bet_bet(self):
        """
        DESCRIPTION: Go to 'Open bets' tab/page and find Build Your Bet bet
        EXPECTED: * Build Your Bet bet is present on 'Open bets' tab/page with selections with Binary and Range templates
        EXPECTED: * WS connection with Live Serv MS is created
        EXPECTED: * 42["scoreboard","eventID"] request is sent to subscribe for Opta updates
        EXPECTED: * Initial data structure response is received
        """
        pass

    def test_002_trigger_lose_status_for_one_of_selectioneg_user_have_placed_a_bet_on_player1_to_score_1plus_goals_in_1st_half_and_player1_didnt_score_any_goal_in_1st_half(self):
        """
        DESCRIPTION: Trigger Lose status for one of selection
        DESCRIPTION: e.g. User have placed a bet on Player1 'To Score 1+ Goals In 1st Half' and Player1 didn't score any goal in 1st Half
        EXPECTED: * Opta live update is received in WS (see preconditions)
        EXPECTED: * Stats tracking field is updated automatically
        EXPECTED: * Left-hand indicator is shown
        EXPECTED: ![](index.php?/attachments/get/120999189)
        EXPECTED: * Progress bar indicator is displayed
        EXPECTED: ![](index.php?/attachments/get/121422785)
        """
        pass

    def test_003_trigger_won_status_for_one_of_selectioneg_team_a_scored_1_goal_and_user_have_placed_bet_on_over_05_goals_build_your_bet_total_goals(self):
        """
        DESCRIPTION: Trigger Won status for one of selection
        DESCRIPTION: e.g. Team-A scored 1 goal and user have placed bet on Over 0,5 Goals 'Build Your Bet TOTAL GOALS'
        EXPECTED: * Opta live update is received in WS (see preconditions)
        EXPECTED: * Stats tracking field is updated automatically
        EXPECTED: * Left-hand indicator is shown
        EXPECTED: ![](index.php?/attachments/get/120999114)
        EXPECTED: * Progress bar indicator is displayed
        EXPECTED: ![](index.php?/attachments/get/120999115)
        """
        pass

    def test_004_trigger_losing_status_for_one_of_selectioneg_user_have_placed_a_bet_on_player1_build_your_bet_to_score_exactly_1_goal_and_player1_still_doesnt_score_any_goal(self):
        """
        DESCRIPTION: Trigger Losing status for one of selection
        DESCRIPTION: e.g. User have placed a bet on Player1 'Build Your Bet TO SCORE EXACTLY 1 GOAL' and Player1 still doesn't score any goal
        EXPECTED: * Opta live update is received in WS (see preconditions)
        EXPECTED: * Stats tracking field is updated automatically
        EXPECTED: * Left-hand indicator is shown
        EXPECTED: ![](index.php?/attachments/get/120999190)
        EXPECTED: * Progress bar indicator is displayed
        EXPECTED: ![](index.php?/attachments/get/121422734)
        """
        pass

    def test_005_trigger_winning_status_for_one_of_selectioneg_user_have_placed_a_bet_on_player1_build_your_bet_to_score_exactly_1_goal_and_player1_already_scored_1_goal(self):
        """
        DESCRIPTION: Trigger Winning status for one of selection
        DESCRIPTION: e.g. User have placed a bet on Player1 'Build Your Bet TO SCORE EXACTLY 1 GOAL' and Player1 already scored 1 goal
        EXPECTED: * Opta live update is received in WS (see preconditions)
        EXPECTED: * Stats tracking field is updated automatically
        EXPECTED: * Left-hand indicator is shown
        EXPECTED: ![](index.php?/attachments/get/120999191)
        EXPECTED: * Progress bar indicator is displayed
        EXPECTED: ![](index.php?/attachments/get/121422740)
        """
        pass

    def test_006_go_to_cash_out_pagetab_and_repeat_steps_1_5_coral_only(self):
        """
        DESCRIPTION: Go to 'Cash out' page/tab and repeat steps #1-5 (Coral only)
        EXPECTED: 
        """
        pass

    def test_007_go_to_my_bets_tab_on_football_edp_and_repeat_steps_1_5_coral_only(self):
        """
        DESCRIPTION: Go to 'My Bets' tab on Football EDP and repeat steps #1-5 (Coral only)
        EXPECTED: 
        """
        pass

    def test_008_settle_event_in_ob_ti_tool_or_wait_until_its_ended_and_go_to_settled_bets_tab(self):
        """
        DESCRIPTION: Settle event in OB TI tool or wait until it's ended and go to 'Settled bets' tab
        EXPECTED: * 'Settled bets' tab is opened
        EXPECTED: * Event is subscribed for Opta updates to Live Serv MS in WS
        EXPECTED: * Subscription request 42["scoreboard","eventID"] is sent, where 'eventID' - id of created event in OB
        EXPECTED: * The very last updated is received
        """
        pass

    def test_009_check_build_your_bet_betdisplaying(self):
        """
        DESCRIPTION: Check Build Your Bet bet
        DESCRIPTION: displaying
        EXPECTED: * Winning/loosing indicators(ticks/crosses) are displayed for the final result for each selection
        EXPECTED: * Progress bars are NOT displayed anymore
        EXPECTED: * Final result for stats descriptions are shown (e.g. 2 Goals, 49 Passes)
        """
        pass

    def test_010_repeat_steps_1_9_for_5_a_side_bet(self):
        """
        DESCRIPTION: Repeat steps #1-9 for 5-a-side bet
        EXPECTED: 
        """
        pass
