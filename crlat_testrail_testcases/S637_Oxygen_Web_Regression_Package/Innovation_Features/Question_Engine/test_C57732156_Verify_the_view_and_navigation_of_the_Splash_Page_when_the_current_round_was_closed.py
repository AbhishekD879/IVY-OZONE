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
class Test_C57732156_Verify_the_view_and_navigation_of_the_Splash_Page_when_the_current_round_was_closed(Common):
    """
    TR_ID: C57732156
    NAME: Verify the view and navigation of the Splash Page when the current round was closed
    DESCRIPTION: This test case verifies:
    DESCRIPTION: - the view of the Splash Page when the current round was closed.
    DESCRIPTION: - Start page navigation for the 'SEE PREVIOUS SELECTIONS' CTA3 button.
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds,
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. The user is logged in to CMS
    PRECONDITIONS: 3. User opens previously created Quiz
    PRECONDITIONS: 4. Content for Splash page configured before
    PRECONDITIONS: 5. Current round already closed (i.e whether the played or not, if the round is closed then they can go  back to check previous games )
    """
    keep_browser_open = True

    def test_001_tap_on_banner_or_link_to_launch_a_quiz(self):
        """
        DESCRIPTION: Tap on banner or link to launch a quiz
        EXPECTED: - Splash page displayed and correctly designed according to:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962bc05f3d524197039a
        EXPECTED: - Button with the text 'SEE PREVIOUS SELECTIONS' is displayed (Retrieved from CMS > CTA3)
        """
        pass

    def test_002_tap_on_the_see_previous_selections_cta3_button(self):
        """
        DESCRIPTION: Tap on the 'SEE PREVIOUS SELECTIONS' CTA3 button.
        EXPECTED: The User is navigated to the Results page > Previous tab.
        """
        pass
