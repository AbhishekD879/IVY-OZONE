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
class Test_C28928_Event_Section_Displaying(Common):
    """
    TR_ID: C28928
    NAME: Event Section Displaying
    DESCRIPTION: This test case verifies event section content displaying on 'Special' tab
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   BMA-8961 Horse Racing Specials Tab
    DESCRIPTION: *   BMA-24371 HR Specials: Re-design
    DESCRIPTION: AUTOTEST: [C1688636]
    PRECONDITIONS: Request to check data:
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/226,223?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-07-30T12:08:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: limitRecords=outcome:1&limitRecords=market:1 - filter just for Ladbrokes brand, since outcomes (selections/odds) are not shown on 'Specials' tab there.
    """
    keep_browser_open = True

    def test_001_tap_horse_racing_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Horse Racing' icon on the Sports Menu Ribbon
        EXPECTED: 'Horse Racing' landing page is opened
        """
        pass

    def test_002_click__tap_specials_tab(self):
        """
        DESCRIPTION: Click / tap 'Specials' tab
        EXPECTED: 'Specials' tab is opened
        """
        pass

    def test_003_open__check_particular_event_section(self):
        """
        DESCRIPTION: Open / check particular event section
        EXPECTED: Events which are related to particular type are shown
        """
        pass

    def test_004_verify_events_ordering(self):
        """
        DESCRIPTION: Verify events ordering
        EXPECTED: Events are ordered by race local time  within one section
        """
        pass

    def test_005_verify_event_section_displaying(self):
        """
        DESCRIPTION: Verify event section displaying
        EXPECTED: *   First event section within first Competitions accordion is expanded by default
        EXPECTED: *   All other event sections are collapsed by default
        EXPECTED: *   Event section is expandable / collapsible
        EXPECTED: *   For mobile:
        EXPECTED: *   Maximum 4 selections are displayed within event section
        EXPECTED: *   'Show all' button is present if there are more than 4 selections within events section
        """
        pass

    def test_006_verify_show_all_button(self):
        """
        DESCRIPTION: Verify 'Show all' button
        EXPECTED: All available selections are present after clicking / tapping 'Show all' button
        """
        pass

    def test_007_verify_event_section_displayingfor_desktop(self):
        """
        DESCRIPTION: Verify event section displaying for Desktop
        EXPECTED: Maximum 9 selections are displayed within event section for 1600 and 1280px screen resolutions
        EXPECTED: *   'Show More' button is present if there are more than 9 selections within events section for 1600 and 1280px screen resolutions
        EXPECTED: *  Maximum 8 selections in two rows are displayed within event section for 1025 and 970px screen resolutions
        EXPECTED: * *   'Show More' button is present if there are more than 8 selections within events section for 1025 and 970px screen resolutions
        """
        pass
