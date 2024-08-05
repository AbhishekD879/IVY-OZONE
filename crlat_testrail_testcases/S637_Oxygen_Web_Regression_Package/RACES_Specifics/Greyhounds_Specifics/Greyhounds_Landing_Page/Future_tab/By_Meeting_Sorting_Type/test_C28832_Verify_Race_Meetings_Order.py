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
class Test_C28832_Verify_Race_Meetings_Order(Common):
    """
    TR_ID: C28832
    NAME: Verify 'Race Meetings' Order
    DESCRIPTION: This test case verifies an order of race Meetings when 'By Meeting' filter is selected
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

    def test_002_from_the_sports_menu_ribbon_tap_ltracegt_icon(self):
        """
        DESCRIPTION: From the sports menu ribbon tap &lt;Race&gt; icon
        EXPECTED: &lt;Race&gt; landing page is opened
        """
        pass

    def test_003_tap_future_tab(self):
        """
        DESCRIPTION: Tap 'Future' tab
        EXPECTED: 'Future' tab is opened
        EXPECTED: 'By Meeting' sorting type is selected by default
        """
        pass

    def test_004_check_order_of_race_meetings_when_by_meeting_filter_is_selected(self):
        """
        DESCRIPTION: Check order of race meetings when 'By Meeting' filter is selected
        EXPECTED: Race meetings are ordered in ascending alphabetical order (A-Z)
        """
        pass
