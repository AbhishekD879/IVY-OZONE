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
class Test_C57732155_Verify_the_view_and_navigation_of_the_Splash_Page_when_user_have_already_played_a_current_game(Common):
    """
    TR_ID: C57732155
    NAME: Verify the view and navigation of the Splash Page when user have already played a current game
    DESCRIPTION: This test case verifies:
    DESCRIPTION: - the view of the Splash Page when User have already played a current game.
    DESCRIPTION: - Start page navigation for the 'See your selections' CTA2 button.
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds,
    PRECONDITIONS: 1. The User is logged in https://m.ladbrokes.com.
    PRECONDITIONS: 2. The User is logged into CMS.
    PRECONDITIONS: 3. The User opens previously created Quiz.
    PRECONDITIONS: 4. Content for Splash page configured before.
    PRECONDITIONS: 5. The User has already played the current game (but the results aren't available yet).
    """
    keep_browser_open = True

    def test_001_tap_on_banner_or_link_to_launch_a_quiz(self):
        """
        DESCRIPTION: Tap on banner or link to launch a quiz
        EXPECTED: - Splash page displayed and correctly designed according to:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962c641a109bd3fc7405
        EXPECTED: - Button with the text 'See your selections' displayed (Retrieved from CMS > CTA2)
        """
        pass

    def test_002_tap_on_the_see_your_selections_cta2_button(self):
        """
        DESCRIPTION: Tap on the 'See your selections' CTA2 button.
        EXPECTED: The User is navigated to the Results page > Latest tab.
        """
        pass
