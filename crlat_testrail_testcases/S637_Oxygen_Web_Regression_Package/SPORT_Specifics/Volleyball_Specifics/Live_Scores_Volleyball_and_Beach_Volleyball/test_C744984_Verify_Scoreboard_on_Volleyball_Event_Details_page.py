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
class Test_C744984_Verify_Scoreboard_on_Volleyball_Event_Details_page(Common):
    """
    TR_ID: C744984
    NAME: Verify Scoreboard on Volleyball Event Details page
    DESCRIPTION: This test case verifies Scoreboard displaying on Event Details page for Volleyball and Beach Volleyball sports.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1) In order to have a Scores Volleyball/Beach Volleyball event should be BIP
    PRECONDITIONS: 2) Link for creating and configuration of events in BetGenius:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Bet+Genius
    PRECONDITIONS: 3) In order to get commentary for event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *    **name** - to see event name that contains Game and Set Scores
    PRECONDITIONS: 4) Open Development tool ->Network-> XHR
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_volleyball_landing_page___in_play_tab_for_desktop_in_play_module_on_matches_tab_for_mobile(self):
        """
        DESCRIPTION: Go to 'Volleyball' landing page -> 'In Play' tab for Desktop (In-Play module on Matches tab for Mobile)
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_003_choose_volleyball_event_with_live_scores_available_and_go_to_event_details_page(self):
        """
        DESCRIPTION: Choose Volleyball event with Live Scores available and go to Event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_verify_set_and_game_scores_displaying(self):
        """
        DESCRIPTION: Verify Set and Game Scores displaying
        EXPECTED: * Game and Set Scores are displayed between team names in the next format:
        EXPECTED: |Team A| (SetsA) GameScoreA - GameScoreB (SetsB) |Team B|
        EXPECTED: e.g. Yong Kong (2) 1 - 13 (2) Matsuda
        EXPECTED: * 'S' label is displayed and located above set value for each team
        EXPECTED: * 'P' label is displayed and located above scores value for each team
        EXPECTED: **For mobile:**
        EXPECTED: Event name, Game and Set Scores are left aligned and are transferred to the second line if there is not enough space
        EXPECTED: **For desktop:**
        EXPECTED: Event name, Game and Set Scores are left aligned and are truncated  in case of long name
        """
        pass

    def test_005_verify_set_and_point_correctness(self):
        """
        DESCRIPTION: Verify Set and Point correctness
        EXPECTED: Sets and Points correspond to values in **event.name** received in Response from SS for GET Request EventToOutcomeForEvent
        """
        pass

    def test_006_verify_points_animation_when_points_are_changed_for_home_team(self):
        """
        DESCRIPTION: Verify Points animation when points are changed for HOME Team
        EXPECTED: * New Point slides from Home Team side and starts displaying new value immediately under 'P' label
        EXPECTED: * Point value is received in 'Push' notification
        """
        pass

    def test_007_verify_points_animation_when_points_are_changed_for_away_team(self):
        """
        DESCRIPTION: Verify Points animation when points are changed for AWAY Team
        EXPECTED: * New Point slides from AWAY Team side and starts displaying new value immediately under 'P' label
        EXPECTED: * Point value is received in **Push** notification
        """
        pass

    def test_008_verify_new_set_appearing_animation_when_home_team_scores(self):
        """
        DESCRIPTION: Verify new Set appearing animation when HOME team scores
        EXPECTED: * New Set and Point slides and starts displaying new value immediately under 'S' label and 'P' label
        EXPECTED: * Set and Point value is received in **Push** notification
        """
        pass

    def test_009_verify_new_set_appearing_animation_when_away_team_scores(self):
        """
        DESCRIPTION: Verify new Set appearing animation when AWAY team scores
        EXPECTED: * New Set and Point slides and starts displaying new value immediately under 'S' label and 'P' label
        EXPECTED: * Set and Point value is received in **Push** notification
        """
        pass

    def test_010_verify_event_date_displaying(self):
        """
        DESCRIPTION: Verify Event Date displaying
        EXPECTED: **For mobile:**
        EXPECTED: * Date is displayed in the next format below Event Name:
        EXPECTED: <Day>, DD-MM-YY, HH:MM AM/PM
        EXPECTED: e.g. Wednesday, 8-Feb-17, 9:00AM
        EXPECTED: * Date is received in **event.startTime** in Response from SS for GET Request EventToOutcomeForEvent
        EXPECTED: **For desktop:**
        EXPECTED: Date is not displayed within scoreboard panel
        """
        pass

    def test_011_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have LIVE Score available
        EXPECTED: **For mobile:**
        EXPECTED: * Scoreboard is not shown
        EXPECTED: * Event name and date is displayed
        EXPECTED: * 'LIVE' label is shown from right side of the date
        EXPECTED: **For desktop:**
        EXPECTED: * Scoreboard panel is not shown at all
        EXPECTED: * Event name, date and 'LIVE' label are shown in the header (i.e. where 'back' button is)
        """
        pass

    def test_012_repeat_steps_2_7_for_beach_volleyball_sport(self):
        """
        DESCRIPTION: Repeat steps #2-7 for Beach Volleyball sport
        EXPECTED: 
        """
        pass
