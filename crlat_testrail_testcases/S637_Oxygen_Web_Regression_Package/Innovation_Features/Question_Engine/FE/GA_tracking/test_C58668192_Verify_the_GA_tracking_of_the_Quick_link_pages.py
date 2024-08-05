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
class Test_C58668192_Verify_the_GA_tracking_of_the_Quick_link_pages(Common):
    """
    TR_ID: C58668192
    NAME: Verify the GA tracking of the Quick link pages
    DESCRIPTION: This test case verifies the Google Analytics tracking of the Splash page.
    PRECONDITIONS: For more information please consider https://confluence.egalacoral.com/display/SPI/GA+TRACKING+CORRECT+4
    PRECONDITIONS: 1. The Quiz is configured in the CMS.
    PRECONDITIONS: 2. Open the Correct4 https://phoenix-invictus.coral.co.uk/correct4.
    PRECONDITIONS: 3. The User is logged in.
    PRECONDITIONS: 4. The User has not played a Quiz yet.
    PRECONDITIONS: 5. Open DevTools in browser.
    """
    keep_browser_open = True

    def test_001_click_on_the_prizes_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Prizes' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: For Coral:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "Prizes",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: "content-view"
        EXPECTED: screen_name: "/correct4/info/prizes" }
        EXPECTED: 2. The following code is not present in the console:
        EXPECTED: { event: “trackPageview”​,
        EXPECTED: page: “/correct4/info/prizes”​ }
        EXPECTED: For Ladbrokes:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventAction: "Prizes",
        EXPECTED: eventLabel: "none"},
        EXPECTED: { event: "content-view"
        EXPECTED: screen_name: "/qe/{sourceId}/info/prizes" }
        EXPECTED: 2. The following code is not present in the console:
        EXPECTED: { event: “trackPageview”​,
        EXPECTED: page: “/{sourceId}/info/prizes”​ }
        """
        pass

    def test_002_click_on_the_back_arrow_button(self):
        """
        DESCRIPTION: Click on the Back arrow button.
        EXPECTED: The Splash page is opened.
        """
        pass

    def test_003_click_on_the_faq_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'FAQ' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: For Coral:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "FAQ",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: "content-view"
        EXPECTED: screen_name: "/correct4/info/faq" }
        EXPECTED: 2. The following code is not present in the console:
        EXPECTED: { event: “trackPageview”​,
        EXPECTED: page: “/correct4/info/faq”​ }
        EXPECTED: For Ladbrokes:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventAction: "FAQ",
        EXPECTED: eventLabel: "none"},
        EXPECTED: { event: "content-view"
        EXPECTED: screen_name: "/qe/{sourceId}/info/faq" }
        EXPECTED: 2. The following code is not present in the console:
        EXPECTED: { event: “trackPageview”​,
        EXPECTED: page: “/{sourceId}/info/faq”​ }
        """
        pass

    def test_004_click_on_the_back_arrow_button(self):
        """
        DESCRIPTION: Click on the Back arrow button.
        EXPECTED: The Splash page is opened.
        """
        pass

    def test_005_click_on_the_terms__conditions_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Terms & Conditions' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: For Coral:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "Terms & Conditions",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: "content-view"
        EXPECTED: screen_name: "/correct4/info/terms" }
        EXPECTED: 2. The following code is not present in the console:
        EXPECTED: { event: “trackPageview”​,
        EXPECTED: page: “/correct4/info/terms”​ }
        EXPECTED: For Ladbrokes
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventAction: "Terms & Conditions",
        EXPECTED: eventLabel: "none"},
        EXPECTED: { event: "content-view"
        EXPECTED: screen_name: "/qe/{sourceId}/info/terms" }
        EXPECTED: 2. The following code is not present in the console:
        EXPECTED: { event: “trackPageview”​,
        EXPECTED: page: “/{sourceId}/info/terms”​ }
        """
        pass
