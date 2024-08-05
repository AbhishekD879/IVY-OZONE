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
class Test_C9608032_Verify_layout_of_Next_Races_tab_on_Horse_Racing_Landing_Page(Common):
    """
    TR_ID: C9608032
    NAME: Verify layout of 'Next Races' tab on Horse Racing Landing Page
    DESCRIPTION: This test case verifies layout of 'Next Races' tab on Horse Racing Landing Page
    PRECONDITIONS: 1. "Next Races" tab should be enabled in CMS(CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=true)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: 4. Navigate to Horse Racing
    PRECONDITIONS: *Note:*
    PRECONDITIONS: 1) The number of events and selections are CMS configurable. CMS -> system-configuration -> structure -> NextRaces.
    PRECONDITIONS: 2) To get info about class for SiteServer use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&existsFilter=event:simpleFilter:market.name:equals:%7CWin%20or%20Each%20Way%7C&simpleFilter=market.name:equals:%7CWin%20or%20Each%20Way%7C&priceHistory=true&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&racingForm=outcome&limitRecords=outcome:3&simpleFilter=event.siteChannels:contains:M&simpleFilter=outcome.outcomeStatusCode:equals:A&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&translationLang=en
    PRECONDITIONS: Where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    """
    keep_browser_open = True

    def test_001_tap_on_next_races_tab(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab
        EXPECTED: * 'Next Races' tab is selected and highlighted
        EXPECTED: * Content is loaded
        """
        pass

    def test_002_verify_next_races_tab_layout(self):
        """
        DESCRIPTION: Verify 'Next Races' tab layout
        EXPECTED: * 'Extra Place' section is displayed at the top of the page (if Extra Place racing events are available)
        EXPECTED: * Event cards are displayed one by one as the list (The number of events depends on CMS configurations)
        """
        pass

    def test_003_verify_live_serve_updated_for_next_races_events(self):
        """
        DESCRIPTION: Verify Live serve updated for Next races events
        EXPECTED: - Selection suspension/price update is displayed in Next races widget
        EXPECTED: - Market suspension/price update is displayed in Next races widget
        EXPECTED: - Event suspension/unsuspension is displayed in Next races widget
        """
        pass
