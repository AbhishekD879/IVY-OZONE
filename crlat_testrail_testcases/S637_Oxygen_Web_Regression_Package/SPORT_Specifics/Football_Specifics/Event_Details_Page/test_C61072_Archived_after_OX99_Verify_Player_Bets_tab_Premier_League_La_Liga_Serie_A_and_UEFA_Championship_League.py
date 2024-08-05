import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C61072_Archived_after_OX99_Verify_Player_Bets_tab_Premier_League_La_Liga_Serie_A_and_UEFA_Championship_League(Common):
    """
    TR_ID: C61072
    NAME: [Archived after OX99] Verify 'Player Bets' tab (Premier League, La Liga, Serie A and UEFA Championship League)
    DESCRIPTION: This test case verifies 'Player Bets' tab on Event Details Page for Football (Premier League, La Liga, Serie A and UEFA Champions League)
    DESCRIPTION: Jira tickets:
    DESCRIPTION: [BMA-16090 (Player Bets: Add PB link to Event pages)] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-16090
    PRECONDITIONS: Oxygen application is loaded
    PRECONDITIONS: Make sure there are NOT started football events from the following leagues:
    PRECONDITIONS: - England -> Premier League (TST2, STG2, PROD TypeID =442),
    PRECONDITIONS: - Spanish -> La Liga (TST2, STG2, PROD TypeID = 971),
    PRECONDITIONS: - Italy -> Serie A (TST2 TypeID=732, PROD TypeID= 734),
    PRECONDITIONS: - UEFA Champions League (TST2, STG2 TypeID= 3022, PROD TypeID= 25230),
    PRECONDITIONS: - some other league.
    PRECONDITIONS: To trigger changes for events (suspension, start) use OB Backoffice:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/ti
    PRECONDITIONS: NOTE:
    PRECONDITIONS: All leagues will be configured in CMS -> Leagues
    PRECONDITIONS: Guide about leagues creation/configuration please find here: https://confluence.egalacoral.com/display/SPI/Guide+for+Bet+Receipt+banners+in+CMS
    """
    keep_browser_open = True

    def test_001_on_football_landing_page_tap_football_event_from_england___premier_league_with_available_goal_markets(self):
        """
        DESCRIPTION: On Football Landing page tap Football event from England - Premier League with available Goal Markets
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab position is defined by EDP-Markets response from CMS
        """
        pass

    def test_002_tap_player_bets_tab(self):
        """
        DESCRIPTION: Tap 'Player Bets' tab
        EXPECTED: - 'Player Bets' page is opened
        EXPECTED: - 'EPL' tab is selected by default on slide with list of players
        """
        pass

    def test_003_tap_back_button_on_player_bets_page(self):
        """
        DESCRIPTION: Tap Back button on 'Player Bets' page
        EXPECTED: - 'Event Details' page is opened for selected in step #2 event
        """
        pass

    def test_004_on_footbal_landing_page_tap_football_event_from_premier_league_without_available_goal_markets(self):
        """
        DESCRIPTION: On Footbal Landing page tap Football event from Premier League without available Goal Markets
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab position is defined by EDP-Markets response from CMS
        """
        pass

    def test_005_on_footbal_landing_page_tap_football_event_from_premier_league_without_available_goal_markets_and_main_market(self):
        """
        DESCRIPTION: On Footbal Landing page tap Football event from Premier League without available Goal Markets and Main Market
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab position is defined by EDP-Markets response from CMS
        """
        pass

    def test_006_repeat_steps_1_5_for_events_from_spain___spanish_la_liga(self):
        """
        DESCRIPTION: Repeat steps #1-5 for events from Spain - Spanish La Liga
        EXPECTED: - Results are the same
        EXPECTED: - In step #2 'LALIGA' tab is selected by default on slide with list of players
        """
        pass

    def test_007_repeat_steps_1_5_for_events_from_italy___italian_serie_a(self):
        """
        DESCRIPTION: Repeat steps #1-5 for events from Italy - Italian Serie A
        EXPECTED: - Results are the same
        EXPECTED: - In step #2 'SERIEA' tab is selected by default on slide with list of players
        """
        pass

    def test_008_repeat_steps_1_5_for_events_from_uefa_club_competiotions___uefa_champions_league(self):
        """
        DESCRIPTION: Repeat steps #1-5 for events from UEFA Club Competiotions - UEFA Champions League
        EXPECTED: - Results are the same
        EXPECTED: - In step #2 'UCL' tab is selected by default on slide with list of players
        """
        pass

    def test_009_on_footbal_landing_page_tap_football_event_not_from_premier_league_la_liga_serie_a_or_uefa_champions_league(self):
        """
        DESCRIPTION: On Footbal Landing page tap Football event not from Premier League, La Liga, Serie A or UEFA Champions League
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab is NOT shown
        """
        pass

    def test_010_on_football_landing_page_tap_football_event_from_any_of_these_leagues_premier_league_la_liga_serie_a_and_uefa_champions_league(self):
        """
        DESCRIPTION: On Football Landing page tap Football event from any of these leagues: Premier League, La Liga, Serie A and UEFA Champions League
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab is shown
        """
        pass

    def test_011_tap_player_bets_tab(self):
        """
        DESCRIPTION: Tap 'Player Bets' tab
        EXPECTED: 'Player Bets' page is opened
        """
        pass

    def test_012_in_ob_backoffice_make_event_from_step_10_suspended(self):
        """
        DESCRIPTION: In OB Backoffice make event from step #10 suspended
        EXPECTED: 
        """
        pass

    def test_013_tap_back_button_on_player_bets_page(self):
        """
        DESCRIPTION: Tap back button on 'Player Bets' page
        EXPECTED: Football Landing page is opened
        """
        pass

    def test_014_on_football_landing_page_tap_the_same_suspened_football_event(self):
        """
        DESCRIPTION: On Football Landing page tap the same suspened Football event
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab is shown
        """
        pass

    def test_015_on_footbal_landing_page_tap_football_event_from_any_of_these_leagues_premier_league_la_liga_serie_a_and_uefa_champions_league(self):
        """
        DESCRIPTION: On Footbal Landing page tap Football event from any of these leagues: Premier League, La Liga, Serie A and UEFA Champions League
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab is shown
        """
        pass

    def test_016_tap_player_bets_tab(self):
        """
        DESCRIPTION: Tap 'Player Bets' tab
        EXPECTED: 'Player Bets' page is opened
        """
        pass

    def test_017_in_ob_backoffice_start_event_check_bet_in_play_list_set_is_off___yes_set_correct_time(self):
        """
        DESCRIPTION: In OB Backoffice start event (check 'Bet In Play List', set 'Is OFF' - Yes, set correct time)
        EXPECTED: 
        """
        pass

    def test_018_tap_back_button_on_player_bets_page(self):
        """
        DESCRIPTION: Tap back button on 'Player Bets' page
        EXPECTED: Football Landing page is opened
        """
        pass

    def test_019_on_footbal_landing_page_tap_the_same_started_football_event(self):
        """
        DESCRIPTION: On Footbal Landing page tap the same started Football event
        EXPECTED: *  'Event Details' page is opened for selected event
        EXPECTED: *  'Player Bets' tab is NOT shown
        """
        pass
