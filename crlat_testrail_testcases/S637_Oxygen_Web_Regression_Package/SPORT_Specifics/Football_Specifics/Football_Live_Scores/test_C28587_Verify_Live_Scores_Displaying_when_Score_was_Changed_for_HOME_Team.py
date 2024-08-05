import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C28587_Verify_Live_Scores_Displaying_when_Score_was_Changed_for_HOME_Team(Common):
    """
    TR_ID: C28587
    NAME: Verify Live Scores Displaying when Score was Changed for HOME Team
    DESCRIPTION: Thos test case verifies live scores displaying when score was changed for HOME team.
    DESCRIPTION: NOTE: Use https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Amelco+Systems in order to generate live scores for BIP event.
    PRECONDITIONS: 1) In order to have a Scores Football event should be BIP event
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **participant_id** -  to verify team name and corresponding team score
    PRECONDITIONS: *   **period_code**='ALL'** - to look at the scorers for the full match
    PRECONDITIONS: *   **period_code**=''FIRST_HALF/SECOND_HALF/EXTRA_TIME_FIRST_HALF/EXTRA_TIME_HALF_TIME/EXTRA_TIME_SECOND_HALF'** - to look at the scorers for the specific time
    PRECONDITIONS: *   **code**='SCORE'**
    PRECONDITIONS: *   **value** - to see a score for particular participant
    PRECONDITIONS: *   **role_code**' - HOME/AWAY to see home and away team
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: 'roleCode' - TEAM_1/TEAM_2
    PRECONDITIONS: PROD: 'roleCode' - HOME/AWAY
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_football_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        EXPECTED: 'Football' landing page is opened
        """
        pass

    def test_003_tap_in_play_tab(self):
        """
        DESCRIPTION: Tap 'In-Play' tab
        EXPECTED: 'In Play' tab is opened
        """
        pass

    def test_004_verify_football_event_with_score_available(self):
        """
        DESCRIPTION: Verify Football event with score available
        EXPECTED: Score is shown between team names
        """
        pass

    def test_005_trigger_the_following_situationvalue_is_changed_for_home_team_rolecodehome(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: **'value'** is changed for HOME team (roleCode="HOME")
        EXPECTED: Score immediately starts displaying new value for Home team
        """
        pass

    def test_006_find_event_from_step_4_and_repeat_step_5(self):
        """
        DESCRIPTION: Find event from step №4 and repeat step №5
        EXPECTED: 
        """
        pass

    def test_007_tap_in_play_icon_from_the_sports_menu_ribbonselect_watch_live_iconrepeat_steps_4_5(self):
        """
        DESCRIPTION: Tap 'In-play' icon from the Sports Menu Ribbon
        DESCRIPTION: Select 'Watch Live' icon
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 'In-Play' tab is shown and 'Watch live' is selected
        EXPECTED: Score immediately starts displaying new value for Home team
        """
        pass

    def test_008_tap_football_icon_from_the_sports_menu_ribbon_on_in_play_pagerepeat_steps_4_5(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon on 'In-Play' page
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 'Football' page is opened
        EXPECTED: Score immediately starts displaying new value for Home team
        """
        pass

    def test_009_tap_in_play_tab_on_the_homepagerepeat_steps_4_5(self):
        """
        DESCRIPTION: Tap 'In-Play' tab on the Homepage
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 'In-Play' tab is opened
        EXPECTED: Score immediately starts displaying new value for Home team
        """
        pass

    def test_010_tap_live_stream_tab_from_the_homepagerepeat_steps_4_5(self):
        """
        DESCRIPTION: Tap 'Live Stream' tab from the Homepage
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: 'Live Stream' tab is opened
        EXPECTED: Score immediately starts displaying new value for Home team
        """
        pass

    def test_011_for_mobiletablethome_page__featured_tab_verify_that_scores_for_the_event_on_in_play_modulehighlight_carouselfeatured_module_created_by_type_idevent_idrepeat_steps_4_5(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Home page > 'Featured' tab :
        DESCRIPTION: Verify that scores for the event on :
        DESCRIPTION: In-play module
        DESCRIPTION: Highlight carousel
        DESCRIPTION: Featured module (created by Type_id/Event_id)
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: Score immediately starts displaying new value for Home team
        """
        pass

    def test_012_go_to_edp_for_the_appropriate_eventrepeat_steps_4_5(self):
        """
        DESCRIPTION: Go to EDP for the appropriate event
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: Score immediately starts displaying new value for Home team
        """
        pass

    def test_013_place_bet_on_appropriate_eventnavigate_to_my_bets_open_betscashout_and_settled_bets_tabsrepeat_steps_4_5(self):
        """
        DESCRIPTION: Place bet on appropriate event
        DESCRIPTION: Navigate to My bets >Open bets/Cashout and Settled bets tabs
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: Score immediately starts displaying new value for Home team
        """
        pass

    def test_014_verify_score_change_for_home_team_for_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify Score change for HOME team for sections in a collapsed state
        EXPECTED: If section is collapsed and Score was changed, after expanding the section - updated Score will be shown there
        """
        pass

    def test_015_verify_score_change_before_application_is_opened(self):
        """
        DESCRIPTION: Verify Score change before application is opened
        EXPECTED: If application was not started/opened and Score was changed for HOME team, after opening application and verified event - updated Score will be shown there
        """
        pass

    def test_016_verify_score_change_when_details_page_of_verified_event_is_opened(self):
        """
        DESCRIPTION: Verify Score change when Details Page of verified event is opened
        EXPECTED: After tapping Back button updated Score will be shown on Landing page
        """
        pass
