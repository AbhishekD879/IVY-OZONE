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
class Test_C2989745_Ladbrokes_Verify_Horse_Racing_Specials_EDP_view(Common):
    """
    TR_ID: C2989745
    NAME: [Ladbrokes] Verify Horse Racing Specials EDP view
    DESCRIPTION: This test case verifies Navigation and View of Horse Racing Specials EDP page
    PRECONDITIONS: To retrieve an information from the Site Server use the following link:
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/226,223?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-07-30T12:08:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: limitRecords=outcome:1&limitRecords=market:1 - filter just for Ladbrokes brand, since outcomes (selections/odds) are not shown on 'Specials' tab there.
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing__specials_tab(self):
        """
        DESCRIPTION: Navigate to Horse Racing > Specials tab
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
