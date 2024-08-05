import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732067_Verify_view_and_data_of_previous_game_cards(Common):
    """
    TR_ID: C57732067
    NAME: Verify view and data of previous game cards
    DESCRIPTION: This test case verifies view and data of previous game cards
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. The user is played previous quizzes few times
    """
    keep_browser_open = True

    def test_001_tap_on_correct_4_link(self):
        """
        DESCRIPTION: Tap on Correct 4 link
        EXPECTED: - User navigated to the end page (Results page) and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        pass

    def test_002_tap_on_previous_tab(self):
        """
        DESCRIPTION: Tap on Previous Tab
        EXPECTED: Previous Tab succssefuly opened and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a8847a29b543109bd
        EXPECTED: Collapsed view of the three most recent games as a 'card' with summary details:
        EXPECTED: - Shirts (if available in cms)
        EXPECTED: - Event details : e.g Champions League ;  Sep 5 ; Emirates Stadium
        EXPECTED: - Game details and scores : e.g. teams with the scores
        EXPECTED: - Won/ Lost indicator in corner (Red, amber, green with icons or £ prize)
        EXPECTED: - Clickable text to View more information for a specific game
        EXPECTED: - Clickable text to Show more games
        """
        pass

    def test_003_tap_on_view_game_summary_for_game_card(self):
        """
        DESCRIPTION: Tap on 'View game summary' for game card
        EXPECTED: Selected game card will expand to show more details
        EXPECTED: (using the same info as on Latest tab) and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a2ffb679bba35fce2
        EXPECTED: Expanded game card items:
        EXPECTED: - Header (Champions league | 5 Sept )
        EXPECTED: - Stadium label in design is not in the scope
        EXPECTED: - Shirts (if available)
        EXPECTED: - Questions & Answers
        EXPECTED: - Won/ Lost indicator (Green & red)
        EXPECTED: - Prize indicator in the corner of answer card
        EXPECTED: - If user WON 1st prize: Show amount £ in green
        EXPECTED: - If user WON 2nd prize: Show amount £ in amber
        EXPECTED: - If user LOST: Show red corner with lost icon Leave Blank
        """
        pass
