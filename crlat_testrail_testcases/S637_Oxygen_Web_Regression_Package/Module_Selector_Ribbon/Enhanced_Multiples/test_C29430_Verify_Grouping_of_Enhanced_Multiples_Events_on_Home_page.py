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
class Test_C29430_Verify_Grouping_of_Enhanced_Multiples_Events_on_Home_page(Common):
    """
    TR_ID: C29430
    NAME: Verify Grouping of Enhanced Multiples Events on Home page
    DESCRIPTION: This test case verifies Grouping of Enhanced Multiples Events on Home page
    DESCRIPTION: Test case to be run on mobile, tablet and desktop.
    PRECONDITIONS: **NOTE:** The events for Enhanced Multiples should be determined by the **drilldownTagNames="EVFLAG_ES****" **in the SiteServer query.
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
    PRECONDITIONS: **From OX 107:**
    PRECONDITIONS: **The full request to check Enhanced Multiples data:**
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/227?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.typeName:equals:|Enhanced%20Multiples|&simpleFilter=event.suspendAtTime:greaterThan:2020-08-28T11:32:30.000Z&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_enhanced_multiples_tab_from_module_selector_ribbon(self):
        """
        DESCRIPTION: Tap 'Enhanced Multiples' tab from Module Selector Ribbon
        EXPECTED: **For mobile/tablet:**
        EXPECTED: *   'Enhanced Multiples' tab is opened
        EXPECTED: *   All sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand section
        EXPECTED: **For desktop:**
        EXPECTED: 'Enhanced Multiples' are displayed in carousel below banner area
        """
        pass

    def test_003_for_mobiletabletexpandcollapse_all_sections(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: Expand/collapse all sections
        EXPECTED: * It is possible to expand/collapse every section
        EXPECTED: * Each expanded section contains valid data
        EXPECTED: * There are NO empty sections
        """
        pass

    def test_004_verify_enhanced_multiples_outcomes_grouping(self):
        """
        DESCRIPTION: Verify Enhanced Multiples Outcomes grouping
        EXPECTED: Enhanced Multiples Outcomes are grouped by **CategoryID**
        """
        pass

    def test_005_verify_section_names(self):
        """
        DESCRIPTION: Verify section names
        EXPECTED: **For mobile/tablet:**
        EXPECTED: Sections are titled based on **CategoryName**
        EXPECTED: **For desktop:**
        EXPECTED: **CategoryName** is displayed on each 'Enhanced Multiples' card next to 'Enhanced' label
        """
        pass

    def test_006_verify_sections_order(self):
        """
        DESCRIPTION: Verify sections order
        EXPECTED: **For mobile/tablet:**
        EXPECTED: Sections are ordered by the **Category displayOrder** in ascending
        EXPECTED: **For desktop:**
        EXPECTED: 'Enhanced Multiples' are displayed in carousel ordered by the **Category displayOrder** in ascending
        """
        pass
