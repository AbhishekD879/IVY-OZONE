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
class Test_C60471271_Verify_Bet_tracker_of_Red_Card_related_markets_when_there_are_no_Red_cards_in_the_match(Common):
    """
    TR_ID: C60471271
    NAME: Verify Bet tracker of "Red Card" related markets when there are no Red cards in the match.
    DESCRIPTION: Note : In a Football event, when the player receives a second yellow card (Same player when receives two yellow cards) it should be considered as Red cards and the stats for all the "Red card" markets listed below should be updated accordingly.
    DESCRIPTION: Epic:https://jira.egalacoral.com/browse/BMA-47914
    DESCRIPTION: Red card related markets:
    DESCRIPTION: 1.Build Your Bet Red card participant-1
    DESCRIPTION: 2.Build Your Bet Red card participant-2
    DESCRIPTION: 3.Build Your Bet Red card in match
    DESCRIPTION: 4.Build Your Bet Red card in 1st half
    DESCRIPTION: 5.Build Your Bet Red card in 2nd half
    PRECONDITIONS: Create a Football event in OpenBet (TI)
    PRECONDITIONS: Request Banach side to map data including Player Bets markets
    PRECONDITIONS: Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: Load app and log in
    PRECONDITIONS: To check Opta live updates subscription open Dev Tools -> Network tab -> WS -> select request to Live Serv MS
    PRECONDITIONS: Endpoints to Live Serv MS:
    PRECONDITIONS: wss://liveserve-publisher-dev1.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - dev1
    PRECONDITIONS: Event should have BYB markets related to Red cards and bets should be placed on the respective markets.
    PRECONDITIONS: And Match should have a Red card to verify the stats of the markets.
    """
    keep_browser_open = True

    def test_001_when_there_is_no_red_card_allotted_in_the_match_for_participant_121build_your_bet_red_card_participant_1_placed_on_yes_selection2build_your_bet_red_card_participant_1_placed_on_no_selection(self):
        """
        DESCRIPTION: When there is NO Red card allotted in the match for Participant-1/2.
        DESCRIPTION: 1.Build Your Bet Red card participant-1 placed on "Yes" selection
        DESCRIPTION: 2.Build Your Bet Red card participant-1 placed on "No" selection
        EXPECTED: Opta update is received in WS.
        EXPECTED: 1. Bet is loosing (Red Down arrow)
        EXPECTED: 2. Bet wins (Red cross) after settlement till then arrow is shown.
        """
        pass

    def test_002_when_there_is_no_red_card_allotted_in_the_match_for_participant_121build_your_bet_red_card_in_match_placed_on_yes_selection2build_your_bet_red_card_in_match_placed_on_no_selection(self):
        """
        DESCRIPTION: When there is NO Red card allotted in the match for Participant-1/2.
        DESCRIPTION: 1.Build Your Bet Red card in match placed on "Yes" selection
        DESCRIPTION: 2.Build Your Bet Red card in match placed on "No" selection
        EXPECTED: Opta update is received in WS.
        EXPECTED: 1. Bet is loosing (Red Down arrow)
        EXPECTED: 2. Bet wins (Red cross) after settlement till then arrow is shown.
        """
        pass

    def test_003_when_there_is_no_red_card_allotted_in_the_match_for_participant_12_in_1st_hald1build_your_bet_red_card_in_1st_half_placed_on_yes_selection2build_your_bet_red_card_in_1st_half_placed_on_no_selection(self):
        """
        DESCRIPTION: When there is NO Red card allotted in the match for Participant-1/2 in 1st Hald.
        DESCRIPTION: 1.Build Your Bet Red card in 1st half placed on "Yes" selection
        DESCRIPTION: 2.Build Your Bet Red card in 1st half placed on "No" selection
        EXPECTED: Opta update is received in WS.
        EXPECTED: 1. Bet is loosing (Red Down arrow)
        EXPECTED: 2. Bet wins (Red cross) after settlement till then arrow is shown.
        """
        pass

    def test_004_when_there_is_no_red_card_allotted_in_the_match_for_participant_12_in_2nd_half1build_your_bet_red_card_in_2nd_half_placed_on_yes_selection2build_your_bet_red_card_in_2nd_half_placed_on_no_selection(self):
        """
        DESCRIPTION: When there is NO Red card allotted in the match for Participant-1/2 in 2nd Half.
        DESCRIPTION: 1.Build Your Bet Red card in 2nd half placed on "Yes" selection
        DESCRIPTION: 2.Build Your Bet Red card in 2nd half placed on "No" selection
        EXPECTED: Opta update is received in WS.
        EXPECTED: 1. Bet is loosing (Red Down arrow)
        EXPECTED: 2. Bet wins (Red cross) after settlement till then arrow is shown.
        """
        pass

    def test_005_go_to_cash_out_pagetab_and_repeat_steps_2_7_coral_only(self):
        """
        DESCRIPTION: Go to 'Cash out' page/tab and repeat steps #2-7 (Coral only)
        EXPECTED: 
        """
        pass

    def test_006_go_to_my_bets_tab_on_football_edp_and_repeat_steps_2_7_coral_only(self):
        """
        DESCRIPTION: Go to 'My Bets' tab on Football EDP and repeat steps #2-7 (Coral only)
        EXPECTED: 
        """
        pass

    def test_007_go_to_user_menu_history_betting_history_open_bets_tab_repeat_all_steps(self):
        """
        DESCRIPTION: Go to User menu> History> Betting history> Open bets tab Repeat all steps
        EXPECTED: 
        """
        pass
