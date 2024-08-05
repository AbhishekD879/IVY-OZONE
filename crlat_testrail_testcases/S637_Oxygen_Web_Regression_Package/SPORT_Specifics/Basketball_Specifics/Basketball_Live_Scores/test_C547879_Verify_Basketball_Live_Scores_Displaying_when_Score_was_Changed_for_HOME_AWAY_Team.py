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
class Test_C547879_Verify_Basketball_Live_Scores_Displaying_when_Score_was_Changed_for_HOME_AWAY_Team(Common):
    """
    TR_ID: C547879
    NAME: Verify Basketball Live Scores Displaying when Score was Changed for HOME/AWAY Team
    DESCRIPTION: This test case verifies Basketball Live Scores Displaying when Score was Changed for HOME/AWAY Team
    PRECONDITIONS: 1) In order to have a Scores Football event should be BIP event
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
        EXPECTED: * 'Live scores' are displayed
        EXPECTED: * 'LIVE' label is displayed
        """
        pass

    def test_005_trigger_the_following_situationvalue_is_changed_for_home_team_rolecodehome(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: 'value' is changed for HOME team (roleCode="HOME")
        EXPECTED: * Score immediately starts displaying new value for HOME team
        EXPECTED: * Score corresponds to the 'value' attribute from WS
        """
        pass

    def test_006_verify_ws_response_with_scbrd_type___all(self):
        """
        DESCRIPTION: Verify WS response with 'SCBRD' type -> ALL
        EXPECTED: The particular score is displayed in 'value' attribute for HOME team
        """
        pass

    def test_007_trigger_the_following_situationvalue_is_changed_for_away_team_rolecodeaway(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: 'value' is changed for AWAY team (roleCode="AWAY")
        EXPECTED: * Score immediately starts displaying new value for AWAY team
        EXPECTED: * Score corresponds to the 'value' attribute from WS
        """
        pass

    def test_008_verify_ws_response_with_scbrd_type___all(self):
        """
        DESCRIPTION: Verify WS response with 'SCBRD' type -> ALL
        EXPECTED: The particular score is displayed in 'value' attribute for AWAY team
        """
        pass

    def test_009_verify_score_change_for_homeaway_team_for_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify 'Score' change for HOME/AWAY team for sections in a collapsed state
        EXPECTED: If section is collapsed and 'Score' was changed, after expanding the section - updated 'Score' will be shown there
        """
        pass

    def test_010_verify_score_change_before_application_is_opened_for_homeaway_team(self):
        """
        DESCRIPTION: Verify 'Score' change before application is opened for HOME/AWAY team
        EXPECTED: If application was not started/opened and 'Score' was changed for HOME/AWAY team, after opening application and verified event - updated 'Score' will be shown there
        """
        pass

    def test_011_verify_score_change_when_details_page_of_verified_event_is_opened(self):
        """
        DESCRIPTION: Verify 'Score' change when Details Page of verified event is opened
        EXPECTED: After tapping 'Back' button updated 'Score' will be shown on Landing page
        """
        pass

    def test_012_repeat_steps_2_11_for_in_play___all_sports_page(self):
        """
        DESCRIPTION: Repeat steps 2-11 for 'In-Play' -> 'All Sports' page
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_2_11_for_in_play___basketball_page(self):
        """
        DESCRIPTION: Repeat steps 2-11 for 'In-Play' -> 'Basketball' page
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_2_11_for_featured_page(self):
        """
        DESCRIPTION: Repeat steps 2-11 for 'Featured' page
        EXPECTED: 
        """
        pass
