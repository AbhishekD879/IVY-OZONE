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
class Test_C28466_Verify_Filtering_of_Enhanced_Multiples_Events(Common):
    """
    TR_ID: C28466
    NAME: Verify Filtering of Enhanced Multiples Events
    DESCRIPTION: This test case verifies Filtering of Enhanced Multiples Events.
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
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
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

    def test_003_verifyenhanced_multiples_section(self):
        """
        DESCRIPTION: Verify 'Enhanced Multiples' section
        EXPECTED: * Expanded 'Enhanced Multiples' section is shown at the top of the 'Type' accordions with Event list for **Mobile/Tablet**
        EXPECTED: * 'Enhanced Multiples' is displayed in carousel below banner area for **Desktop**
        EXPECTED: * Section contains EM outcomes
        """
        pass

    def test_004_verify_present_em_outcomes(self):
        """
        DESCRIPTION: Verify present EM Outcomes
        EXPECTED: EM outcomes are shown due to the following rules:
        EXPECTED: *   Just outcomes of events with attribute **typeName="Enhanced Multiples****" **are shown
        EXPECTED: *   Just outcomes of events with **NO isStarted="true"** attribute are shown
        EXPECTED: *   **Each outcome is shown separately **(of events with more then one market and more than one outcome, of  events one market and more than one outcome, of  events with one market and one outcome)
        """
        pass

    def test_005_navigate_to_any_ltsportsgt_page_where_enhanced_multiples_events_are_not_present(self):
        """
        DESCRIPTION: Navigate to any &lt;Sports&gt; page where Enhanced Multiples events are NOT present
        EXPECTED: **Desktop**:
        EXPECTED: *  &lt;Sport&gt; Landing Page is opened
        EXPECTED: * 'Matches'-&gt;'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  &lt;Sport&gt; Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_006_verify_presence_of_enhanced_multiples_section_for_mobiletablet_and_carousel_for_desktop(self):
        """
        DESCRIPTION: Verify presence of  'Enhanced Multiples' section for **Mobile/Tablet** and carousel for **Desktop**
        EXPECTED: 'Enhanced Multiples' section for **Mobile/Tablet** and carousel for **Desktop** is NOT shown
        """
        pass

    def test_007_repeat_steps_3_6_for_tomorrow_tab_for_desktoptablet(self):
        """
        DESCRIPTION: Repeat steps 3-6 for 'Tomorrow' tab for Desktop/Tablet
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_3_6_for_future_tab_for_desktoptablet(self):
        """
        DESCRIPTION: Repeat steps 3-6 for 'Future' tab for Desktop/Tablet
        EXPECTED: 
        """
        pass

    def test_009_for_desktoprepeat_steps_3_6_on_ltsportsgt_event_details_page_but_only_for_pre_match_events(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 3-6 on &lt;Sports&gt; Event Details Page but only for Pre-match events
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_3_6_on_home_page(self):
        """
        DESCRIPTION: Repeat steps 3-6 on Home page
        EXPECTED: **For mobile/tablet:**
        EXPECTED: *   'Enhanced Multiples' are displayed in sections within  'Enhanced Multiples' tab
        EXPECTED: *   All sections are collapsed by default
        EXPECTED: **For desktop:**
        EXPECTED: 'Enhanced Multiples' are displayed in carousel below banner area
        """
        pass
