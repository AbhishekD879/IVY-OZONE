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
class Test_C57732051_To_EditVerify_appearing_of_Quiz_Pop_ups_after_selecting_Dont_show_again(Common):
    """
    TR_ID: C57732051
    NAME: [To-Edit]Verify appearing  of Quiz Pop-ups after selecting 'Don't show again'
    DESCRIPTION: [To-Edit] - the screenshot needs to be updated
    DESCRIPTION: This test case verifies displaying of Quiz Pop-ups
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. User did not play quiz yet
    """
    keep_browser_open = True

    def test_001_open_page_url_which_is_configured_to_trigger_pop_up_on_cms_quiz_gt_pop_ups(self):
        """
        DESCRIPTION: Open Page URL which is configured to trigger Pop-Up on CMS (Quiz &gt; Pop-Ups)
        EXPECTED: - Pop-up appears after [xx] seconds after page fully loads first
        EXPECTED: - Pop-up with buttons:
        EXPECTED: Take quiz
        EXPECTED: Don't show me again
        EXPECTED: Maybe later
        EXPECTED: Texts from CMS displayed and designed:
        """
        pass

    def test_002_user_select_dont_show_again_on_the_launching_pop_up(self):
        """
        DESCRIPTION: User select 'Don't show again' on the launching pop-up
        EXPECTED: - Pop-up should be closed and user redirected to the previous page
        """
        pass

    def test_003_open_page_url_which_is_configured_to_trigger_pop_up_on_cms_quiz_gt_pop_ups(self):
        """
        DESCRIPTION: Open Page URL which is configured to trigger Pop-Up on CMS (Quiz &gt; Pop-Ups)
        EXPECTED: - Pop-up should NOT appear again on the configured page
        """
        pass
