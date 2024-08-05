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
class Test_C2592684_Specials_carousel_displaying_depending_on_min_number_of_linked_selections(Common):
    """
    TR_ID: C2592684
    NAME: Specials carousel displaying depending on min number of linked selections
    DESCRIPTION: This test case verifies that specials carousel appears only when there is a at least 1 linked selection
    DESCRIPTION: AUTOTEST: [C2861362]
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: - You should have a <Race> event WITHOUT linked selections
    PRECONDITIONS: - "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should be on a <Race> EDP that selections will be linked to
    PRECONDITIONS: **From OX 107:**
    PRECONDITIONS: **The full request to check Enhanced Multiples data:**
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/227?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.typeName:equals:|Enhanced%20Multiples|&simpleFilter=event.suspendAtTime:greaterThan:2020-08-28T11:32:30.000Z&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_verify_specials_carousel_displaying(self):
        """
        DESCRIPTION: Verify Specials carousel displaying
        EXPECTED: Specials carousel is not displayed
        """
        pass

    def test_002___in_ti_tool_link_selection_from_horse_race_specials_to_the_horse_race_event_from_preconditions__refresh_the_page_in_application_and_verify_specials_carousel_displaying(self):
        """
        DESCRIPTION: - In TI tool link selection from horse race specials to the horse race event from preconditions
        DESCRIPTION: - Refresh the page in application and verify Specials carousel displaying
        EXPECTED: Specials carousel is displayed with the linked selection
        """
        pass

    def test_003___in_ti_tool_unlink_the_selection_from_the_event__refresh_the_page_in_application_and_verify_specials_carousel_displaying(self):
        """
        DESCRIPTION: - In TI tool unlink the selection from the event
        DESCRIPTION: - Refresh the page in application and verify Specials carousel displaying
        EXPECTED: Specials carousel is not displayed anymore
        """
        pass
