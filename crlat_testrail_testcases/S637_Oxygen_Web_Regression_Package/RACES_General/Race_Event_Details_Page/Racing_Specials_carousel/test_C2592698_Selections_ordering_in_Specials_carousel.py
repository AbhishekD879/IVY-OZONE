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
class Test_C2592698_Selections_ordering_in_Specials_carousel(Common):
    """
    TR_ID: C2592698
    NAME: Selections ordering in Specials carousel
    DESCRIPTION: This test case verifies that selections in Specials carousel are ordered according to the display order in OpenBet
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: - You should have a couple linked selections with different 'Display Order' value that belongs to different events with different 'Display Order' value to <Race> event
    PRECONDITIONS: - "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should be on a <Race> EDP that has linked selections
    PRECONDITIONS: **From OX 107:**
    PRECONDITIONS: **The full request to check Enhanced Multiples data:**
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/227?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.typeName:equals:|Enhanced%20Multiples|&simpleFilter=event.suspendAtTime:greaterThan:2020-08-28T11:32:30.000Z&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_verify_ordering_of_selections_in_specials_carousel(self):
        """
        DESCRIPTION: Verify ordering of selections in Specials carousel
        EXPECTED: - Firstly selections are grouped by events and events are ordered by the events' 'Display Order' value, then events' time and then events' name
        EXPECTED: - Secondly selections are grouped by markets and ordered by markets' 'Display Order' value, then by markets' name
        EXPECTED: - Thirdly selections are ordered by the selections' 'Display Order' value within their market and then according to the selections name
        """
        pass
