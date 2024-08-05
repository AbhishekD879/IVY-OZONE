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
class Test_C1747391_Verify_score_updates_for_Primary_Markets(Common):
    """
    TR_ID: C1747391
    NAME: Verify score updates for Primary Markets
    DESCRIPTION: This test case verifies displaying of scores for all Primary Markets
    DESCRIPTION: NOTE:
    DESCRIPTION: - Use https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Amelco+Systems in order to create BIP event and generate live scores.
    DESCRIPTION: - List of Primary markets:
    DESCRIPTION: 1 - Match Betting (market template: |Match Betting|)
    DESCRIPTION: 2 - Match Result (market template: |Match Betting|)
    DESCRIPTION: 3 - Extra-Time Result (market template: |Extra-Time Result|)
    DESCRIPTION: 4 - Penalty Shoot-Out Winner (market template: |Penalty Shoot-Out Winner|)
    DESCRIPTION: 5 - To Qualify (market template: |To Qualify|)
    DESCRIPTION: 6 - To Lift the trophy (market template: |To Qualify|)
    DESCRIPTION: 7 - To finish 3rd (market template: |To Qualify|)
    DESCRIPTION: 8 - To reach the final (market template: |To Qualify|)
    PRECONDITIONS: 1) In order to have Football event with scores, event should be BIP
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: participant_id -  to verify team name and corresponding team score
    PRECONDITIONS: period_code='ALL'** - to look at the scorers for the full match
    PRECONDITIONS: period_code='FIRST_HALF/SECOND_HALF/EXTRA_TIME_FIRST_HALF/EXTRA_TIME_HALF_TIME/EXTRA_TIME_SECOND_HALF** - to look at the scorers for the specific time
    PRECONDITIONS: code='SCORE'**
    PRECONDITIONS: value - to see a score for particular participant
    PRECONDITIONS: role_code' - HOME/AWAY to see home and away team
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: 'roleCode' - TEAM_1/TEAM_2
    PRECONDITIONS: PROD: 'roleCode' - HOME/AWAY
    PRECONDITIONS: 3) BIP events with primary markets are configured through Amelco
    PRECONDITIONS: 4) Featured tab is configured in CMS with corresponding Football BIP event(s)
    PRECONDITIONS: 5) App is loaded & Featured tab is opened
    """
    keep_browser_open = True

    def test_001_find_bip_football_event_from_preconditions(self):
        """
        DESCRIPTION: Find BIP Football event (from Preconditions)
        EXPECTED: BIP Football event is available
        """
        pass

    def test_002__in_amelco_inplay__commentary_feed_select_first_halfsecond_half_from_the_drop_down__trigger_score_update_in_app_verify_corresponding_bip_football_event(self):
        """
        DESCRIPTION: * In Amelco (Inplay > Commentary feed): Select First Half/Second Half from the drop down > trigger score update
        DESCRIPTION: * In app: Verify corresponding BIP Football event
        EXPECTED: Score starts displaying new value for Home/Away team
        """
        pass

    def test_003__in_amelco_inplay_inplay__commentary_feed_select_extra_time_first_half_from_the_drop_down__trigger_score_update_in_app_refresh_the_page__verify_scores_updates_for_corresponding_bip_football_event(self):
        """
        DESCRIPTION: * In Amelco (Inplay): (Inplay > Commentary feed): Select Extra-Time First Half from the drop down > trigger score update
        DESCRIPTION: * In app: Refresh the page & verify scores updates for corresponding BIP Football event
        EXPECTED: * Same event with the next active and available Primary Market appears after refresh (e.g. Extra-Time Result (market template: |Extra-Time Result|)
        EXPECTED: * Scores remain displayed for the next available Primary Market
        EXPECTED: * New scores are added to the previous ones for Home/Away team
        """
        pass

    def test_004__in_amelco_inplay_inplay__commentary_feed_select_extra_time_half_time_from_the_drop_down__trigger_score_update_in_app_verify_scores_updates_for_corresponding_bip_football_event(self):
        """
        DESCRIPTION: * In Amelco (Inplay): (Inplay > Commentary feed): Select Extra-Time Half Time from the drop down > trigger score update
        DESCRIPTION: * In app: Verify scores updates for corresponding BIP Football event
        EXPECTED: * Scores remain displayed for the next available Primary Market
        EXPECTED: * New scores are added to the previous ones for Home/Away team
        """
        pass

    def test_005__in_amelco_inplay_inplay__commentary_feed_select_extra_time_second_half_from_the_drop_down__trigger_score_update_in_app_verify_scores_updates_for_corresponding_bip_football_event(self):
        """
        DESCRIPTION: * In Amelco (Inplay): (Inplay > Commentary feed): Select Extra-Time Second Half from the drop down > trigger score update
        DESCRIPTION: * In app: Verify scores updates for corresponding BIP Football event
        EXPECTED: * Scores remain displayed for the next available Primary Market
        EXPECTED: * New scores are added to the previous ones for Home/Away team
        """
        pass

    def test_006_verify_score_change_for_for_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify Score change for for sections in a collapsed state
        EXPECTED: Scores are updated after expanding a section
        """
        pass

    def test_007_repeat_steps_2_6_for_home__in_play__in_play_all_sports_pages(self):
        """
        DESCRIPTION: Repeat steps 2-6 for Home > In Play & In Play All Sports pages
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_6_for_in_play__football__football__in_play_pages(self):
        """
        DESCRIPTION: Repeat steps 2-6 for In Play > Football & Football > In Play pages
        EXPECTED: 
        """
        pass
