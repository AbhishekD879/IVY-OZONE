import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C2989457_Verify_interactions_on_Extra_Place_races_module_on_Home_page(Common):
    """
    TR_ID: C2989457
    NAME: Verify interactions on 'Extra Place' races module on Home page
    DESCRIPTION: This test case verifies clicks on 'View' link, 'Extra Place' main content area and 'Extra Place' signposting icon
    DESCRIPTION: is covered by AUTOTEST [C1592556]
    PRECONDITIONS: 1. 'Next Races' tab should be present on Home page (click [here](https://ladbrokescoral.testrail.com/index.php?/cases/view/29371) to see how to configure it)
    PRECONDITIONS: 2. 'Extra Place' horse racing events should be present
    PRECONDITIONS: 3. User is viewing 'Next Races' tab on Home page
    PRECONDITIONS: **To configure HR Extra Place Race meeting use TI tool** (click [here](https://confluence.egalacoral.com/display/SPI/OpenBet+Systems) for credentials):
    PRECONDITIONS: - HR event should be not started ('rawIsOffCode'= 'N' in SS response)
    PRECONDITIONS: - HR event should have primary market 'Win or Each Way'
    PRECONDITIONS: - HR event should have 'Extra Place Race' flag ticked on market level ('drilldownTagNames'='MKTFLAG_EPR' in SS response)
    PRECONDITIONS: **To check info regarding event use the following link:**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: **To get info about class events use link:**
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: **To get info about Extra place events use link:**
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isResulted:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.isLiveNowEvent:isFalse&simpleFilter=event.rawIsOffCode:notEquals:Y&existsFilter=event:simpleFilter:market.drilldownTagNames:intersects:MKTFLAG_EPR&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&racingForm=event&limitRecords=outcome:1&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: **To configure 'Extra Place' signposting icon:**
    PRECONDITIONS: 1) Open CMS -> Promotions ->  EXTRA PLACE RACE (if promotion is configured in another case use the instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Promotions+CMS+configuration).
    PRECONDITIONS: 2) Required fields for CMS configuration of created EXTRA PLACE RACE promotion:
    PRECONDITIONS: * 'Is Signposting Promotion' checkbox (should be checked for activation Promo SIgnposting for different promotions)
    PRECONDITIONS: * 'Event-level flag' field
    PRECONDITIONS: * 'Market-level flag' field
    PRECONDITIONS: * 'Overlay BET NOW button url' field (not required but without current URL 'BET NOW' button will be unclickable)
    PRECONDITIONS: * 'Promotion Text' field (for editing promo footer text / not required)
    """
    keep_browser_open = True

    def test_001_tap_on_extra_place_event_content_area(self):
        """
        DESCRIPTION: Tap on 'Extra Place' event content area
        EXPECTED: Event content area is clickable and leads to Race Card of a corresponding event
        """
        pass

    def test_002_navigate_back_to_home_page_and_tap_on__view__for_coral___sign_for_ladbrokes(self):
        """
        DESCRIPTION: Navigate back to Home page and tap on:
        DESCRIPTION: - 'View >' **for Coral**
        DESCRIPTION: - '>' sign **for Ladbrokes**
        EXPECTED: Navigation to Race Card of a corresponding event takes place
        """
        pass

    def test_003_navigate_back_to_home_page_and_tap_on_extra_place_signposting_icon(self):
        """
        DESCRIPTION: Navigate back to Home page and tap on 'Extra Place' signposting icon
        EXPECTED: Respective promo pop-up appears
        """
        pass
