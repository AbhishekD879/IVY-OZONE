import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C819987_Verify_Game_Score_changing_on_Badminton_Event_Details_page(Common):
    """
    TR_ID: C819987
    NAME: Verify Game Score changing on Badminton Event Details page
    DESCRIPTION: This test case verifies Game Score changing on Event Details page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1) In order to have a Scores Badminton event should be BIP
    PRECONDITIONS: 2) In order to get commentary for event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *    **eventParticipant id** - to verify player name and corresponding player score
    PRECONDITIONS: *    **periodCode="ALL"** on **periodIndex=X** - to verify Game scrore correctness for each team
    PRECONDITIONS: *    **periodCode="SET"** on **periodIndex=X** - to verify Points scrore correctness for each team
    PRECONDITIONS: *    **fact** - to verify Game/Points Score for particular team on **factCode="SCORE"** level
    PRECONDITIONS: *    **roleCode="PLAYER_1"** / **roleCode="PLAYER_2"** - to determine HOME and AWAY teams
    PRECONDITIONS: 3) [How to generate Live Scores for Badminton][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+Updates+for+Volleyball%2C+Beach+Volleyball+and+Badminton
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_badminton_landing_page___in_play_tab_for_desktopnote_for_mobile_in_play_events_are_displayed_in_in_play_module_at_the_top_of_the_page_if_available(self):
        """
        DESCRIPTION: Go to 'Badminton' landing page -> 'In Play' tab (for Desktop)
        DESCRIPTION: Note: for mobile in-play events are displayed in 'In-Play' module at the top of the page (if available)
        EXPECTED: * 'In-Play' tab is opened (desktop)
        EXPECTED: * In-Play' module is displayed (mobile)
        """
        pass

    def test_003_choose_badminton_event_with_live_scores_available_and_go_to_event_details_page(self):
        """
        DESCRIPTION: Choose Badminton event with Live Scores available and go to Event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_change_game_score_for_home_team(self):
        """
        DESCRIPTION: Change Game Score for Home team
        EXPECTED: * Game Score immediately starts displaying new value for Home player
        EXPECTED: * Update is received as push notification
        EXPECTED: * Game Score corresponds to **fact** attribute on **periodCode="ALL"** level where **roleCode="PLAYER_1"** from SS comentary response
        EXPECTED: * Point Score is updated automatically as new Game is started
        EXPECTED: * Point Score corresponds to **fact** attribute on **periodCode="SET"** level where **roleCode="PLAYER_1"** from SS comentary response
        EXPECTED: **NOTE** use **eventParticipant id** parameter to match particular team and Game Score
        """
        pass

    def test_005_change_game_score_for_away_team(self):
        """
        DESCRIPTION: Change Game Score for Away team
        EXPECTED: * Game Score immediately starts displaying new value for Away player
        EXPECTED: * Update is received as push notification
        EXPECTED: * Game Score corresponds to **fact** attribute on **periodCode="ALL"** level where **roleCode="PLAYER_2"** from SS comentary response
        EXPECTED: * Point score is updated automatically as new Game is started
        EXPECTED: * Point Score corresponds to **fact** attribute on **periodCode="SET"** level where **roleCode="PLAYER_2"** from SS comentary response
        EXPECTED: **NOTE** use **eventParticipant id** parameter to match particular team and Game Score
        """
        pass

    def test_006_verify_game_score_animation(self):
        """
        DESCRIPTION: Verify Game Score animation
        EXPECTED: * New Set Score slides and starts displaying new value immediately under 'G' label
        """
        pass
