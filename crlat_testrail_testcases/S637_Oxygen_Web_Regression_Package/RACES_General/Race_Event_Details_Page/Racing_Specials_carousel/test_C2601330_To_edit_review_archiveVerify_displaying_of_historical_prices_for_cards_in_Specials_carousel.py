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
class Test_C2601330_To_edit_review_archiveVerify_displaying_of_historical_prices_for_cards_in_Specials_carousel(Common):
    """
    TR_ID: C2601330
    NAME: (To edit/review/archive)Verify displaying of historical prices for cards in Specials carousel
    DESCRIPTION: This test case verifies that historical price is not reflected for outcomes in Specials carousel
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: - You should have a linked LP, SP, LP/SP selections to <Race> event
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

    def test_001___in_ti_tool_increasedecrease_the_price_for_linked_selections__in_application_verify_selections_card_in_specials_carousel(self):
        """
        DESCRIPTION: - In TI tool increase/decrease the price for linked selections
        DESCRIPTION: - In application verify selection's card in Specials carousel
        EXPECTED: LP, LP/SP selections:
        EXPECTED: - The price is properly updated
        EXPECTED: - The historical price is NOT displayed under the outcome button
        EXPECTED: SP selection:
        EXPECTED: - The price is not updated
        EXPECTED: - The historical price is NOT displayed under the outcome button
        """
        pass
