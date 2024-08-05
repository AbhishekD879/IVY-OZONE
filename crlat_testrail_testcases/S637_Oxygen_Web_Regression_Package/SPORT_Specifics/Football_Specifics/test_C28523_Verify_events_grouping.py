import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28523_Verify_events_grouping(Common):
    """
    TR_ID: C28523
    NAME: Verify events grouping
    DESCRIPTION: This test case verifies event grouping
    PRECONDITIONS: 1. In order to get a list with Classes IDs and Types IDs use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: XX - sports Category ID (Football=16)
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. For each Class retrieve a list of Event IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&translationLang=LL&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: XXX - is a comma separated list of Class ID's;
    PRECONDITIONS: XX - sports Category ID (Football=16)
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football-MR).
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. For each Type retrieve a list of Event IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&translationLang=LL&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: XXX - is a comma separated list of Type ID's;
    PRECONDITIONS: XX - sports Category ID (Football=16)
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football-MR).
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_verify_events_grouping_on_todays_page_desktoptablet(self):
        """
        DESCRIPTION: Verify event's grouping on Today's page (Desktop/Tablet)
        EXPECTED: * Events are grouped by **classId** and **typeId**
        EXPECTED: * First **three** accordions are expanded by default
        EXPECTED: * The remaining accordions are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the accordions by clicking the accordion's header
        EXPECTED: * If no events to show, the message **No events found** is displayed
        """
        pass

    def test_004_verify_accordions_headers_titles(self):
        """
        DESCRIPTION: Verify accordions header's titles
        EXPECTED: The accordion header titles are in the following format and corresponds to the attributes:
        EXPECTED: **className** (sport name is not displayed) + **-** + **typeName**
        """
        pass

    def test_005_verify_leagues_accordions_order(self):
        """
        DESCRIPTION: Verify Leagues accordions order
        EXPECTED: Leagues accordions are ordered by:
        EXPECTED: 1.  Class **displayOrder ** in ascending order where minus ordinals are displayed first
        EXPECTED: 2.  Type **displayOrder ** in ascending order
        """
        pass

    def test_006_verify_events_order_in_the_league_accordion(self):
        """
        DESCRIPTION: Verify events order in the League accordion
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1.  **startTime** - chronological order in the first instance
        EXPECTED: 2.  **Event displayOrder** in ascending
        EXPECTED: 3.  **Alphabetical order**
        """
        pass

    def test_007_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: * 'Matches' page is loaded
        EXPECTED: * 'Coupons' switcher is selected by default and highlighted
        EXPECTED: * List of matches and coupons is displayed below the 'Coupons' and 'Competitions' switchers
        """
        pass

    def test_008_repeat_steps_3_7_for_tomorrows_matches_desktoptablet(self):
        """
        DESCRIPTION: Repeat steps 3-7 for Tomorrow's matches (Desktop/Tablet)
        EXPECTED: * Events are grouped by **classId** and **typeId**
        EXPECTED: * First **three** accordions are expanded by default
        EXPECTED: * The remaining accordions are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the accordions by clicking the accordion's header
        EXPECTED: * If no events to show, the message **No events found** is displayed
        """
        pass

    def test_009_repeat_steps_3_7_for_future_matches_desktoptablet(self):
        """
        DESCRIPTION: Repeat steps 3-7 for Future matches (Desktop/Tablet)
        EXPECTED: * Events are grouped by **classId** and **typeId**
        EXPECTED: * First **three** accordions are expanded by default
        EXPECTED: * The remaining accordions are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the accordions by clicking the accordion's header
        EXPECTED: * If no events to show, the message **No events found** is displayed
        """
        pass

    def test_010_repeat_steps_3_7_for_outrights(self):
        """
        DESCRIPTION: Repeat steps 3-7 for Outrights
        EXPECTED: * Events are grouped by **classId** and **typeId**
        """
        pass
