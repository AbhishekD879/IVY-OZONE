import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C60473228_Verify_Winning_Lossing_Left_hand_indicators_for_correct_score_market(Common):
    """
    TR_ID: C60473228
    NAME: Verify Winning/Lossing Left-hand indicators for correct score market
    DESCRIPTION: This test case verifies left hand Stat indicators for correct score market.
    PRECONDITIONS: Create a Football event in OpenBet (TI)
    PRECONDITIONS: Request Banach side to map data including Player Bets markets
    PRECONDITIONS: Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: Load app and log in
    PRECONDITIONS: To check Opta live updates subscription open Dev Tools -> Network tab -> WS -> select request to Live Serv MS
    PRECONDITIONS: Endpoints to Live Serv MS:
    PRECONDITIONS: wss://liveserve-publisher-dev1.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - dev1
    """
    keep_browser_open = True

    def test_001_place_a_byb_bet_on_an_event_with_opta_stats_available___consisting_of_the_following_marketscorrect_score1st_half_correct_score2nd_half_correct_score(self):
        """
        DESCRIPTION: Place a BYB bet on an event with Opta stats available - consisting of the following markets:
        DESCRIPTION: Correct Score
        DESCRIPTION: 1st Half Correct Score
        DESCRIPTION: 2nd Half Correct Score
        EXPECTED: Bet placed successfully and it should be available in My bets> Open bets/ Cash out (Coral) tabs.
        """
        pass

    def test_002_go_to_ti_and_change_the_event_from_pre_play_to_in_play_state_is_off__yes_save_changes_or_wait_until_it_was_done_by_trader(self):
        """
        DESCRIPTION: Go to TI and change the event from pre-play to in play state (Is OFF = YES) Save changes. or wait until it was done by trader.
        EXPECTED: Changes are successfully saved
        """
        pass

    def test_003_go_back_to_the_app___my_betsopen_bets_tab__without_refreshing_the_page_verify_the_left_hand_stat_indicators_forcorrect_score1st_half_correct_score2nd_half_correct_score_markets(self):
        """
        DESCRIPTION: Go back to the app -> My Bets/Open Bets tab  without refreshing the page. Verify the left hand stat indicators for
        DESCRIPTION: Correct Score
        DESCRIPTION: 1st Half Correct Score
        DESCRIPTION: 2nd Half Correct Score markets.
        EXPECTED: Default indicators should shown with out page refresh.
        EXPECTED: Indicator will depend on opening prediction e.g If prediction is 0-0 then green starting position, if prediction is 1-0, then red starting position.
        """
        pass

    def test_004_trigger_winning_for_one_of_selection(self):
        """
        DESCRIPTION: Trigger winning for one of selection
        EXPECTED: Opta update is received in WS.
        EXPECTED: Green arrow showing up appears on left side of the selection name without page refresh.
        EXPECTED: ![](index.php?/attachments/get/129019509)
        """
        pass

    def test_005_trigger_losing_for_one_of_selection(self):
        """
        DESCRIPTION: Trigger losing for one of selection
        EXPECTED: Opta update is received in WS.
        EXPECTED: Red arrow showing down appears on left side of the selection name without page refresh.
        EXPECTED: ![](index.php?/attachments/get/129019507)
        """
        pass

    def test_006_verify_won_indicator_if_your_prediction_won(self):
        """
        DESCRIPTION: Verify won indicator if your prediction won
        EXPECTED: won indicator(Green tick) should be displayed on left side of selection only after that particular time period completion.(e.g: Green tick should display after completion of first half if you placed First half correct score market.)
        EXPECTED: ![](index.php?/attachments/get/129019511)
        """
        pass

    def test_007_verify_lost_red_cross_indicator_if_your_prediction_lost(self):
        """
        DESCRIPTION: Verify lost (Red cross) indicator if your prediction lost
        EXPECTED: Red cross should de displayed on left side of selection with out page refresh.
        EXPECTED: ![](index.php?/attachments/get/129019510)
        """
        pass

    def test_008_go_to_cash_out_pagetab_and_repeat_steps_2_7_coral_only(self):
        """
        DESCRIPTION: Go to 'Cash out' page/tab and repeat steps #2-7 (Coral only)
        EXPECTED: 
        """
        pass

    def test_009_go_to_my_bets_tab_on_football_edp_and_repeat_steps_2_7_coral_only(self):
        """
        DESCRIPTION: Go to 'My Bets' tab on Football EDP and repeat steps #2-7 (Coral only)
        EXPECTED: 
        """
        pass

    def test_010_go_to_user_menu_history_betting_history_open_bets_tab_repeat_all_steps(self):
        """
        DESCRIPTION: Go to User menu> History> Betting history> Open bets tab Repeat all steps
        EXPECTED: 
        """
        pass
