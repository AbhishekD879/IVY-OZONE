import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C52274481_In_Play_Watch_Live_Verify_that_Data_is_Loading_after_Quick_Expanding_Collapsing_of_Sport_AccordionSport_Category(Common):
    """
    TR_ID: C52274481
    NAME: In-Play/Watch Live: Verify that Data is Loading after Quick Expanding/Collapsing of  Sport Accordion(Sport Category)
    DESCRIPTION: This test case verifies that Data is Loading after Quick Expanding/Collapsing of  Sport Accordion(Sport Category)
    DESCRIPTION: ![](index.php?/attachments/get/75809217)
    DESCRIPTION: ![](index.php?/attachments/get/75809229)
    PRECONDITIONS: * In-Play events are available on 'Watch Live' tab
    PRECONDITIONS: * The app is open
    PRECONDITIONS: * Open In-Play tab
    """
    keep_browser_open = True

    def test_001_navigate_to_watch_live_on_in_play(self):
        """
        DESCRIPTION: Navigate to 'Watch Live' on In-Play
        EXPECTED: * The 'Watch Live' tab is opened
        EXPECTED: * The events from the first category are expanded (based on config)
        EXPECTED: * Next events are collapsed
        """
        pass

    def test_002_collapse_the_first_sports_category_for_example_football(self):
        """
        DESCRIPTION: Collapse the first sports category (for example, Football)
        EXPECTED: All events are collapsed from the selected category
        """
        pass

    def test_003_double_click_on_the_same_sports_category(self):
        """
        DESCRIPTION: Double-click on the same sports category
        EXPECTED: All events are collapsed from the selected category
        """
        pass

    def test_004_single_click_on_the_same_sports_category(self):
        """
        DESCRIPTION: Single click on the same sports category
        EXPECTED: * The spinner is shown
        EXPECTED: * The Sport Accordion is expanded
        EXPECTED: * After some seconds the events are loaded
        """
        pass

    def test_005_click_four_times_in_a_row(self):
        """
        DESCRIPTION: Click four times in a row
        EXPECTED: * The spinner is shown
        EXPECTED: * The Sport Accordion is expanded
        EXPECTED: * After some seconds the events are loaded
        """
        pass

    def test_006_click_three_times_on_a_different_sports_categoryfor_example_tennis(self):
        """
        DESCRIPTION: Click three times on a different sports category(for example, Tennis)
        EXPECTED: * The spinner is shown
        EXPECTED: * The Sport Accordion is expanded
        EXPECTED: * After some seconds the events are loaded
        """
        pass
