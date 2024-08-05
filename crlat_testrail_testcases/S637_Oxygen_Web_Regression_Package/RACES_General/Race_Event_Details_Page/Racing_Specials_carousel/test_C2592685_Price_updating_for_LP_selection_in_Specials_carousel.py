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
class Test_C2592685_Price_updating_for_LP_selection_in_Specials_carousel(Common):
    """
    TR_ID: C2592685
    NAME: Price updating for LP selection in Specials carousel
    DESCRIPTION: This test case verifies live price updates for LP selection in Specials carousel
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: - You should have a linked LP selection to <Race> event
    PRECONDITIONS: - "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should be on a <Race> EDP that has linked selections
    PRECONDITIONS: To get SiteServer info about event use the following url: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYYYY?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: X.XX - current supported version of OpenBet SiteServer
    PRECONDITIONS: YYYYYYY- event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes which defines price type for an event:
    PRECONDITIONS: 'priceTypeCodes' = 'LP'
    PRECONDITIONS: 'priceTypeCodes' = 'SP'
    PRECONDITIONS: 'priceTypeCodes' = 'LP,SP'
    PRECONDITIONS: **From OX 107:**
    PRECONDITIONS: **The full request to check Enhanced Multiples data:**
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/227?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.typeName:equals:|Enhanced%20Multiples|&simpleFilter=event.suspendAtTime:greaterThan:2020-08-28T11:32:30.000Z&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001___in_ti_tool_increase_the_price_for_linked_lp_selection__in_application_verify_live_price_update(self):
        """
        DESCRIPTION: - In TI tool increase the price for linked LP selection
        DESCRIPTION: - In application verify live price update
        EXPECTED: - Corresponding 'Price/Odds' button immediately displays new price
        EXPECTED: - The outcome button changes its color to red for a few seconds
        EXPECTED: - old price shown crossed out below the outcome botton (for Coral with 'was' word)
        EXPECTED: ![](index.php?/attachments/get/118703021)
        """
        pass

    def test_002___in_ti_tool_decrease_the_price_for_linked_lp_selection__in_application_verify_live_price_update(self):
        """
        DESCRIPTION: - In TI tool decrease the price for linked LP selection
        DESCRIPTION: - In application verify live price update
        EXPECTED: - Corresponding 'Price/Odds' button immediately displays new price
        EXPECTED: - The outcome button changes its color to blue for a few seconds
        EXPECTED: - old price shown crossed out below the outcome botton (for Coral with 'was' word)
        """
        pass
