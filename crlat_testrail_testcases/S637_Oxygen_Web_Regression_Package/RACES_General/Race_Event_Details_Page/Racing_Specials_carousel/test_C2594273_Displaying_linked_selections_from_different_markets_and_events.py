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
class Test_C2594273_Displaying_linked_selections_from_different_markets_and_events(Common):
    """
    TR_ID: C2594273
    NAME: Displaying linked selections from different markets and events
    DESCRIPTION: This test case verifies that linked selections from different markets and events are displayed in Specials carousel
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: - You should have couple linked selections from one <Race> event from the same market to another <Race> event
    PRECONDITIONS: - "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should be on a <Race> EDP that has linked selections
    PRECONDITIONS: **From OX 107:**
    PRECONDITIONS: **The full request to check Enhanced Multiples data:**
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/227?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.typeName:equals:|Enhanced%20Multiples|&simpleFilter=event.suspendAtTime:greaterThan:2020-08-28T11:32:30.000Z&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_verify_that_all_linked_selections_are_displayed(self):
        """
        DESCRIPTION: Verify that all linked selections are displayed
        EXPECTED: All linked selections are displayed
        """
        pass

    def test_002___in_ti_tool_link_selection_from_another_market_of_the_race_event_from_preconditions__in_application_refresh_the_page_and_verify_selections_displaying(self):
        """
        DESCRIPTION: - In TI tool link selection from another market of the <Race> event from preconditions
        DESCRIPTION: - In Application refresh the page and verify selections displaying
        EXPECTED: All linked selections are displayed
        """
        pass

    def test_003___in_ti_tool_link_selection_from_another_race_event__in_application_refresh_the_page_and_verify_selections_displaying(self):
        """
        DESCRIPTION: - In TI tool link selection from another <Race> event
        DESCRIPTION: - In Application refresh the page and verify selections displaying
        EXPECTED: All linked selections are displayed
        """
        pass
