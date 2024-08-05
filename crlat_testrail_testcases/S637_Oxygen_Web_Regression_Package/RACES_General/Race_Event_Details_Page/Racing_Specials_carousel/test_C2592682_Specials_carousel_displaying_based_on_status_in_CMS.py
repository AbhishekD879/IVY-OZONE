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
class Test_C2592682_Specials_carousel_displaying_based_on_status_in_CMS(Common):
    """
    TR_ID: C2592682
    NAME: Specials carousel displaying based on status in CMS
    DESCRIPTION: This test case verifies displaying of Specials carousel based on status in CMS
    DESCRIPTION: Note: Cannot be automated as we decided not to turn off anything in CMS (because other tests or QAs can turn it on while autotest is running so autotest will be not stable)
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

    def test_001_verify_that_specials_carousel_is_present(self):
        """
        DESCRIPTION: Verify that Specials carousel is present
        EXPECTED: Specials carousel is displayed
        """
        pass

    def test_002___in_cms__system_configuration__structure_deactivate_horse_races_specials_carousel__refresh_the_page_in_application_verify_that_specials_carousel_disappeared_and_request_for_the_linked_selections_is_not_send(self):
        """
        DESCRIPTION: - In CMS > System Configuration > Structure deactivate "Horse Races Specials Carousel"
        DESCRIPTION: - Refresh the page in application, verify that Specials carousel disappeared and request for the linked selections is not send
        EXPECTED: - Specials carousel is not displayed anymore
        EXPECTED: - There is no request in console:  "[eventID]?translationLang=en"
        """
        pass
