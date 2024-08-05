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
class Test_C2592695_Undisplaying_of_the_selection_of_the_resulted_event_in_Specials_carousel(Common):
    """
    TR_ID: C2592695
    NAME: Undisplaying of the selection of the resulted event in Specials carousel
    DESCRIPTION: This test case verifies reflection of the selection of the resulted event
    DESCRIPTION: AUTOTEST [C2855503]
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

    def test_001___in_ti_tool_result_the_event_of_the_linked_selection_isresultedtrue_or_isfinishedtrue_attribute_should_be_present_on_event_level_in_ss_response__in_application_verify_the_selection_is_undisplayed_after_page_refresh(self):
        """
        DESCRIPTION: - In TI tool result the event of the linked selection ('isResulted=true' OR 'isFinished=true' attribute should be present on event level in SS response)
        DESCRIPTION: - In application verify the selection is undisplayed after page refresh
        EXPECTED: The selection of the resulted event is undisplayed after page refresh.
        """
        pass
