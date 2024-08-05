import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C35219402_Verify_Turned_off_Highlights_Carousel_in_CMS_The_event_results_undisplayed_suspended(Common):
    """
    TR_ID: C35219402
    NAME: Verify Turned off 'Highlights Carouse'l in CMS/The event results, undisplayed, suspended
    DESCRIPTION: This test case verifies that Highlights Carousel/module is not displayed when the Highlights Carousel is not available (turned off in CMS for this page
    DESCRIPTION: OR when the last Highlights Module is either resulted/ suspended/undisplayed)
    PRECONDITIONS: The app is installed and launched
    PRECONDITIONS: "Featured" Tab is opened
    PRECONDITIONS: ["Highlights Carousel" is configured in CMS
    PRECONDITIONS: "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel] - will be available after functional implementation
    PRECONDITIONS: At least 3 Highlight cards are displayed
    """
    keep_browser_open = True

    def test_001_navigate_to_the_homepage_on_the_featured_tab(self):
        """
        DESCRIPTION: Navigate to the Homepage on the Featured Tab
        EXPECTED: The homepage is displayed with featured tab
        EXPECTED: The Highlights Carousel with more than 1 Highlights Module is displayed as per design
        """
        pass

    def test_002_emulate_that_highlights_carousel_is_turned_off_in_cms_module_deactivation(self):
        """
        DESCRIPTION: Emulate that Highlights Carousel is turned off in CMS (Module deactivation)
        EXPECTED: The event Highlights Carousel be removed from the HC automatically
        """
        pass

    def test_003_emulate_that_highlights_carousel_is_turned_on_in_cms(self):
        """
        DESCRIPTION: Emulate that Highlights Carousel is turned on in CMS
        EXPECTED: The Highlights Carousel is displayed on the HP
        """
        pass

    def test_004_emulate_that_the_event_resultsundisplayedsuspended(self):
        """
        DESCRIPTION: Emulate that the event results/undisplayed/suspended
        EXPECTED: The event card is removed from the HC automatically/User to refresh the page
        """
        pass
