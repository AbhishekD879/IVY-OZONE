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
class Test_C28829_Verify_data_for_Future_tab(Common):
    """
    TR_ID: C28829
    NAME: Verify data for 'Future' tab
    DESCRIPTION: This test case verifies data which is displayed in 'Future' tab
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

    def test_002_on_the_homepage_tap_ltracegt_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: On the homepage tap &lt;Race&gt; icon from the sports menu ribbon
        EXPECTED: 1.  &lt;Race&gt; landing page is opened
        EXPECTED: 2.  'Today' tab is displayed
        """
        pass

    def test_003_tap_future_tab(self):
        """
        DESCRIPTION: Tap 'Future' tab
        EXPECTED: 'Future' tab is opened
        EXPECTED: 'By Meeting' sorting type is selected by default
        """
        pass

    def test_004_chack_data_which_is_displayed_in_future_tab(self):
        """
        DESCRIPTION: Chack data which is displayed in 'Future' tab
        EXPECTED: 1.  A list of all future's racing is displayed
        EXPECTED: 2.  Data corresponds to the Site Server response
        EXPECTED: 3.  Event start times correspond to day after tomorrow's date and further (see **'startTime'** attribute)
        """
        pass
