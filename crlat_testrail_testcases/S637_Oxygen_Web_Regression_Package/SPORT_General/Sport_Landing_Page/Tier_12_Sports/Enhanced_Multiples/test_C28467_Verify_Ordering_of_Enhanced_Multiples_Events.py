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
class Test_C28467_Verify_Ordering_of_Enhanced_Multiples_Events(Common):
    """
    TR_ID: C28467
    NAME: Verify Ordering of Enhanced Multiples Events
    DESCRIPTION: This test case verifies Ordering of Enhanced Multiples Events.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: **NOTE: Make sure you have  Enhanced Multiples events on Some sports (Sport events with typeName="Enhanced Multiples").**
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. For each Class retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XXX - is a comma separated list of **Class **ID's;
    PRECONDITIONS: *   XX - sports **Category **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH).
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. For each Type retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&translationLang=LL&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: *   XXX - is a comma separated list of **Type **ID's;
    PRECONDITIONS: *   XX - sports **Category **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH)
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 4. In order to check particular event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_any_ltsportsgt_page_where_enhanced_multiples_events_are_present(self):
        """
        DESCRIPTION: Navigate to any &lt;Sports&gt; page where Enhanced Multiples events are present
        EXPECTED: **Desktop**:
        EXPECTED: *  &lt;Sport&gt; Landing Page is opened
        EXPECTED: * 'Matches'-&gt;'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  &lt;Sport&gt; Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_go_to_enhanced_multiples_section_for_mobiletablet_and_carousel_for_desktop(self):
        """
        DESCRIPTION: Go to 'Enhanced Multiples' section for **Mobile/Tablet** and carousel for **Desktop**
        EXPECTED: 
        """
        pass

    def test_004_verify_em_outcomes_ordering_within_section_for_mobiletablet_and_carousel_for_desktop(self):
        """
        DESCRIPTION: Verify EM Outcomes ordering within section for **Mobile/Tablet** and carousel for **Desktop**
        EXPECTED: **For Mobile**
        EXPECTED: EM Outcomes are ordered by:
        EXPECTED: *   by **StartTime** in ascending of the events they belong to
        EXPECTED: *   if StartTime the same then by selections displayOrder
        EXPECTED: *   if StartTime and displayOrder are the same than **Alphabetically**
        EXPECTED: **For desktop**
        EXPECTED: EM Outcomes are ordered by:
        EXPECTED: *   by **StartTime** in ascending of the events they belong to
        """
        pass

    def test_005_clicktap_on_enhanced_multiples_tab_from_module_selector_ribbon_on_the_homepage(self):
        """
        DESCRIPTION: Click/Tap on 'Enhanced Multiples' tab from Module Selector Ribbon on the Homepage
        EXPECTED: **For mobile/tablet:**
        EXPECTED: *   'Enhanced Multiples' tab is opened
        EXPECTED: *   All sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand section
        EXPECTED: **For desktop:**
        EXPECTED: 'Enhanced Multiples' are displayed in carousel below banner area
        """
        pass

    def test_006_verify_em_outcomes_ordering_within_section_within_the_same_category(self):
        """
        DESCRIPTION: Verify EM Outcomes ordering within section (within the same Category)
        EXPECTED: EM Outcomes are ordered by:
        EXPECTED: *   by **StartTime **in ascending of the events they belong to
        EXPECTED: *   if StartTime the same then by selections displayOrder
        EXPECTED: *   if StartTime and displayOrder are the same than **Alphabetically**
        """
        pass

    def test_007_for_desktoprepeat_steps_3_4_on_ltsportsgt_event_details_page_but_only_for_pre_match_events(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 3-4 on &lt;Sports&gt; Event Details Page but only for Pre-match events
        EXPECTED: 
        """
        pass
