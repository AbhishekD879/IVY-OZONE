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
class Test_C10530954_Verify_data_filtering_and_arrangement_order(Common):
    """
    TR_ID: C10530954
    NAME: Verify data filtering and arrangement order
    DESCRIPTION: This test case verifies data filtering and arrangement order of event and league data on 'Outrights' page and EDP for Outright events.
    PRECONDITIONS: 1) Following Tabs should be enabled in Sports Pages - SPORT CATEGORIES - #TIER_2_SPORT_NAME within CMS: Matches, Competitions, Outrights
    PRECONDITIONS: 2) Chosen TIER_2_SPORT should contain: League #1 with 1 Live(and Active) and 1 Upcoming('Start Time' value = '00:00 AM Current Date' + 47H:55M) 'Outright' events; League #2 with 1 Upcoming('Start Time' value = '00:00 AM Current Date' + 23H:55M) 'Outright' events
    PRECONDITIONS: 3) Each aforementioned event should have an 'Outright' market; 'Live' aforementioned event should have 2 'Outright' markets with different names and Disporders.
    PRECONDITIONS: 4) Load Oxygen app
    PRECONDITIONS: 5) Navigate to a chosen 'Tier 2' Sports Landing Page
    PRECONDITIONS: In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: +
    PRECONDITIONS: For each Class retrieve a list of **Event **IDs use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: XXX - is a comma separated list of **Class **ID's;
    PRECONDITIONS: +
    PRECONDITIONS: For each Type retrieve a list of **Event **IDs use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&translationLang=LL&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: XXX - is a comma separated list of **Type **ID's;
    PRECONDITIONS: ---
    PRECONDITIONS: XX - sports **Category **ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH).
    """
    keep_browser_open = True

    def test_001_switch_to_outrights_tab(self):
        """
        DESCRIPTION: Switch to 'Outrights' tab
        EXPECTED: League dropdowns(lanes) are shown below the 'Tabs' lane
        EXPECTED: Leagues arrangement order is based on hierarchy sorting rules that account:
        EXPECTED: Accordions are ordered by:
        EXPECTED: 1) Class **displayOrder ** in ascending
        EXPECTED: 2) Type **displayOrder ** in ascending
        EXPECTED: 3) Alphabetical (Accordion Title name)
        """
        pass

    def test_002_expand_the_leagues_1_and_2_created_in_pre_conditions(self):
        """
        DESCRIPTION: Expand the Leagues #1 and #2 (created in pre-conditions)
        EXPECTED: Event cards arrangement order is based on sorting rules that account:
        EXPECTED: Sorting by Event ID, accounting : Disporder, Start Time, Name of each event within a type
        EXPECTED: 'Live' event is shown first within a list of events for the expanded League #1
        """
        pass

    def test_003_verify_list_of_events_in_each_of_the_expanded_leagues(self):
        """
        DESCRIPTION: Verify list of events in each of the expanded Leagues
        EXPECTED: **Pre-match events:**
        EXPECTED: Events with next attributes are shown:
        EXPECTED: *   **eventSortCode="TNMT"**/"TRxx" ****(xx - numbers from 01 to 20)
        EXPECTED: *   AND/OR **dispSortName **is positive (e.g. dispSortName="3W")
        EXPECTED: **Started events:**
        EXPECTED: Events with the following attributes are shown:
        EXPECTED: *   **eventSortCode="TNMT"**/"TRxx" ****(xx - numbers from 01 to 20) AND/OR ​**dispSortName **is positive (e.g. dispSortName="3W")
        EXPECTED: *   AND **isMarketBetInRun="true" **(on the any Market level)
        EXPECTED: *   AND **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
        """
        pass

    def test_004_clicktap_on_event_card_of_the_live_event_from_a_league_1(self):
        """
        DESCRIPTION: Click(Tap) on event card of the 'Live' event from a League #1
        EXPECTED: 'Outright' Event details page is opened
        EXPECTED: All Market dropdowns(lanes) are expanded and arrangement order of markets is based rules that account:
        EXPECTED: Sorting by Market ID, accounting : Disporder, Name of each Market within an event
        """
        pass
