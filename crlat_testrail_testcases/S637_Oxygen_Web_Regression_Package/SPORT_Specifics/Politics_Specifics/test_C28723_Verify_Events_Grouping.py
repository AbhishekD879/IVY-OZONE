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
class Test_C28723_Verify_Events_Grouping(Common):
    """
    TR_ID: C28723
    NAME: Verify Events Grouping
    DESCRIPTION: This test case verifies events grouping
    PRECONDITIONS: 1. In order to get a list with **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID (Politics = 46)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. For each **Class **retrieve a list of Event IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?simpleFilter=market.siteChannels:contains:M&translationLang=LL&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: *   XXX - is a comma separated list of **Class **ID's;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. For each **Type **retrieve a list of Event IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?simpleFilter=market.siteChannels:contains:M&translationLang=LL&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: *   XXX - is a comma separated list of **Type **ID's;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tappolitics_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Politics' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop:**
        EXPECTED: *   Politics Landing Page is opened
        EXPECTED: *   'Today' tab is opened by default
        EXPECTED: *   'By Competitions' sorting type is chosen by default
        EXPECTED: **Mobile:**
        EXPECTED: * Politics Landing Page (single view) is opened
        EXPECTED: * All available events for this sport are displayed on 1 page
        EXPECTED: * Available modules (in-play/upcoming) and sections (outrights/specials) are displayed one below another
        """
        pass

    def test_003_verify_events_grouping(self):
        """
        DESCRIPTION: Verify event's grouping
        EXPECTED: Events are grouped by '**classId**' and '**typeId'**
        """
        pass

    def test_004_tap_tomorrow_tab_desktop(self):
        """
        DESCRIPTION: Tap 'Tomorrow' tab (Desktop)
        EXPECTED: *   'Tomorrow' tab is opened
        EXPECTED: *   'By Competitions' sorting type is chosen by default
        """
        pass

    def test_005_verify_events_grouping(self):
        """
        DESCRIPTION: Verify event's grouping
        EXPECTED: Events are grouped by '**classId**' and '**typeId'**
        """
        pass

    def test_006_tap_future_tab_desktop(self):
        """
        DESCRIPTION: Tap 'Future' tab (Desktop)
        EXPECTED: *   'Future' tab is opened
        EXPECTED: *   'By Competitions' sorting type is chosen by default
        """
        pass

    def test_007_verify_events_grouping(self):
        """
        DESCRIPTION: Verify event's grouping
        EXPECTED: Events are grouped by '**classId**' and '**typeId'**
        """
        pass

    def test_008_tap_outrights_tab_desktop(self):
        """
        DESCRIPTION: Tap 'Outrights' tab (Desktop)
        EXPECTED: *   'Outrights' tab is opened
        EXPECTED: *   'By Competitions' sorting type is chosen by default
        """
        pass

    def test_009_verify_events_grouping(self):
        """
        DESCRIPTION: Verify event's grouping
        EXPECTED: Events are grouped by '**classId**' and '**typeId'**
        """
        pass
