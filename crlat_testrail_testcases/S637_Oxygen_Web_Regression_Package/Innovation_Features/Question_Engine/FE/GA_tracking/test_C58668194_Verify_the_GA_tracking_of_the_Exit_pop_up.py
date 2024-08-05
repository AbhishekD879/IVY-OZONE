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
class Test_C58668194_Verify_the_GA_tracking_of_the_Exit_pop_up(Common):
    """
    TR_ID: C58668194
    NAME: Verify the GA tracking of the Exit pop-up
    DESCRIPTION: This test case verifies the Google Analytics tracking of the Exit pop-up.
    PRECONDITIONS: For more information please consider https://confluence.egalacoral.com/display/SPI/GA+TRACKING+CORRECT+4
    PRECONDITIONS: 1. The Quiz is configured in the CMS.
    PRECONDITIONS: 2. Open the Correct4 https://phoenix-invictus.coral.co.uk/correct4.
    PRECONDITIONS: 3. The User is logged in.
    PRECONDITIONS: 4. The User has not played a Quiz yet.
    PRECONDITIONS: 5. Open DevTools in browser.
    """
    keep_browser_open = True

    def test_001_click_on_the_play_now_for_free_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Play now for free' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question1”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/{sourceId}/question1”​ }
        """
        pass

    def test_002_click_on_the_exit_button_on_the_desktop__x_icon_on_the_mobileenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Exit' button on the Desktop / 'X' icon on the mobile.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: No additional code is present in the console.
        """
        pass

    def test_003_click_on_the_keep_playing_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Keep playing' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Exit - Are You Sure?",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventLabel: "Keep Playing" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Exit - Are You Sure?",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventLabel: "Keep Playing" }
        """
        pass

    def test_004_click_on_the_exit_button_on_the_desktop__x_icon_on_the_mobileenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Exit' button on the Desktop / 'X' icon on the mobile.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: No additional code is present in the console.
        """
        pass

    def test_005_click_on_the_exit_game_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Exit game' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Exit - Are You Sure?",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventLabel: "Exit Game" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Exit - Are You Sure?",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventLabel: "Exit Game" }
        """
        pass
