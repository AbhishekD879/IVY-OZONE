import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28448_Verify_Data_Filtering(Common):
    """
    TR_ID: C28448
    NAME: Verify Data Filtering
    DESCRIPTION: This test case verifies data filtering
    PRECONDITIONS: 1. In order to get a list with **Classes IDs **and **Leagues Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. For each Type retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&translationLang=LL&existsFilter=event:simpleFilter:market.isActive&simpleFilter=event.startTime:lessThan:YYYY2-MM2-DD2T00:00:00Z&simpleFilter=event.startTime:greaterThanOrEqual:YYYY1-MM1-DD1T00:00:00Z
    PRECONDITIONS: *   XXX -  is a comma separated list of **Type **ID's;
    PRECONDITIONS: *   YYYY1-MM1-DD1 - is Today's date
    PRECONDITIONS: *   YYYY2-MM2-DD2 - is the Tomorrow's date
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH).
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: **Desktop**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_verify_cash_out_icon(self):
        """
        DESCRIPTION: Verify 'Cash Out' icon
        EXPECTED: 'CASH OUT' icon is shown if at least one of it's events has cashoutAvail="Y
        EXPECTED: For mobile/tablet view:
        EXPECTED: 'Cash out' icon is shown next to Type name
        EXPECTED: For desktop view:
        EXPECTED: 'Cash out' icon is shown on the right side, before expand/collapse accordion arrow
        """
        pass

    def test_004_verify_the_list_of_events(self):
        """
        DESCRIPTION: Verify the list of events
        EXPECTED: Only Today's events are displayed (Event Start Time is today's date/time)
        """
        pass

    def test_005_note_number_of_todays_events_present_on_today_tab_for_desktop(self):
        """
        DESCRIPTION: Note number of Today's events present on Today tab (for Desktop)
        EXPECTED: 
        """
        pass

    def test_006_verify_number_of_todays_events_on_response_from_siteserver(self):
        """
        DESCRIPTION: Verify number of Today's events on response from SiteServer
        EXPECTED: Number of events matches with number of events from the previous step
        """
        pass
