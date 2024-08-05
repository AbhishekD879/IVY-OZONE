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
class Test_C2592696_Specials_carousel_details_UI(Common):
    """
    TR_ID: C2592696
    NAME: Specials carousel details UI
    DESCRIPTION: This test case verifies the selection displaying in Specials carousel
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: - You should have a linked selection to <Race> event
    PRECONDITIONS: - "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should be on a <Race> EDP that has linked selections
    PRECONDITIONS: https://app.zeplin.io/project/5de6962b0c68b753005a2b58/screen/5de915e803e79d7f2532dff4
    PRECONDITIONS: **From OX 107:**
    PRECONDITIONS: **The full request to check Enhanced Multiples data:**
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/227?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.typeName:equals:|Enhanced%20Multiples|&simpleFilter=event.suspendAtTime:greaterThan:2020-08-28T11:32:30.000Z&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_verify_that_ui_elements_are_present(self):
        """
        DESCRIPTION: Verify that UI elements are present:
        EXPECTED: - Specials carousel is placed below the video streaming buttons and above Markets tab
        EXPECTED: - Cards label name in Specials carousel is the same as in CMS > System Configuration > Structure > Racing Specials carousel section > label field
        EXPECTED: - The selection's name is the same as selection's name in TI tool
        EXPECTED: - The price of the selection button is the same as in TI tool
        EXPECTED: ![](index.php?/attachments/get/118703017)
        """
        pass
