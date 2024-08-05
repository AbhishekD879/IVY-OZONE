import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C29405_Football_BIP_events_Live_Score_displaying_and_updating(Common):
    """
    TR_ID: C29405
    NAME: Football BIP events: Live Score displaying and updating
    DESCRIPTION: This test case verifies Live Score displaying and updating on Football BIP events on the Featured tab (mobile/tablet)/ Featured section (desktop).
    DESCRIPTION: NOTE: UAT assistance is needed in order to generate/update live scores for BIP event.
    DESCRIPTION: **Jira tickets:** BMA-3592
    PRECONDITIONS: 1) Make sure you have retrieved Football BIP events with an available score
    PRECONDITIONS: 2) In order to get event with Score use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **eventParticipantID** -  to verify team name and corresponding team score
    PRECONDITIONS: *   **periodCode**='ALL' & **description**="Total Duration of the game/match' - to look at the scorers for the full match
    PRECONDITIONS: *   **factCode**='SCORE' &** name**='Score of the match/game' - to see Match facts
    PRECONDITIONS: *   **'fact'** - to see a score for particular participant
    PRECONDITIONS: *   **'roleCode'** - HOME/AWAY to see home and away team.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_featured_tab_on_module_selector_ribbon(self):
        """
        DESCRIPTION: Go to Featured tab on Module Selector Ribbon
        EXPECTED: **For mobile/tablet:**
        EXPECTED: 'Featured' tab is opened
        EXPECTED: **For desktop:**
        EXPECTED: Module Ribbon Tabs are transformed into sections, displayed in the following order:
        EXPECTED: 1) Enhanced multiples carousel
        EXPECTED: 2) In-Play & Live Stream
        EXPECTED: 3) Next Races Carousel
        EXPECTED: 4) Featured area
        """
        pass

    def test_003_verify_football_event_with_scores_available(self):
        """
        DESCRIPTION: Verify Football event with scores available
        EXPECTED: Event is shown
        """
        pass

    def test_004_verify_score_displaying(self):
        """
        DESCRIPTION: Verify score displaying
        EXPECTED: Total score is shown between team names
        EXPECTED: Each score for particular team is shown near team name
        """
        pass

    def test_005_verify_score_correctness_for_each_team(self):
        """
        DESCRIPTION: Verify score correctness for each team
        EXPECTED: Score corresponds to the** 'fact'** attribute from the SS on periodCode="**ALL**" level
        """
        pass

    def test_006_verify_score_ordering(self):
        """
        DESCRIPTION: Verify score ordering
        EXPECTED: *   Score for the home team is shown near home team name (roleCode="HOME")
        EXPECTED: *   Score for the away team is shown near away team name (roleCode="AWAY")
        EXPECTED: Note: use **eventParticipantId **for matching Team and Score
        """
        pass

    def test_007_trigger_the_following_situationfactis_changed_for_home_team_rolecodehome(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: **'fact'** is changed for HOME team (roleCode="HOME")
        EXPECTED: Score is immediately start displaying new value for Home team
        """
        pass

    def test_008_trigger_the_following_situationfactis_changed_for_away_team_rolecodeaway(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: **'fact'** is changed for AWAY team (roleCode="AWAY")
        EXPECTED: Score is immediately start displaying new value for Away team
        """
        pass

    def test_009_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have LIVE Score available
        EXPECTED: Only 'LIVE' label is shown between team names instead of Score
        """
        pass
