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
class Test_C34278878_Verify_displaying_of_the_Highlights_carousel(Common):
    """
    TR_ID: C34278878
    NAME: Verify displaying of the Highlights carousel
    DESCRIPTION: This test case verifies displaying of the Highlights carousel
    PRECONDITIONS: The app is installed and launched
    PRECONDITIONS: "Featured" Tab is opened
    PRECONDITIONS: ["Highlights Carousel" is configured in CMS
    PRECONDITIONS: "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel] - will be available after functional implementation
    PRECONDITIONS: At least 3 Highlight cards to be displayed
    """
    keep_browser_open = True

    def test_001_navigate_to_the_homepage_on_the_featured_tab(self):
        """
        DESCRIPTION: Navigate to the Homepage on the Featured Tab
        EXPECTED: The Homepage is displayed with Featured Tab
        EXPECTED: The Highlights Carousel with more than 1 Highlights card is displayed as per design:
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/17649946)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/17649948)
        """
        pass

    def test_002_swipe_the_highlights_carousel(self):
        """
        DESCRIPTION: Swipe the Highlights Carousel
        EXPECTED: The carousel is swiped
        EXPECTED: 2nd highlight card is displayed in the middle (part of 1st and 3rd highlight card are displayed on the edge of the screen)
        """
        pass

    def test_003_scroll_carousel_to_the_last_card(self):
        """
        DESCRIPTION: Scroll Carousel to the last card
        EXPECTED: Extra white space after the card is not shown
        """
        pass

    def test_004_click_anywhere_on_the_slidecard_except_the_odds_button(self):
        """
        DESCRIPTION: Click anywhere on the slide/card (except the odds button)
        EXPECTED: User is navigated to the EDP of the event
        """
        pass
