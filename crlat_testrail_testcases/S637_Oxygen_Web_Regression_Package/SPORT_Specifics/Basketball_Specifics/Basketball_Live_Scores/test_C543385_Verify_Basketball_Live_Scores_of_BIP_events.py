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
class Test_C543385_Verify_Basketball_Live_Scores_of_BIP_events(Common):
    """
    TR_ID: C543385
    NAME: Verify Basketball Live Scores of BIP events
    DESCRIPTION: This test case verifies Basketball Live Score of BIP events
    PRECONDITIONS: 1) In order to have a Scores Basketball event should be BIP event
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: **participant_id** -  to verify team name and corresponding team score
    PRECONDITIONS: **period_code='ALL'** - to look at the scorers for the full match
    PRECONDITIONS: **period_code='QUARTER'** - to look at the scorers for the the specific time
    PRECONDITIONS: **period_index='1/2/3/4'** - to identify the particular 'QUARTER'
    PRECONDITIONS: **code='SCORE'**
    PRECONDITIONS: **value** - to see a score for the particular participant
    PRECONDITIONS: **role_code - 'TEAM_1'/'TEAM_2' or 'HOME'/'AWAY'** - to see home and away team
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: roleCode - 'TEAM_1'/'TEAM_2'
    PRECONDITIONS: PROD: roleCode - 'HOME/'AWAY'
    PRECONDITIONS: 3) Use the following link for verification SS commentary response http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: *NOTE:*
    PRECONDITIONS: 1) Use https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Amelco+Systems in order to generate live scores for BIP event.
    PRECONDITIONS: 2) If in the SiteServer commentary response the event has a typeFlagCode ="US" the scores should be displayed in reverse order i.e. away score on top and home score on bottom.
    PRECONDITIONS: 3) We received all score information, but no clock or period information. This means that the only period stored within OB is the "ALL" period, and so all 'values' are stored against this period.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_basketball_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Basketball' icon from the Sports Menu Ribbon
        EXPECTED: 'Basketball' landing page is opened
        """
        pass

    def test_003_tap_in_play_tab(self):
        """
        DESCRIPTION: Tap 'In-Play' tab
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_004_verify_basketball_event_with_scores_available(self):
        """
        DESCRIPTION: Verify 'Basketball' event with scores available
        EXPECTED: * Event is shown
        EXPECTED: * Live scores are displayed
        EXPECTED: * 'LIVE' label is displayed
        """
        pass

    def test_005_verify_score_displaying(self):
        """
        DESCRIPTION: Verify score displaying
        EXPECTED: Each score for particular team is shown at the same row as team's name near the Price/Odds button
        """
        pass

    def test_006_verify_score_correctness_for_each_team(self):
        """
        DESCRIPTION: Verify score correctness for each team
        EXPECTED: Score corresponds to the **'value'** attribute from WS
        """
        pass

    def test_007_verify_score_ordering_for_events(self):
        """
        DESCRIPTION: Verify score ordering for events
        EXPECTED: * 'Score' for the home team is shown at the same row as team name near the Price/Odds button (roleCode="HOME"/"TEAM_1")
        EXPECTED: * 'Score' for the away team s shown at the same row as team name near the Price/Odds button  (roleCode="AWAY"/"TEAM_2")
        """
        pass

    def test_008_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have 'Live Score' available
        EXPECTED: * 'LIVE' label is shown below the team names
        EXPECTED: * 'Live Scores' are NOT displayed
        """
        pass

    def test_009_verify_live_score_for_outright_events(self):
        """
        DESCRIPTION: Verify 'Live Score' for 'Outright' events
        EXPECTED: * 'Live Scores' are not shown for Outright events
        EXPECTED: * 'LIVE' label is displayed
        """
        pass

    def test_010_repeat_steps_2_9_for_in_play___all_sports_page(self):
        """
        DESCRIPTION: Repeat steps 2-9 for 'In-Play' -> 'All Sports' page
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_2_9_for_in_play___basketball_page(self):
        """
        DESCRIPTION: Repeat steps 2-9 for 'In-Play' -> 'Basketball' page
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_2_9_for_featured_page(self):
        """
        DESCRIPTION: Repeat steps 2-9 for 'Featured' page
        EXPECTED: 
        """
        pass
