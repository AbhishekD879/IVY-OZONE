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
class Test_C2989455_Verify_live_updates_for_Extra_Place_races_module_on_Home_page(Common):
    """
    TR_ID: C2989455
    NAME: Verify live updates for 'Extra Place' races module on Home page
    DESCRIPTION: This test case verifies that when 'Extra Place' races events become live or resulted/finished, they are removed from module by live updates (automatically, without page refresh)
    PRECONDITIONS: 1. 'Next Races' tab should be present on Home page (click [here](https://ladbrokescoral.testrail.com/index.php?/cases/view/29371) to see how to configure it)
    PRECONDITIONS: 2. 'Extra Place' horse racing events should be present
    PRECONDITIONS: 3. User is viewing 'Next Races' tab on Home page
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
    PRECONDITIONS: **To configure HR Extra Place Race meeting use TI tool** (click [here](https://confluence.egalacoral.com/display/SPI/OpenBet+Systems) for credentials):
    PRECONDITIONS: - HR event should be not started ('rawIsOffCode'= 'N' in SS response)
    PRECONDITIONS: - HR event should have primary market 'Win or Each Way'
    PRECONDITIONS: - HR event should have 'Extra Place Race' flag ticked on market level ('drilldownTagNames'='MKTFLAG_EPR' in SS response)
    """
    keep_browser_open = True

    def test_001_make_one_of_extra_place_races_events_become_live(self):
        """
        DESCRIPTION: Make one of 'Extra Place' races events become live
        EXPECTED: * Event is removed from 'Extra Place' module automatically
        EXPECTED: * Another event does not appear in module automatically
        """
        pass

    def test_002_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Another  'Extra Place' event appears in module
        """
        pass

    def test_003_undisplay_one_of_extra_place_events(self):
        """
        DESCRIPTION: Undisplay one of 'Extra Place' events
        EXPECTED: * Event is removed from 'Extra Place' module automatically
        EXPECTED: * Another event does not appear in module automatically
        """
        pass

    def test_004_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Another  'Extra Place' event appears in module
        """
        pass

    def test_005_make_all_events_live_or_undisplayed(self):
        """
        DESCRIPTION: Make all events live or undisplayed
        EXPECTED: * Events are removed automatically
        EXPECTED: * Module is not shown at all
        """
        pass
