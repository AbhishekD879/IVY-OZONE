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
class Test_C28830_Verify_By_Meeting_Sorting_Type(Common):
    """
    TR_ID: C28830
    NAME: Verify 'By Meeting' Sorting Type
    DESCRIPTION: This test case verifies 'Future' tab when 'By Meeting' sorting type is selected
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

    def test_002_from_the_sports_menu_ribbon_select_race_icon(self):
        """
        DESCRIPTION: From the sports menu ribbon select <Race> icon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_tap_future_tab(self):
        """
        DESCRIPTION: Tap 'Future' tab
        EXPECTED: 1.  'Future' tab is opened
        EXPECTED: 2.  'By Meeting' sorting type is selected by default
        """
        pass

    def test_004_check_by_meeting_section(self):
        """
        DESCRIPTION: Check 'By Meeting' section
        EXPECTED: 1.  List of 'By Meetings' is shown
        EXPECTED: 2.  All sections are collapsed by default
        EXPECTED: 3.  It is possible to collapse / expand these groups by tapping group name or on the arrow
        EXPECTED: 4.  Race meeting names are in be bold
        """
        pass

    def test_005_check_event_section(self):
        """
        DESCRIPTION: Check event section
        EXPECTED: 1.  Each event is in separate block
        EXPECTED: 2.  Event name is shown
        EXPECTED: 3.  Event start date is displayed below the event name
        """
        pass

    def test_006_tap_event_name(self):
        """
        DESCRIPTION: Tap event name
        EXPECTED: User is redirected to the event details page
        """
        pass
