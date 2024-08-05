import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C117012_Verify_availability_of_Sport_Tabs_in_Sports_Menu_Ribbon_on_In_Play_page(Common):
    """
    TR_ID: C117012
    NAME: Verify availability of Sport Tabs in Sports Menu Ribbon on 'In-Play' page
    DESCRIPTION: This test case verifies conditions under which Sport Tabs are displayed in Sports Menu Ribbon on 'In-Play' page
    DESCRIPTION: To be run on Mobile, Tablet and Desktop.
    PRECONDITIONS: 1) To get Sports which have 'Live Now' events:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:intersects:16,34,51,5,6,24,18,22,31,30,32,23,55,26,28,25,1,9,10,13,48,46,20,3,54,36,8,35,12,42,53,21,19,39,61,104,103,65,82,97,2,52,72,80,29,99,50,59,154,37,110,105,87,108,79,7,149,16,34,51,6,18,9,20,54,36,12,61,104,103,65,82,97,2,52,72,80,29,99,50,59,154,37,110,105,87,108,79,7,149&existsFilter=class:simpleFilter:event.drilldownTagNames:intersects:EVFLAG_BL&existsFilter=class:simpleFilter:event.siteChannels:contains:M&simpleFilter=class.siteChannels:contains:M&existsFilter=class:simpleFilter:event.isLiveNowEvent&simpleFilter=class.hasLiveNowEvent&translationLang=LL
    PRECONDITIONS: 2) To get Sports which have 'Upcoming' events:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.22/Class?simpleFilter=class.categoryId:intersects:16,34,51,5,6,24,18,22,31,30,32,23,55,26,28,25,1,9,10,13,48,46,20,3,54,36,8,35,12,42,53,21,19,39,61,104,103,65,82,97,2,52,72,80,29,99,50,59,154,37,110,105,87,108,79,7,149,16,34,51,6,18,9,20,54,36,12,61,104,103,65,82,97,2,52,72,80,29,99,50,59,154,37,110,105,87,108,79,7,149&existsFilter=class:simpleFilter:event.drilldownTagNames:intersects:EVFLAG_BL&existsFilter=class:simpleFilter:event.siteChannels:contains:M&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasNext24HourEvent&existsFilter=class:simpleFilter:event.isNext24HourEvent&translationLang=LL
    PRECONDITIONS: 3) To get events for particular class ID:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.22/EventToOutcomeForClass/XXX?&translationLang=en
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXX - class ID
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_for_mobiletablettap_in_play_icon_on_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: **For Mobile/Tablet: **
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: *   'In-Play' Landing Page is opened
        EXPECTED: *   Sports Menu Ribbon is shown with Categories where In-Play events are available
        EXPECTED: *   First &lt;Sport&gt; tab is opened by default
        EXPECTED: *   Two filter switchers are visible: 'Live Now' and 'Upcoming'
        """
        pass

    def test_003_for_mobiletabletverify_sport_tabs_filtering(self):
        """
        DESCRIPTION: **For Mobile/Tablet: **
        DESCRIPTION: Verify Sport tabs filtering
        EXPECTED: Each unique Sport Tab is displayed in Sports Menu Ribbon only if at least one class for the corresponding category has the following attributes:
        EXPECTED: *   Class's attribute 'siteChannels' contains 'M'
        EXPECTED: *   Class's attribute hasLiveNowEvent="true" OR hasNext24HourEvent="true"
        EXPECTED: *   At least one event in the class has attribute 'siteChannels' that contains 'M'
        EXPECTED: *   At least one event in the class contains attribute drilldownTagNames="EVFLAG_BL"
        EXPECTED: *   At least one event in the class contains attribute isLiveNowEvent="true" OR isNext24HourEvent="true"
        """
        pass

    def test_004_for_desktopnavigate_to_in_play__live_stream_section_on_homepage_and_verify_sport_tabs_filtering(self):
        """
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section on Homepage and verify Sport tabs filtering
        EXPECTED: Each unique Sport Tab is displayed in Sports Menu Ribbon only if at least one class for the corresponding category has the following attributes:
        EXPECTED: *   Class's attribute 'siteChannels' contains 'M'
        EXPECTED: *   Class's attribute hasLiveNowEvent="true"
        EXPECTED: *   At least one event in the class has attribute 'siteChannels' that contains 'M'
        EXPECTED: *   At least one event in the class contains attribute drilldownTagNames="EVFLAG_BL"
        EXPECTED: *   At least one event in the class contains attribute isLiveNowEvent="true"
        """
        pass
