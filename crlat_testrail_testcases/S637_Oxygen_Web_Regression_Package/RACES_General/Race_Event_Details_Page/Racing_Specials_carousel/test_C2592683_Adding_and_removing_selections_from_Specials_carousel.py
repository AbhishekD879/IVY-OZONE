import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2592683_Adding_and_removing_selections_from_Specials_carousel(Common):
    """
    TR_ID: C2592683
    NAME: Adding and removing selections from Specials carousel
    DESCRIPTION: This test case verifies adding and removing selections from Specials carousel
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: - You should have a linked selection to <Race> event
    PRECONDITIONS: - "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should be on a <Race> EDP that has linked selections
    PRECONDITIONS: **From OX 107:**
    PRECONDITIONS: **The full request to check Enhanced Multiples data:**
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/227?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.typeName:equals:|Enhanced%20Multiples|&simpleFilter=event.suspendAtTime:greaterThan:2020-08-28T11:32:30.000Z&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_verify_that_specials_carousel_contains_all_linked_selections(self):
        """
        DESCRIPTION: Verify that Specials carousel contains all linked selections
        EXPECTED: Specials carousel is displayed with all linked selection
        """
        pass

    def test_002___in_ti_tool_link_one_more_selection_to_the_event__refresh_the_page_in_application_and_verify_that_new_selection_appears(self):
        """
        DESCRIPTION: - In TI tool link one more selection to the event
        DESCRIPTION: - Refresh the page in application and verify that new selection appears
        EXPECTED: New selection is present in Specials carousel
        """
        pass

    def test_003___in_ti_tool_unlink_one_of_the_linked_selections__refresh_the_page_in_application_and_verify_that_unlinked_selection_is_no_more_displayed(self):
        """
        DESCRIPTION: - In TI tool unlink one of the linked selections
        DESCRIPTION: - Refresh the page in application and verify that unlinked selection is no more displayed
        EXPECTED: Removed selection is not displayed in Specials carousel anymore
        """
        pass
