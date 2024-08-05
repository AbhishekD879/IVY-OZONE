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
class Test_C58668191_Verify_the_GA_tracking_of_the_Splash_page(Common):
    """
    TR_ID: C58668191
    NAME: Verify the GA tracking of the Splash page
    DESCRIPTION: This test case verifies the Google Analytics tracking of the Splash page.
    PRECONDITIONS: For more information please consider https://confluence.egalacoral.com/display/SPI/GA+TRACKING+CORRECT+4
    PRECONDITIONS: 1. The Quiz is configured in the CMS.
    PRECONDITIONS: 2. Open the website https://phoenix-invictus.coral.co.uk/.
    PRECONDITIONS: 3. The User is logged in.
    PRECONDITIONS: 4. The User has not played a Quiz yet.
    PRECONDITIONS: 5. Open DevTools in browser.
    """
    keep_browser_open = True

    def test_001_select_correct4_tabenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Select 'Correct4' tab.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: For Coral:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "content-view",
        EXPECTED: screen_name: "/correct4/splash"​ }
        EXPECTED: 2. Make sure that only 1 'content-view' tag is fired.
        EXPECTED: 3. The following code is not present in the console:
        EXPECTED: { event: "trackPageview",
        EXPECTED: page: "/correct4/splash" }
        EXPECTED: For Ladbrokes:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "content-view",
        EXPECTED: screen_name: "/{sourceId}/splash"​ }
        EXPECTED: 2. Make sure that only 1 'content-view' tag is fired.
        EXPECTED: 3. The following code is not present in the console:
        EXPECTED: { event: "trackPageview",
        EXPECTED: page: "/{sourceId}/splash" }
        """
        pass

    def test_002_click_on_the_cta_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the CTA button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory’: "Correct4"
        EXPECTED: eventAction: "{CTA NAME}" //e.g. "Play Now For Free", "See Your Selections", "See Previous Games", "Login To View"
        EXPECTED: eventLabel: "none" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory’: "{SourceId}"
        EXPECTED: eventAction: "{CTA NAME}" //e.g. "Play Now For Free", "See Your Selections", "See Previous Games", "Login To View"
        EXPECTED: eventLabel: "none" }
        """
        pass

    def test_003_click_on_the_back_arrow_button_on_the_mobile(self):
        """
        DESCRIPTION: Click on the Back arrow button on the mobile.
        EXPECTED: The Exit pop-up is opened.
        """
        pass

    def test_004_click_on_the_exit_game_button(self):
        """
        DESCRIPTION: Click on the 'Exit game' button.
        EXPECTED: The Exit pop-up is closed.
        EXPECTED: The User is redirected to the Splash page.
        """
        pass

    def test_005_click_on_the_x_icon_on_the_mobileenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'X' icon on the mobile.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "Exit",
        EXPECTED: eventLabel: "none" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventAction: "Exit",
        EXPECTED: eventLabel: "none" }
        """
        pass
