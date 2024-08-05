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
class Test_C57732154_Verify_the_view_and_navigation_of_the_Splash_Page_when_user_havent_played_a_current_game(Common):
    """
    TR_ID: C57732154
    NAME: Verify the view and navigation of the Splash Page when user haven't played a current game
    DESCRIPTION: This test case verifies:
    DESCRIPTION: - the view of the Splash Page when User haven't played a current game.
    DESCRIPTION: - Start page navigation for a 'PLAY NOW FOR FREE' CTA1 button.
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds,
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. The user is logged in to CMS
    PRECONDITIONS: 3. User opens previously created Quiz
    PRECONDITIONS: 4. Content for Splash page configured before
    PRECONDITIONS: 5. User haven't played the current game yet
    """
    keep_browser_open = True

    def test_001_tap_on_banner_or_link_to_launch_a_quiz(self):
        """
        DESCRIPTION: Tap on banner or link to launch a quiz
        EXPECTED: - Splash page displayed and correctly designed according to:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962ddc6f4e9be56f646c
        EXPECTED: - Button with the text 'Play now for free' displayed (Retrieved from CMS > CTA1)
        """
        pass

    def test_002_tap_on_the_play_now_for_free_cta1_button(self):
        """
        DESCRIPTION: Tap on the 'Play now for free' CTA1 button.
        EXPECTED: The User is navigated to the first question page.
        """
        pass
