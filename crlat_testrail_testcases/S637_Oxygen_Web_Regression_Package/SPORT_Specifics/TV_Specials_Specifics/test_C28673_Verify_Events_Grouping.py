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
class Test_C28673_Verify_Events_Grouping(Common):
    """
    TR_ID: C28673
    NAME: Verify Events Grouping
    DESCRIPTION: This test case verifies events grouping
    PRECONDITIONS: 1. In order to get a list with **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - **Category **ID (TV Specials=48)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. For each **Class **retrieve a list of Event IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?simpleFilter=market.siteChannels:contains:M&translationLang=LL&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: *   XXX - is a comma separated list of **Class **ID's;
    PRECONDITIONS: *   XX - sports **Category **ID (TV Specials=48)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. For each **Type **retrieve a list of Event IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?simpleFilter=market.siteChannels:contains:M&translationLang=LL&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: *   XXX - is a comma separated list of **Type **ID's;
    PRECONDITIONS: *   XX - sports **Category **ID (TV Specials =48)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_taptv_specials_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'TV Specials' icon on the Sports Menu Ribbon
        EXPECTED: Desktop:
        EXPECTED: * TV Specials Landing Page is opened
        EXPECTED: * '**Events**' tab is opened by default
        EXPECTED: * First **three **sections are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: Mobile:
        EXPECTED: * TV Specials Landing Page (single view) is opened
        EXPECTED: * All available events for this sport are displayed on 1 page
        EXPECTED: * Available modules (in-play/upcoming) and sections (outrights/specials) are displayed one below another
        """
        pass

    def test_003_verify_events_grouping(self):
        """
        DESCRIPTION: Verify event's grouping
        EXPECTED: Events are grouped by **'classId'** and '**typeId'**
        """
        pass

    def test_004_tap_tomorrow_tab_for_desktop_only(self):
        """
        DESCRIPTION: Tap 'Tomorrow' tab (for desktop only)
        EXPECTED: 'Tomorrow' tab is opened
        """
        pass

    def test_005_verify_events_grouping(self):
        """
        DESCRIPTION: Verify event's grouping
        EXPECTED: Events are grouped by **'classId'** and '**typeId'**
        """
        pass

    def test_006_tap_future_tab_for_desktop_only(self):
        """
        DESCRIPTION: Tap 'Future' tab (for desktop only)
        EXPECTED: 'Future' tab is opened
        """
        pass

    def test_007_verify_events_grouping(self):
        """
        DESCRIPTION: Verify event's grouping
        EXPECTED: Events are grouped by **'classId'** and '**typeId'**
        """
        pass

    def test_008_tap_outrights_tab_outrights_section_for_mobile(self):
        """
        DESCRIPTION: Tap 'Outrights' tab (outrights section for mobile)
        EXPECTED: 'Outrights' tab is opened
        """
        pass

    def test_009_verify_events_grouping(self):
        """
        DESCRIPTION: Verify event's grouping
        EXPECTED: Events are grouped by **'classId'** and '**typeId'**
        """
        pass
