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
class Test_C28926_Specials_Tab_when_there_are_no_specials_events_available(Common):
    """
    TR_ID: C28926
    NAME: 'Specials' Tab when there are no specials events available
    DESCRIPTION: This test case verifies 'Specials' tab when there are no specials events available
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   BMA-8961 Horse Racing Specials Tab
    PRECONDITIONS: Make sure that there are no available specials events
    PRECONDITIONS: No events available with drilldownTagNames=MKTFLAG_SP
    PRECONDITIONS: To retrieve an information from the Site Server use the following link:
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/226,223?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-07-30T12:08:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: limitRecords=outcome:1&limitRecords=market:1 - filter just for Ladbrokes brand, since outcomes (selections/odds) are not shown on 'Specials' tab there.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_click__tap_horse_racing_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Click / tap 'Horse Racing' icon on the Sports Menu Ribbon
        EXPECTED: 'Horse Racing' landing page is opened
        """
        pass

    def test_003_verify_specials_tab(self):
        """
        DESCRIPTION: Verify 'Specials' tab
        EXPECTED: 'Specials' tab is NOT shown in app
        """
        pass
