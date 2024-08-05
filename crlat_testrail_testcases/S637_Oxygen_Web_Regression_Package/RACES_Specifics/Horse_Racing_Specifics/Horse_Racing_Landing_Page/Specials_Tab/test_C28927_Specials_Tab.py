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
class Test_C28927_Specials_Tab(Common):
    """
    TR_ID: C28927
    NAME: 'Specials' Tab
    DESCRIPTION: This test case verifies 'Specials' tab on horse Racing landing page
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   BMA-8961 Horse Racing Specials Tab
    DESCRIPTION: *   BMA_22884 Horse Racing - Add bet filter to all horse racing pages
    DESCRIPTION: AUTOTEST: [C1684489]
    PRECONDITIONS: To retrieve an information from the Site Server use the following link:
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/226,223?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-07-30T12:08:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: limitRecords=outcome:1&limitRecords=market:1 - filter just for Ladbrokes brand, since outcomes (selections/odds) are not shown on 'Specials' tab there.
    PRECONDITIONS: See attributes:
    PRECONDITIONS: *   Horse Racing **categoryId**=21
    PRECONDITIONS: *   **'typeName'** on event level to identify needed event types to be displayed on the application
    PRECONDITIONS: *   **'display order' **on type level to identify order of competitions displaying
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

    def test_003_click__tap_specials_tab(self):
        """
        DESCRIPTION: Click / tap 'Specials' tab
        EXPECTED: 'Specials' tab is opened
        """
        pass

    def test_004_verify_competition_section_displaying(self):
        """
        DESCRIPTION: Verify competition section displaying
        EXPECTED: *   All competitions are expanded by default;
        EXPECTED: *   All competitions are collapsible, expandable.
        """
        pass

    def test_005_verify_competition_section_name(self):
        """
        DESCRIPTION: Verify competition section name
        EXPECTED: Competition section name corresponds to **'typeName'** attribute in response from SiteServer
        """
        pass

    def test_006_verify_competition_section_ordering(self):
        """
        DESCRIPTION: Verify competition section ordering
        EXPECTED: - Competition sections are ordered by **display order **in ascending order** **on type level
        EXPECTED: - Alphabetical order in second instance if display order is the same on type level
        """
        pass

    def test_007_verify_long_selection_names(self):
        """
        DESCRIPTION: Verify long selection names
        EXPECTED: Long selection names are wrapped
        """
        pass
