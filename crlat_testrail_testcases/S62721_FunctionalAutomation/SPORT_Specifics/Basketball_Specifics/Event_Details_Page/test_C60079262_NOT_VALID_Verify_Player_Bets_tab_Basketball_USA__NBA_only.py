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
class Test_C60079262_NOT_VALID_Verify_Player_Bets_tab_Basketball_USA__NBA_only(Common):
    """
    TR_ID: C60079262
    NAME: [NOT VALID] Verify 'Player Bets' tab (Basketball USA - NBA only)
    DESCRIPTION: This test case verifies 'Player Bets' tab on Event Details Page for Basketball (NBA only)
    DESCRIPTION: Jira tickets:
    DESCRIPTION: [BMA-16090 (Player Bets: Add PB link to Event pages)] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-16090
    PRECONDITIONS: Oxygen application is loaded
    PRECONDITIONS: Make sure there are not started Basketball USA events from the NBA league (TST2, STG2, PROD TypeID =136) and some other league.
    PRECONDITIONS: To trigger changes for events (suspension, start) use OB Backoffice:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/ti
    PRECONDITIONS: NOTE:
    PRECONDITIONS: All leagues are configured in CMS -> Leagues
    PRECONDITIONS: Guide about leagues creation/configuration please find here: https://confluence.egalacoral.com/display/SPI/Guide+for+Bet+Receipt+banners+in+CMS
    """
    keep_browser_open = True

    def test_001_on_basketball_landing_page_tap_football_event_from_usa___nba_with_available_main_markets(self):
        """
        DESCRIPTION: On Basketball Landing page tap Football event from USA - NBA with available Main Markets
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab is shown after 'Main Markets' tab
        """
        pass

    def test_002_tap_player_bets_tab(self):
        """
        DESCRIPTION: Tap 'Player Bets' tab
        EXPECTED: - 'Player Bets' page is opened
        EXPECTED: - 'NBA' tab is selected by default on slide with list of players
        """
        pass

    def test_003_tap_back_button_on_player_bets_page(self):
        """
        DESCRIPTION: Tap Back button on 'Player Bets' page
        EXPECTED: - 'Event Details' page is opened for selected in step #2 event
        """
        pass

    def test_004_on_basketball_landing_page_tap_football_event_from_usa___nba_without_available_main_markets(self):
        """
        DESCRIPTION: On Basketball Landing page tap Football event from USA - NBA without available Main Markets
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab is shown after 'All Markets' tab
        """
        pass

    def test_005_on_basketball_landing_page_tap_event_not_from_usa___nba(self):
        """
        DESCRIPTION: On Basketball Landing page tap event not from USA - NBA
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab is NOT shown
        """
        pass

    def test_006_on_basketball_landing_page_tap_event_from_usa___nba(self):
        """
        DESCRIPTION: On Basketball Landing page tap event from USA - NBA
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab is shown
        """
        pass

    def test_007_tap_player_bets_tab(self):
        """
        DESCRIPTION: Tap 'Player Bets' tab
        EXPECTED: 'Player Bets' page is opened
        """
        pass

    def test_008_in_ob_backoffice_make_event_from_step_6_suspended(self):
        """
        DESCRIPTION: In OB Backoffice make event from step #6 suspended
        EXPECTED: 
        """
        pass

    def test_009_tab_back_button_on_player_bets_page(self):
        """
        DESCRIPTION: Tab back button on 'Player Bets' page
        EXPECTED: Basketball Landing page is opened
        """
        pass

    def test_010_on_basketball_landing_page_tap_the_same_suspende_event_from_usa___nba(self):
        """
        DESCRIPTION: On Basketball Landing page tap the same suspende event from USA - NBA
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab is shown
        """
        pass

    def test_011_on_basketball_landing_page_tap_event_from_usa___nba(self):
        """
        DESCRIPTION: On Basketball Landing page tap event from USA - NBA
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab is shown
        """
        pass

    def test_012_tap_player_bets_tab(self):
        """
        DESCRIPTION: Tap 'Player Bets' tab
        EXPECTED: 'Player Bets' page is opened
        """
        pass

    def test_013_in_ob_backoffice_start_event_check_bet_in_play_list_set_is_off___yes_set_correct_time(self):
        """
        DESCRIPTION: In OB Backoffice start event (check 'Bet In Play List', set 'Is OFF' - Yes, set correct time)
        EXPECTED: 
        """
        pass

    def test_014_tab_back_button_on_player_bets_page(self):
        """
        DESCRIPTION: Tab back button on 'Player Bets' page
        EXPECTED: Basketball Landing page is opened
        """
        pass

    def test_015_on_footbal_landing_page_tap_the_same_started_football_event(self):
        """
        DESCRIPTION: On Footbal Landing page tap the same started Football event
        EXPECTED: - 'Event Details' page is opened for selected event
        EXPECTED: - 'Player Bets' tab is NOT shown
        """
        pass
