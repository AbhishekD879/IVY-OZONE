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
class Test_C13035461_Verify_Handball_Score_correctness_for_teams_with_names_in_brackets_on_Event_Details_page(Common):
    """
    TR_ID: C13035461
    NAME: Verify Handball Score correctness for teams with names in brackets on Event Details page
    DESCRIPTION: This test case verifies Scoreboard for teams with names in brackets on Event Details page
    DESCRIPTION: AUTOTEST [C58612468]
    PRECONDITIONS: 1) In order to have a Scores Sports event should be BIP
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

    def test_002_go_tohandball_landing_page___in_play_taborin_play_page___handball_sportorhandball_page__in_play_module(self):
        """
        DESCRIPTION: Go to:
        DESCRIPTION: 'Handball' landing page -> 'In Play' tab
        DESCRIPTION: OR
        DESCRIPTION: In Play page -> Handball Sport
        DESCRIPTION: OR
        DESCRIPTION: Handball Page ->In Play Module
        EXPECTED: Page is opened
        EXPECTED: List of Handball events is loaded
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
        EXPECTED: |Team A (Test A)| ScoreA - ScoreB |Team B (Test B)|
        EXPECTED: e.g. |Auto (Women)| 5-7 |Auto (Men)|
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
        EXPECTED: No extra values are added to the scores
        """
        pass
