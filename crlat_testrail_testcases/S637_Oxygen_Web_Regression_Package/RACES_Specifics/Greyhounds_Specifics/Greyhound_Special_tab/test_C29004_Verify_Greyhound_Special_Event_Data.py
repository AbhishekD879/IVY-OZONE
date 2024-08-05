import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C29004_Verify_Greyhound_Special_Event_Data(Common):
    """
    TR_ID: C29004
    NAME: Verify 'Greyhound Special' Event Data
    DESCRIPTION: This test case verifies 'Greyhound Special' events data
    PRECONDITIONS: To retrieve an information from the Site Server (tst2) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/*X.XX */EventToOutcomeForClass/201?translationLang=LL
    PRECONDITIONS: Where *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Class id = 201 for Greyhound Specials class
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'typeName'** on event level to identify needed event types to be displayed on the application
    PRECONDITIONS: **'classID'** on event level to see class id for selected event type
    PRECONDITIONS: **'className'** on event level to see class name where event belongs to
    PRECONDITIONS: **'name'** on event level to see event name and local time
    PRECONDITIONS: **'isStarted'**=true to see whether event is started
    PRECONDITIONS: **The full request to check data:**
    PRECONDITIONS: Ladbrokes
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/198,201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T14:17:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: Coral
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-26T00:00:00.000Z&simpleFilter=event.startTime:lessThan:2020-08-27T00:00:00.000Z&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T13:35:30.000Z&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load 'Invictus' application
        EXPECTED: 
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: Greyhounds landing page is opened
        EXPECTED: 'Today' tab is opened
        EXPECTED: **'By Meeting'** sorting type is selected by default
        """
        pass

    def test_003_go_to_the_special_event_type_section(self):
        """
        DESCRIPTION: Go to the special event type section
        EXPECTED: Event type section is shown
        """
        pass

    def test_004_verify_class_name_and_class_id_from_the_site_server_response_for_chosen_event_type(self):
        """
        DESCRIPTION: Verify class Name and Class Id from the Site Server response for chosen event type
        EXPECTED: Displayed event type corresponds to the attributes
        EXPECTED: **'classId'**=201 and **'className'**='|Greyhounds - Specials|'
        """
        pass

    def test_005_verify_section_content(self):
        """
        DESCRIPTION: Verify section content
        EXPECTED: Only NOT started events are displayed in the section
        """
        pass

    def test_006_verify_events_within_section(self):
        """
        DESCRIPTION: Verify events within section
        EXPECTED: Only events for current day are displayed (see **'startTime'** attribute on event level)
        """
        pass

    def test_007_verify_started_event_within_sectionevent_with_attributesisstartedtrue_and_rawisoffcode_orrawisoffcodey(self):
        """
        DESCRIPTION: Verify started event within section
        DESCRIPTION: (event with attributes:
        DESCRIPTION: **'isStarted'**=true AND r**awIsOffCode="-"** OR
        DESCRIPTION: **rawIsOffCode="Y"**)
        EXPECTED: Started events disappear from the chosen section
        """
        pass

    def test_008_verify_event_type_section_if_all_events_from_this_event_type_are_started(self):
        """
        DESCRIPTION: Verify event type section if all events from this event type are started
        EXPECTED: Event type section disappear from the front end
        """
        pass

    def test_009_go_to_the_by_time_sorting_type__gt_verify_special_events(self):
        """
        DESCRIPTION: Go to the 'By Time' sorting type -&gt; verify special events
        EXPECTED: Greyhound special events are NOT shown on the 'By Time' sorting type
        """
        pass

    def test_010_go_to_the_tomorrow_tab__gt_verify_special_events(self):
        """
        DESCRIPTION: Go to the 'Tomorrow' tab -&gt; verify special events
        EXPECTED: Greyhound special events are NOT shown on the 'Tomorrow' tab
        EXPECTED: They are not shown neither on 'By Meeting' nor on 'By Time' sorting types
        """
        pass

    def test_011_go_to_the_future_tab__gt_verify_special_events(self):
        """
        DESCRIPTION: Go to the 'Future' tab -&gt; verify special events
        EXPECTED: Greyhound special events are NOT shown on the 'Future' tab
        EXPECTED: They are not shown neither on 'By Meeting' nor on 'By Time' sorting types
        """
        pass
