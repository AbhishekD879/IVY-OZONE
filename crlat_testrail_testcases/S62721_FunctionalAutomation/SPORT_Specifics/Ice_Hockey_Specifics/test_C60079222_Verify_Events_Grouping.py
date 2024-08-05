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
class Test_C60079222_Verify_Events_Grouping(Common):
    """
    TR_ID: C60079222
    NAME: Verify Events Grouping
    DESCRIPTION: This test case verifies events grouping
    PRECONDITIONS: 1. In order to get a list with **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID (Ice Hockey=22)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. For each **Class **retrieve a list of Event IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&translationLang=LL&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: *   XXX - is a comma separated list of **Class **ID's;
    PRECONDITIONS: *   XX - sports **Category **ID (Ice Hockey=22)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Ice Hockey-HH).
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. For each **Type **retrieve a list of Event IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&translationLang=LL&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: *   XXX - is a comma separated list of **Type **ID's;
    PRECONDITIONS: *   XX - sports **Category **ID (Ice Hockey=22)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g.Ice Hockey-HH).
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapice_hockey_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Ice Hockey' icon on the Sports Menu Ribbon
        EXPECTED: *   Ice Hockey Landing Page is opened
        EXPECTED: *   '**Matches**'->'**Today**' tab is opened by default (for desktop)/ 'Matches' tab is opened (for mobile)
        """
        pass

    def test_003_go_to_leagues_section_and_verify_events_grouping(self):
        """
        DESCRIPTION: Go to Leagues section and verify event's grouping
        EXPECTED: Events are grouped by **'classId' **and '**typeId'**
        """
        pass

    def test_004_tap_tomorrow_tab_for_desktop_only(self):
        """
        DESCRIPTION: Tap '**Tomorrow**' tab (for desktop only)
        EXPECTED: 'Tomorrow' tab is opened
        """
        pass

    def test_005_go_to_leagues_section_and_verify_events_grouping(self):
        """
        DESCRIPTION: Go to Leagues section and verify event's grouping
        EXPECTED: Events are grouped by **'classId' **and '**typeId'**
        """
        pass

    def test_006_tap_future_tab_for_destop_only(self):
        """
        DESCRIPTION: Tap '**Future**' tab (for destop only)
        EXPECTED: 'Future' tab is opened
        """
        pass

    def test_007_go_to_leagues_section_and_verify_events_grouping(self):
        """
        DESCRIPTION: Go to Leagues section and verify event's grouping
        EXPECTED: Events are grouped by **'classId' **and '**typeId'**
        """
        pass

    def test_008_tap_outrights_tab(self):
        """
        DESCRIPTION: Tap '**Outrights**' tab
        EXPECTED: 'Outrights' tab is opened
        """
        pass

    def test_009_go_to_leagues_sectionand_verify_events_grouping(self):
        """
        DESCRIPTION: Go to Leagues section and verify event's grouping
        EXPECTED: Events are grouped by **'classId' **and '**typeId'**
        """
        pass
