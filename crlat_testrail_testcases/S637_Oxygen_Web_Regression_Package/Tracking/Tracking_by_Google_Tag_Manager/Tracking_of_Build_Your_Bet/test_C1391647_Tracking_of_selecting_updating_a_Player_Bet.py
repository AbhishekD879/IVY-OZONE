import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1391647_Tracking_of_selecting_updating_a_Player_Bet(Common):
    """
    TR_ID: C1391647
    NAME: Tracking of selecting/updating a Player Bet
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of selecting a Player Bet and Statistic from the 'Player Bets' accordion/updating Player Bet and Statistic, Statistic number within the Bet Dashboard
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Browser console should be opened
    PRECONDITIONS: 3. Navigate to Football Landing page
    PRECONDITIONS: 4. Go to the Event details page with the BYB (Leagues with available BYB are marked with BYB icon on accordion) > 'Build Your Bet' tab
    """
    keep_browser_open = True

    def test_001_choose_a_player_statistic_and_statistic_number_from_the_player_bets_accordion(self):
        """
        DESCRIPTION: Choose a player, statistic and statistic number from the 'Player Bets' accordion
        EXPECTED: Player, statistic and statistic number are chosen
        """
        pass

    def test_002_click_on_add_to_bet_button(self):
        """
        DESCRIPTION: Click on 'Add to Bet' button
        EXPECTED: The selections are added to BYB Dashboard
        """
        pass

    def test_003_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'build bet',
        EXPECTED: 'eventLabel' : 'select player bet',
        EXPECTED: 'playerName' : '<< PLAYER NAME >>'
        EXPECTED: 'playerStat' : '<< STATISTIC NAME >>',
        EXPECTED: 'playerStatNum' : '<< STATISTIC NUMBER >>' }
        EXPECTED: )
        """
        pass

    def test_004_edit_added_player_bet_change_player_name_or_statistic_within_the_byb_dashboard__click_on_done_button(self):
        """
        DESCRIPTION: Edit added Player Bet (change player name or statistic) within the BYB Dashboard > Click on 'Done' button
        EXPECTED: Player name and Statistic are changed
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'build bet',
        EXPECTED: 'eventLabel' : 'select player bet',
        EXPECTED: 'playerName' : '<< PLAYER NAME >>'
        EXPECTED: 'playerStat' : '<< STATISTIC NAME >>',
        EXPECTED: 'playerStatNum' : '<< STATISTIC NUMBER >>' }
        EXPECTED: )
        """
        pass

    def test_006_change_the_statistic_number_within_the_byb_dashboard(self):
        """
        DESCRIPTION: Change the statistic number within the BYB Dashboard
        EXPECTED: The statistic number is changed
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: he following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'build bet',
        EXPECTED: 'eventLabel' : 'update statistic',
        EXPECTED: 'playerName' : '<< PLAYER NAME >>'
        EXPECTED: 'playerStat' : '<< STATISTIC NAME >>',
        EXPECTED: 'playerStatNum' : '<< STATISTIC NUMBER >>' }
        EXPECTED: )
        """
        pass
