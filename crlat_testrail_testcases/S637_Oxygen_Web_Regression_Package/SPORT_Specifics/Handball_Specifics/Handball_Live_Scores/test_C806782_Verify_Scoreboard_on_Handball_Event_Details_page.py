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
class Test_C806782_Verify_Scoreboard_on_Handball_Event_Details_page(Common):
    """
    TR_ID: C806782
    NAME: Verify Scoreboard on Handball Event Details page
    DESCRIPTION: This test case verifies Scoreboard displaying on Event Details page for Handball sport.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1) In order to have a Scores Handball event should be BIP
    PRECONDITIONS: 2) Link for creating and configuration of events in BetGenius:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Bet+Genius
    PRECONDITIONS: 3) In order to get commentary for event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *    **name** - to see event name that contains Points
    PRECONDITIONS: 4) Open Development tool ->Network-> XHR
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_handball_landing_page___in_play_tab(self):
        """
        DESCRIPTION: Go to 'Handball' landing page -> 'In Play' tab
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_003_choose_handball_event_with_live_scores_available_and_go_to_event_details_page(self):
        """
        DESCRIPTION: Choose Handball event with Live Scores available and go to Event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_verify_score_displaying(self):
        """
        DESCRIPTION: Verify Score displaying
        EXPECTED: * Game and Set Scores are displayed between team names in the next format:
        EXPECTED: |Team A| ScoreA - ScoreB |Team B|
        EXPECTED: e.g. Yong Kong 1 - 13 Matsuda
        EXPECTED: **For mobile:**
        EXPECTED: Event name and Scores are left aligned and are transferred to the second line if there is not enough space
        EXPECTED: **For desktop:**
        EXPECTED: Event name and Scores are left aligned and are truncated  in case of long name
        """
        pass

    def test_005_verify_score_correctness(self):
        """
        DESCRIPTION: Verify Score correctness
        EXPECTED: Scores correspond to values in event.name received in Response from SS for GET Request EventToOutcomeForEvent
        """
        pass

    def test_006_verify_scores_animation_when_scores_are_changed_for_home_team(self):
        """
        DESCRIPTION: Verify Scores animation when scores are changed for HOME Team
        EXPECTED: * New Score slides and starts displaying new value immediately next to HOME Team
        EXPECTED: * Updated Score value is received in 'Push' notification
        """
        pass

    def test_007_verify_scores_animation_when_scores_are_changed_for_away_team(self):
        """
        DESCRIPTION: Verify Scores animation when scores are changed for AWAY Team
        EXPECTED: * New Score slides and starts displaying new value immediately next to AWAY Team
        EXPECTED: * Updated Score value is received in 'Push' notification
        """
        pass

    def test_008_verify_event_date_dispaying(self):
        """
        DESCRIPTION: Verify Event Date dispaying
        EXPECTED: **For mobile:**
        EXPECTED: * Date is displayed in the next format below Event Name:
        EXPECTED: <Day>, DD-MM-YY, HH:MM AM/PM
        EXPECTED: e.g. Wednesday, 8-Feb-17, 9:00AM
        EXPECTED: * Date is received in **event.startTime** in Response from SS for GET Request EventToOutcomeForEvent
        EXPECTED: **For desktop:**
        EXPECTED: Date is not displayed within scoreboard panel
        """
        pass

    def test_009_verify_event_which_doesnt_have_live_scores_available(self):
        """
        DESCRIPTION: Verify event which doesn't have Live Scores available
        EXPECTED: **For mobile:**
        EXPECTED: * Scoreboard is not shown
        EXPECTED: * Event name and date is displayed
        EXPECTED: * 'LIVE' label is shown from right side of the date
        EXPECTED: **For desktop:**
        EXPECTED: * Scoreboard panel is not shown at all
        EXPECTED: * Event name, date and 'LIVE' label are shown in the header (i.e. where 'back' button is)
        """
        pass
