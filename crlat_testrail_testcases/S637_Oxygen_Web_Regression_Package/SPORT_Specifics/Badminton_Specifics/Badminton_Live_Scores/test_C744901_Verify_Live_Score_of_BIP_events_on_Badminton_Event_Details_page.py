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
class Test_C744901_Verify_Live_Score_of_BIP_events_on_Badminton_Event_Details_page(Common):
    """
    TR_ID: C744901
    NAME: Verify Live Score of BIP events on Badminton Event Details page
    DESCRIPTION: This test case verifies Live Score of BIP events on Event Details page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1) In order to have a Scores Badminton event should be BIP
    PRECONDITIONS: 2) In order to get commentary for event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *    **eventParticipant id** - to verify player name and corresponding player score
    PRECONDITIONS: *    **periodCode="SET"** on **periodIndex=X** - to verify Points score correctness for each team
    PRECONDITIONS: *    **periodCode="ALL"** on **periodIndex=X** - to verify Game score correctness for each team
    PRECONDITIONS: *    **fact** - to verify Game/Points Score for particular team on **factCode="SCORE"** level
    PRECONDITIONS: *    **startTime** - to check date correctness
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

    def test_004_verify_game_and_points_scores_displaying(self):
        """
        DESCRIPTION: Verify Game and Points Scores displaying
        EXPECTED: * Game and Set Scores are displayed between team names in the next format:
        EXPECTED: |Team A| (GameScoreA) PointsScoreA - PointsScoreB (GameScoreB) |Team B|
        EXPECTED: e.g. Yong Kong (2) 1 - 13 (2) Matsuda
        EXPECTED: * 'G' label is displayed and located above games value for each team
        EXPECTED: * 'P' label is displayed and located above points value for each team
        EXPECTED: **For mobile:**
        EXPECTED: Event name, Game and Points Scores are left aligned and are transferred to the second line if there is not enough space
        EXPECTED: **For desktop:**
        EXPECTED: Event name, Game and Points Scores are left aligned and are
        EXPECTED: truncated  in case of long name
        """
        pass

    def test_005_verify_points_score_correctness_for_each_team(self):
        """
        DESCRIPTION: Verify Points Score correctness for each team
        EXPECTED: Points Score corresponds to **fact** attribute on **periodCode="SET"** level and the highest **periodIndex** value from SS commentary response
        EXPECTED: **NOTE** use **eventParticipant id** parameter to match particular team and Points Score
        """
        pass

    def test_006_verify_game_score_correctness_for_each_team(self):
        """
        DESCRIPTION: Verify Game Score correctness for each team
        EXPECTED: Game Score corresponds to **fact** attribute on **periodCode="ALL"** level from SS commentary response
        EXPECTED: **NOTE** use **eventParticipant id** parameter to match particular team and Game Score
        """
        pass

    def test_007_verify_event_date(self):
        """
        DESCRIPTION: Verify Event Date
        EXPECTED: **For mobile:**
        EXPECTED: * Date is displayed in the next format below Event Name:
        EXPECTED: <Day>, DD-MM-YY, HH:MM AM/PM
        EXPECTED: e.g. Wednesday, 8-Feb-17, 9:00AM
        EXPECTED: * Date is received in **event.startTime** in Response from SS for GET Request EventToOutcomeForEvent
        EXPECTED: **For desktop:**
        EXPECTED: Date is not displayed within scoreboard panel
        """
        pass

    def test_008_verify_event_which_doesnt_have_live_score_available(self):
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

    def test_009_verify_game_and_points_scores_for_outright_event(self):
        """
        DESCRIPTION: Verify Game and Points Scores for Outright event
        EXPECTED: * Scores are not shown for Outright events
        EXPECTED: * Only 'LIVE' label is shown next to date
        """
        pass
