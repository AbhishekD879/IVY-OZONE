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
class Test_C28831_Verify_Race_Meetings_data_filtering(Common):
    """
    TR_ID: C28831
    NAME: Verify 'Race Meetings' data filtering
    DESCRIPTION: This test case verifies whether data about race meetings is stored properly from Site server
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

    def test_004_verify_list_of_race_meetings(self):
        """
        DESCRIPTION: Verify list of 'Race Meetings'
        EXPECTED: Race meeting name corresponds to the '**typeName'** parameter from Site Server
        """
        pass

    def test_005_check_event_start_time_in_the_list_of_events(self):
        """
        DESCRIPTION: Check Event Start Time in the list of events
        EXPECTED: Events are shown ONLY for the day after tomorrow and further (see **'startTime'** attribute)
        """
        pass
