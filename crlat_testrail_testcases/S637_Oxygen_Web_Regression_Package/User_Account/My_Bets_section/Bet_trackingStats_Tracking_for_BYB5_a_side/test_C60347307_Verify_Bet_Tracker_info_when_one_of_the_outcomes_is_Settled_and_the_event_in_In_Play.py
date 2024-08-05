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
class Test_C60347307_Verify_Bet_Tracker_info_when_one_of_the_outcomes_is_Settled_and_the_event_in_In_Play(Common):
    """
    TR_ID: C60347307
    NAME: Verify Bet Tracker info when one of the outcomes is Settled and the event in In Play
    DESCRIPTION: This test case verifies Bet Tracker info when one of the outcome is Settled, but other are still open and event is in-play
    PRECONDITIONS: * Make sure that Bet Tracking feature is enabled in CMS: System-configuration -> Structure -> BetTracking config -> enabled = true
    PRECONDITIONS: * Create a Football event in OpenBet (T.I.)
    PRECONDITIONS: * Request Banach side to map data including Player Bets markets
    PRECONDITIONS: * Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: * Place a Build Your Bet/5-a-side bets with selection template = Range and template = Binary
    PRECONDITIONS: * Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: * Start recorded event (In TI set 'Іs Off' = yes)
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Go to Open Bets page/tab -> event subscription for Opta updates should be made in Live Serv MS: 42["scoreboard","eventID"] and initial response must be received
    PRECONDITIONS: * To check Opta live updates open Dev Tools -> Network tab -> WS -> select request to Live Serv MS
    PRECONDITIONS: * To check OpenBet Outcome Statuses: Dev tools > Network find accountHistory request
    PRECONDITIONS: * Endpoints to Live Serv MS:
    PRECONDITIONS: - wss://liveserve-publisher-dev1.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - dev1
    PRECONDITIONS: **NOTE**
    PRECONDITIONS: Selections with 'template = Binary' means that only 2 options are available. E.g. 'Both Team to score' -> Yes/No.
    PRECONDITIONS: Selections with template = Range' means that multiple-choice prediction is available. E.g. 'Christain Eriksen to Make 55+ Passes'
    """
    keep_browser_open = True

    def test_001_create_build_your_bet_bet_matching_the_following_criteria1st_selection___relates_to_1st_half_ex_result_after_15_minsfirst_team_to_score_in_1st_halfred_card_in_1st_half_etc2nd_selection___relates_to_2nd_half__entire_match(self):
        """
        DESCRIPTION: Create **Build Your Bet** bet matching the following criteria:
        DESCRIPTION: 1st selection - relates to 1st half (ex. RESULT AFTER 15 MINS/FIRST TEAM TO SCORE IN 1ST HALF/RED CARD IN 1ST HALF etc)
        DESCRIPTION: 2nd selection - relates to 2nd half / entire match
        EXPECTED: 
        """
        pass

    def test_002_settle_a_market_related_to_1st_half_used_in_the_bet_in_ob_ti_tool_or_wait_until_its_settled_by_traders(self):
        """
        DESCRIPTION: Settle a Market related to 1st half used in the bet in OB TI tool or wait until it's settled by traders
        EXPECTED: * Outcome should be settled
        EXPECTED: * Bet with the settled outcome stays on 'Open Bets' tab/page
        """
        pass

    def test_003_verify_build_your_bet_bet_updating_statuses(self):
        """
        DESCRIPTION: Verify Build Your Bet bet updating statuses
        EXPECTED: * Statuses for the Settled outcome are received from Openbet
        EXPECTED: * only 'Won'/'Lost' statuses are displayed for this outcome
        EXPECTED: * Progress Bar disappears for this outcome
        EXPECTED: * Statuses for Open outcome continue updating from Live Serv MS
        EXPECTED: * Opta tracking keeps being displayed for the non-settled selections
        """
        pass

    def test_004_settle_event_in_ob_ti_tool_or_wait_until_its_settled_by_traders(self):
        """
        DESCRIPTION: Settle Event in OB TI tool or wait until it's settled by traders
        EXPECTED: * Event should be settled
        EXPECTED: * Bet with settled event disappears from 'Open Bets' tab/page after its refresh
        """
        pass

    def test_005_verify_build_your_bet_bet_displaying_in_settled_bets(self):
        """
        DESCRIPTION: Verify Build Your Bet bet displaying in Settled bets
        EXPECTED: * Won / Lost indicators(ticks/crosses) are displayed for the final result for each selection
        EXPECTED: * Progress bars are NOT displayed anymore for selections with **Range** template
        EXPECTED: * Final result for stats descriptions are shown (e.g. 2 Goals, 49 Passes) for selections with **Range** template
        EXPECTED: ![](index.php?/attachments/get/114837485) ![](index.php?/attachments/get/114837490)
        """
        pass

    def test_006_coralgo_to_my_bets_tab_and_repeat_steps_1_5(self):
        """
        DESCRIPTION: **Coral**
        DESCRIPTION: Go to My Bets tab and repeat steps 1-5
        EXPECTED: 
        """
        pass

    def test_007_go_to_cash_out_tab_and_repeat_steps_1_5_coral_only(self):
        """
        DESCRIPTION: Go to Cash out tab and repeat steps #1-5 (Coral only)
        EXPECTED: 
        """
        pass
