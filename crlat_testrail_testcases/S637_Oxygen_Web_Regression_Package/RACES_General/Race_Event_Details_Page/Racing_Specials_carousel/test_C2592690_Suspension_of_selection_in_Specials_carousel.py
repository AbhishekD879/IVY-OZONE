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
class Test_C2592690_Suspension_of_selection_in_Specials_carousel(Common):
    """
    TR_ID: C2592690
    NAME: Suspension of selection in Specials carousel
    DESCRIPTION: This test case verifies suspension of the selection in Specials carousel on the event/market/selection levels
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

    def test_001___in_ti_tool_suspend_the_linked_selection__in_application_verify_the_selection_is_suspended_in_live(self):
        """
        DESCRIPTION: - In TI tool suspend the linked selection
        DESCRIPTION: - In application verify the selection is suspended in live
        EXPECTED: Suspended selection in Specials carousel is suspended in live
        """
        pass

    def test_002___in_ti_tool_enable_the_linked_selection__in_application_verify_the_selection_is_enabled_in_live(self):
        """
        DESCRIPTION: - In TI tool enable the linked selection
        DESCRIPTION: - In application verify the selection is enabled in live
        EXPECTED: Unsuspended selection in Specials carousel is enabled in live
        """
        pass

    def test_003___in_ti_tool_suspend_the_market_of_the_linked_selections__in_application_verify_the_selections_are_suspended_in_live(self):
        """
        DESCRIPTION: - In TI tool suspend the market of the linked selections
        DESCRIPTION: - In application verify the selections are suspended in live
        EXPECTED: Selections from the market are suspended in live in Special carousel
        """
        pass

    def test_004___in_ti_tool_enable_the_market_of_the_linked_selections__in_application_verify_the_selections_are_enabled_in_live(self):
        """
        DESCRIPTION: - In TI tool enable the market of the linked selections
        DESCRIPTION: - In application verify the selections are enabled in live
        EXPECTED: Selections from the market are enabled in live in Special carousel
        """
        pass

    def test_005___in_ti_tool_suspend_the_event_of_the_linked_selections__in_application_verify_the_selections_are_suspended_in_live(self):
        """
        DESCRIPTION: - In TI tool suspend the event of the linked selections
        DESCRIPTION: - In application verify the selections are suspended in live
        EXPECTED: Selections from different markets from the suspended event are suspended in live in Special carousel
        """
        pass

    def test_006___in_ti_tool_enable_the_event_of_the_linked_selections__in_application_verify_the_selection_are_enabled_in_live(self):
        """
        DESCRIPTION: - In TI tool enable the event of the linked selections
        DESCRIPTION: - In application verify the selection are enabled in live
        EXPECTED: Selections from different markets from the enabled event are enabled in live in Special carousel
        """
        pass
