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
class Test_C57732053_Verify_appearing_of_Quiz_Pop_ups_when_user_abandons_the_Quiz(Common):
    """
    TR_ID: C57732053
    NAME: Verify appearing  of Quiz Pop-ups when user abandons the Quiz
    DESCRIPTION: This test case verifies displaying of Quiz Pop-ups
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. User did not play quiz yet
    """
    keep_browser_open = True

    def test_001_open_correct_4qe_link(self):
        """
        DESCRIPTION: Open Correct 4/QE link
        EXPECTED: - Correct 4/QE successfully opened
        """
        pass

    def test_002_user_abandons_the_quiz_by_selecting_the_back_arrow_or_x(self):
        """
        DESCRIPTION: User abandons the Quiz by selecting the Back arrow or 'X'
        EXPECTED: - Correct 4/QE should be closed and user redirected to the previous page
        """
        pass

    def test_003_open_page_url_which_is_configured_to_trigger_pop_up_on_cms_quiz__pop_ups(self):
        """
        DESCRIPTION: Open Page URL which is configured to trigger Pop-Up on CMS (Quiz > Pop-Ups)
        EXPECTED: - Pop-up should appear on the configured page until predictions made
        """
        pass

    def test_004_open_any_page_url_which_is_not_configured_to_trigger_pop_up(self):
        """
        DESCRIPTION: Open ANY page URL which is NOT configured to trigger Pop-Up
        EXPECTED: - Pop-up should NOT appear on any other pages
        """
        pass
