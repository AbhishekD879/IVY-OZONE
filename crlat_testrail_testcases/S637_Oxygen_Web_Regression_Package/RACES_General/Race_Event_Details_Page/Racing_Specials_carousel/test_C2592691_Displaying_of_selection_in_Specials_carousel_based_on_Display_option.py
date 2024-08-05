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
class Test_C2592691_Displaying_of_selection_in_Specials_carousel_based_on_Display_option(Common):
    """
    TR_ID: C2592691
    NAME: Displaying of selection in Specials carousel based on "Display" option
    DESCRIPTION: This test case verifies displaying of the selection in Specials carousel on the "Display" option on event/market/selection levels
    DESCRIPTION: AUTOTEST: [C2861414]
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

    def test_001___in_ti_tool_undisplay_the_selection_from_preconditions__in_application_refresh_the_page_and_verify_the_selection_is_no_more_displayed(self):
        """
        DESCRIPTION: - In TI tool undisplay the selection from preconditions
        DESCRIPTION: - In application refresh the page and verify the selection is no more displayed
        EXPECTED: Corresponding selection in Specials carousel is no more displayed
        """
        pass

    def test_002___in_ti_tool_display_the_selection_from_preconditions__in_application_refresh_the_page_and_verify_the_selection_is_displayed(self):
        """
        DESCRIPTION: - In TI tool display the selection from preconditions
        DESCRIPTION: - In application refresh the page and verify the selection is displayed
        EXPECTED: Corresponding selection in Specials carousel is displayed
        """
        pass

    def test_003___in_ti_tool_undisplay_the_market_of_the_selection_from_preconditions__in_application_refresh_the_page_and_verify_the_selection_is_no_more_displayed(self):
        """
        DESCRIPTION: - In TI tool undisplay the market of the selection from preconditions
        DESCRIPTION: - In application refresh the page and verify the selection is no more displayed
        EXPECTED: Corresponding selection in Specials carousel is no more displayed
        """
        pass

    def test_004___in_ti_tool_display_the_market_of_the_selection_from_preconditions__in_application_refresh_the_page_and_verify_the_selection_is_displayed(self):
        """
        DESCRIPTION: - In TI tool display the market of the selection from preconditions
        DESCRIPTION: - In application refresh the page and verify the selection is displayed
        EXPECTED: Corresponding selection in Specials carousel is displayed
        """
        pass

    def test_005___in_ti_tool_undisplay_the_event_of_the_selection_from_preconditions__in_application_refresh_the_page_and_verify_the_selection_is_no_more_displayed(self):
        """
        DESCRIPTION: - In TI tool undisplay the event of the selection from preconditions
        DESCRIPTION: - In application refresh the page and verify the selection is no more displayed
        EXPECTED: Corresponding selection in Specials carousel is no more displayed
        """
        pass

    def test_006___in_ti_tool_display_the_event_of_the_selection_from_preconditions__in_application_refresh_the_page_and_verify_the_selection_is_displayed(self):
        """
        DESCRIPTION: - In TI tool display the event of the selection from preconditions
        DESCRIPTION: - In application refresh the page and verify the selection is displayed
        EXPECTED: Corresponding selection in Specials carousel is displayed
        """
        pass
