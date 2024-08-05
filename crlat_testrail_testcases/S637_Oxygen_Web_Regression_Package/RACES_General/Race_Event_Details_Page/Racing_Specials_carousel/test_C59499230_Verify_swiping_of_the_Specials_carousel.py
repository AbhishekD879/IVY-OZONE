import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C59499230_Verify_swiping_of_the_Specials_carousel(Common):
    """
    TR_ID: C59499230
    NAME: Verify swiping of the Specials carousel
    DESCRIPTION: This test case verifies that swiping of Specials carousel is smoothy
    PRECONDITIONS: How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: You should have a linked selection to <Race> event
    PRECONDITIONS: "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: You should be on a <Race> EDP that has linked at least two selections
    PRECONDITIONS: **From OX 107:**
    PRECONDITIONS: **The full request to check Enhanced Multiples data:**
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/227?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.typeName:equals:|Enhanced%20Multiples|&simpleFilter=event.suspendAtTime:greaterThan:2020-08-28T11:32:30.000Z&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: Home page is opened
        """
        pass

    def test_002_go_to_hr_edp_that_has_linked_at_least_two_selection_from_preconditions(self):
        """
        DESCRIPTION: Go to HR EDP that has linked at least two selection (from preconditions)
        EXPECTED: Specials carousel is placed below the video streaming buttons and above Markets tab
        """
        pass

    def test_003_swipe_the_selections_in_specials_carousel_starting_from_the_left_side(self):
        """
        DESCRIPTION: Swipe the selections in Specials carousel starting from the left side
        EXPECTED: Selections in Specials carousel swipe smoothy
        """
        pass

    def test_004_in_ti_tool_link_one_more_selection_to_the_eventrefresh_the_page_in_application_and_verify_that_new_selection_appears(self):
        """
        DESCRIPTION: In TI tool link one more selection to the event
        DESCRIPTION: Refresh the page in application and verify that new selection appears
        EXPECTED: New selection is present in Specials carousel
        """
        pass

    def test_005_swipe_the_selections_in_specials_carousel_starting_from_the_left_side(self):
        """
        DESCRIPTION: Swipe the selections in Specials carousel starting from the left side
        EXPECTED: Selections in Specials carousel swipe smoothy
        """
        pass
