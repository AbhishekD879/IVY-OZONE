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
class Test_C57732050_Verify_switching_On_Off_quiz_Pop_up(Common):
    """
    TR_ID: C57732050
    NAME: Verify switching On/Off  quiz Pop-up
    DESCRIPTION: This test case verifies switching On/Off  quiz Pop-up
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    """
    keep_browser_open = True

    def test_001___open_cms__quiz__pop_ups__switch_off_the_pop_up_to_launch_a_quiz_in_the_quiz_pop_up_librarysave_changes(self):
        """
        DESCRIPTION: - Open CMS > Quiz > Pop-Ups
        DESCRIPTION: - Switch Off the pop-up to launch a quiz in the quiz Pop-up library
        DESCRIPTION: Save changes
        EXPECTED: CMS configuration saved
        """
        pass

    def test_002_open_page_url_which_is_configured_to_trigger_pop_up_on_cms_quiz__pop_ups(self):
        """
        DESCRIPTION: Open Page URL which is configured to trigger Pop-Up on CMS (Quiz > Pop-Ups)
        EXPECTED: - Pop-up should NOT appear again on the configured page
        """
        pass

    def test_003___open_cms__quiz__pop_ups__switch_on_the_pop_up_to_launch_a_quiz_in_the_quiz_pop_up_librarysave_changes(self):
        """
        DESCRIPTION: - Open CMS > Quiz > Pop-Ups
        DESCRIPTION: - Switch On the pop-up to launch a quiz in the quiz Pop-up library
        DESCRIPTION: Save changes
        EXPECTED: CMS configuration saved
        """
        pass

    def test_004_open_page_url_which_is_configured_to_trigger_pop_up_on_cms_quiz__pop_ups(self):
        """
        DESCRIPTION: Open Page URL which is configured to trigger Pop-Up on CMS (Quiz > Pop-Ups)
        EXPECTED: - Pop-up appears after [xx] seconds after page fully loads first
        EXPECTED: - Pop-up with buttons:
        EXPECTED: Take quiz
        EXPECTED: Don't show me again
        EXPECTED: Maybe later
        EXPECTED: Texts from CMS displayed and designed:
        EXPECTED: ![](index.php?/attachments/get/36694089)
        """
        pass
