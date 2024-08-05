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
class Test_C58668196_Verify_the_GA_tracking_of_the_Previous_tab(Common):
    """
    TR_ID: C58668196
    NAME: Verify the GA tracking of the Previous tab
    DESCRIPTION: This test case verifies the Google Analytics tracking of the Previous tab elements.
    PRECONDITIONS: For more information please consider https://confluence.egalacoral.com/display/SPI/GA+TRACKING+CORRECT+4
    PRECONDITIONS: 1. The Quiz is configured in the CMS.
    PRECONDITIONS: 2. Open the Correct4 https://phoenix-invictus.coral.co.uk/correct4.
    PRECONDITIONS: 3. The User is logged in.
    PRECONDITIONS: 4. The User has already played a Quiz.
    PRECONDITIONS: 5. Open DevTools in browser.
    """
    keep_browser_open = True

    def test_001_proceed_to_the_results_page(self):
        """
        DESCRIPTION: Proceed to the Results page.
        EXPECTED: The Results page is opened.
        """
        pass

    def test_002_select_the_previous_tabenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Select the 'Previous' tab.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The 'Previous' tab is opened.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Previous",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: “trackPageview”​
        EXPECTED: virtualUrl: “/correct4/previous-quiz”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Previous",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: “trackPageview”​
        EXPECTED: virtualUrl: “/correct4/previous-quiz”​ }
        """
        pass

    def test_003_select_the_latest_tabenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Select the 'Latest' tab.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The 'Latest' tab is opened.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Latest",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: “trackPageview”​
        EXPECTED: virtualUrl: “/correct4/latest-quiz”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Latest",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: “trackPageview”​
        EXPECTED: virtualUrl: “/correct4/latest-quiz”​ }
        """
        pass

    def test_004_select_the_previous_tab(self):
        """
        DESCRIPTION: Select the 'Previous' tab.
        EXPECTED: The 'Previous' tab is opened.
        """
        pass

    def test_005_tap_on_the_view_game_summary_to_expand_the_boxenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Tap on the ‘View Game Summary’ to expand the box.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The box is expanded.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "View Game Summary",
        EXPECTED: eventLabel: "Expand" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "/{SourceId}",
        EXPECTED: eventAction: "View Game Summary",
        EXPECTED: eventLabel: "Expand" }
        """
        pass

    def test_006_tap_on_the_view_game_summary_to_collapse_the_boxenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Tap on the ‘View Game Summary’ to collapse the box.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The box is collapsed.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "View Game Summary",
        EXPECTED: eventLabel: "Collapse" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "/{SourceId}",
        EXPECTED: eventAction: "View Game Summary",
        EXPECTED: eventLabel: "Colapse" }
        """
        pass

    def test_007_tap_on_the_show_more_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Tap on the ‘Show More’ button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: Additional previous games are displayed.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "View Historic Games",
        EXPECTED: eventLabel: "Show More" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventAction: "View Historic Games",
        EXPECTED: eventLabel: "Show More" }
        """
        pass
