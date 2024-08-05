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
class Test_C28828_Verify_Future_Tab(Common):
    """
    TR_ID: C28828
    NAME: Verify 'Future' Tab
    DESCRIPTION: This test case verifies 'Future' tab
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

    def test_002_tap_ltracegt_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap &lt;Race&gt; icon from the Sports Menu Ribbon
        EXPECTED: &lt;Race&gt; landing page is opened
        """
        pass

    def test_003_tap_future_tab(self):
        """
        DESCRIPTION: Tap 'Future' tab
        EXPECTED: 1.  'Future' tab is opened
        EXPECTED: 2.  'By Meeting' sorting type is selected by default
        """
        pass

    def test_004_verify_future_tab(self):
        """
        DESCRIPTION: Verify 'Future' tab
        EXPECTED: 1.  Two sorting types are present: 'By Meeting' and 'By Time'
        EXPECTED: 2.  Race Meeting sections are collapsed by default
        """
        pass

    def test_005_check_portrait_and_landscape_modes_for_devices(self):
        """
        DESCRIPTION: Check portrait and landscape modes for devices
        EXPECTED: All page is displayed correctly
        """
        pass
