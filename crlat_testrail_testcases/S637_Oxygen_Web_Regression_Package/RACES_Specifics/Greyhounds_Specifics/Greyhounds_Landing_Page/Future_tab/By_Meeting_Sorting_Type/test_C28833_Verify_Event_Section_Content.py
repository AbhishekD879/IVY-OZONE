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
class Test_C28833_Verify_Event_Section_Content(Common):
    """
    TR_ID: C28833
    NAME: Verify Event Section Content
    DESCRIPTION: This test case verifies event section content
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
        EXPECTED: 'Future' tab is selected
        """
        pass

    def test_004_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
        EXPECTED: Event name corresponds to the** 'name' **attribute from the Site Server (including race local time)
        """
        pass

    def test_005_verify_event_time(self):
        """
        DESCRIPTION: Verify event time
        EXPECTED: Event time is shown before the event name
        EXPECTED: Event time corresponds to the race local time (see **'name'** attribute)
        """
        pass

    def test_006_verify_event_date(self):
        """
        DESCRIPTION: Verify event date
        EXPECTED: Event date corresponds to the Site Server response ( see **'startTime' **attribute)
        """
        pass

    def test_007_verify_date_format(self):
        """
        DESCRIPTION: Verify date format
        EXPECTED: Date formats isthe following:
        EXPECTED: **DD-MM-YYYY**
        """
        pass
