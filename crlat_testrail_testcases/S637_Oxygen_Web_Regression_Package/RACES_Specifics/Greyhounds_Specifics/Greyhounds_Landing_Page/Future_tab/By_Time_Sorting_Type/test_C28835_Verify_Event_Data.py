import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28835_Verify_Event_Data(Common):
    """
    TR_ID: C28835
    NAME: Verify Event Data
    DESCRIPTION: This test case verifies whether data about events is displayed correctly
    PRECONDITIONS: Request to check data:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/198,201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-14T00:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2020-08-12T10:37:30.000Z&simpleFilter=event.classId:notIntersects:201&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_from_the_sports_menu_ribbon_tap_race_icon(self):
        """
        DESCRIPTION: From the sports menu ribbon tap <Race> icon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_tap_future_tab(self):
        """
        DESCRIPTION: Tap 'Future' tab
        EXPECTED: 'Future' tab is opened
        EXPECTED: 'By Meeting' sorting type is selected by default
        """
        pass

    def test_004_select_by_time_sorting_type(self):
        """
        DESCRIPTION: Select 'By Time' sorting type
        EXPECTED: 'Events' section is visible
        """
        pass

    def test_005_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: Event name corresponds to the **'name' **attribute
        EXPECTED: Tapping event name leads to the event details page
        """
        pass

    def test_006_verify_event_start_date_and_start_time(self):
        """
        DESCRIPTION: Verify Event Start Date and Start Time
        EXPECTED: Event time corresponds to the race local time (see time in the **'name'** attribute)
        """
        pass

    def test_007_verify_event_start_date(self):
        """
        DESCRIPTION: Verify event start date
        EXPECTED: Event start date corresponds to the **'startTime' **attribute
        EXPECTED: Event start time is shown in **'HH:MM EventName' **format
        """
        pass

    def test_008_verify_by_time_sorting_type_when_there_are_no_events_to_show(self):
        """
        DESCRIPTION: Verify 'By Time' sorting type when there are no events to show
        EXPECTED: 1.  'Events' section is not displayed
        EXPECTED: 2.  Message is visible 'No events found'
        """
        pass
