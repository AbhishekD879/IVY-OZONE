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
class Test_C28834_Verify_By_Time_Sorting(Common):
    """
    TR_ID: C28834
    NAME: Verify 'By Time' Sorting
    DESCRIPTION: This test case verifies 'By Time' sorting of events
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
        EXPECTED: - 'By Time' sorting type is opened
        EXPECTED: - 'Events' section is visible
        """
        pass

    def test_005_check_events_section(self):
        """
        DESCRIPTION: Check 'Events' section
        EXPECTED: - Section header is entitled 'Events'
        EXPECTED: - 'Events' section is expanded by default
        EXPECTED: - It is possible to collaps / expand 'Events' section
        """
        pass

    def test_006_verify_by_time_sorting(self):
        """
        DESCRIPTION: Verify 'By Time' sorting
        EXPECTED: Events are sorted in the following order:
        EXPECTED: 1)** **chronologically **by race** **local time** order in the first instance
        EXPECTED: 2) alphabetically by **name** in ascending order if event start times are the same
        """
        pass
