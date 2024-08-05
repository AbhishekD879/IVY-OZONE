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
class Test_C2989783_Ladbrokes_Verify_Greyhounds_Specials_EDP_view(Common):
    """
    TR_ID: C2989783
    NAME: [Ladbrokes] Verify Greyhounds Specials EDP view
    DESCRIPTION: This test case verifies Navigation and View of Greyhounds Specials EDP page
    PRECONDITIONS: To retrieve an information from the Site Server (tst2) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/*X.XX */EventToOutcomeForClass/227?translationLang=LL
    PRECONDITIONS: Where X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Class id = *id* for Racing Specials class ('Specials' checkbox should be checked in Flags on Type and Class level)
    PRECONDITIONS: **The full request to check data:**
    PRECONDITIONS: Ladbrokes
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/198,201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T14:17:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: Coral
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-26T00:00:00.000Z&simpleFilter=event.startTime:lessThan:2020-08-27T00:00:00.000Z&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T13:35:30.000Z&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_navigate_to_greyhounds_gt_specials_tab(self):
        """
        DESCRIPTION: Navigate to Greyhounds &gt; Specials tab
        EXPECTED: 
        """
        pass

    def test_002_click_on_some_event_in_specials_accordion(self):
        """
        DESCRIPTION: Click on some event in Specials accordion
        EXPECTED: User is navigated to Specials EDP
        """
        pass

    def test_003_verify_specials_edp_view(self):
        """
        DESCRIPTION: Verify Specials EDP view
        EXPECTED: Header:
        EXPECTED: - Event name and time displayed. Time in Format "Day-of-the-week Date Month Year"
        EXPECTED: Market section:
        EXPECTED: - Header with Market name expandable/collapsible
        EXPECTED: - Selections with prices displayed under header. No silks or runner numbers.
        """
        pass
