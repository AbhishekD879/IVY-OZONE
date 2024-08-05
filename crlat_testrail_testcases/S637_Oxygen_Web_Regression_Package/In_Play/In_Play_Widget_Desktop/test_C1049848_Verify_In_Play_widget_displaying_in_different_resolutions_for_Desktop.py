import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C1049848_Verify_In_Play_widget_displaying_in_different_resolutions_for_Desktop(Common):
    """
    TR_ID: C1049848
    NAME: Verify In-Play widget displaying in different resolutions for Desktop
    DESCRIPTION: This test case verifies In-Play widget displaying in different resolutions for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: * For checking data get from In-Play MS use the following instruction:
    PRECONDITIONS: 1. Dev Tools->Network->WS
    PRECONDITIONS: 2. Open "IN_PLAY_SPORTS::XX::LIVE_EVENT::XX" response
    PRECONDITIONS: XX - category ID
    PRECONDITIONS: 3. Look at 'eventCount' attribute for every type available in WS for appropriate category
    PRECONDITIONS: * Use the following link for checking attributes of In-Play events: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL" - means Bet In Play List
    PRECONDITIONS: isStarted="true" - means event is started
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_sports_landing_page_that_contains_live_events_for_width__1280px(self):
        """
        DESCRIPTION: Navigate to Sports Landing page that contains Live events for width > 1280px
        EXPECTED: * Sports Landing page is loaded
        EXPECTED: * In-Play widget is displayed in 3-rd column
        EXPECTED: * In-Play widget is expanded by default
        """
        pass

    def test_003_verify_in_play_widget_content(self):
        """
        DESCRIPTION: Verify In-Play widget content
        EXPECTED: In Play widget is displayed with following elements:
        EXPECTED: * 'In Play' header
        EXPECTED: * Carousel with event cards and navigation arrows
        EXPECTED: * 'In-Play' footer
        """
        pass

    def test_004_navigate_to_sports_event_details_page_and_verify_in_play_widget_displaying(self):
        """
        DESCRIPTION: Navigate to Sports Event Details page and verify In-Play widget displaying
        EXPECTED: * Sports Event Details page is loaded
        EXPECTED: * In-Play widget is NOT displayed
        """
        pass

    def test_005_back_to_sports_landing_page_and_verify_in_play_widget_displaying_from_width_1025px_to_1279px(self):
        """
        DESCRIPTION: Back to Sports Landing page and verify In-Play widget displaying from width 1025px to 1279px
        EXPECTED: * Sports Landing page is loaded
        EXPECTED: * In-Play widget is displayed below main content as the separate section
        """
        pass

    def test_006_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step 3
        EXPECTED: In Play widget is displayed with following elements:
        EXPECTED: * 'In Play' header
        EXPECTED: * Carousel with event cards and navigation arrows
        EXPECTED: * 'In-Play' footer
        """
        pass

    def test_007_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step 4
        EXPECTED: * Sports Event Details page is loaded
        EXPECTED: * In-Play widget is NOT displayed
        """
        pass
