import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65949625_Verify_Inplay_widget_visibility_in_Football_page(Common):
    """
    TR_ID: C65949625
    NAME: Verify Inplay widget visibility in Football  page
    DESCRIPTION: This Test case verifies the inplay widget
    PRECONDITIONS: 1. Football sport should be
    PRECONDITIONS: configured in CMS
    PRECONDITIONS: 2.DesktopWidgetsToggle should be enabled in the CMS
    PRECONDITIONS: -To enable inPlay and liveStream in CMS -> System configuration  -> Search for DesktopWidgetsToggle under structure -> Check  the field values for inPlay and liveStream -> Save change
    PRECONDITIONS: 3. Live events should be present
    """
    keep_browser_open = True

    def test_001_launch_application(self):
        """
        DESCRIPTION: Launch application
        EXPECTED: Application should be launched successfully
        """
        pass

    def test_002_navigate_to_football_sport(self):
        """
        DESCRIPTION: Navigate to Football sport
        EXPECTED: Matches tab will load by default with inplay widget
        """
        pass

    def test_003_inplay_widget_visibility(self):
        """
        DESCRIPTION: Inplay widget visibility
        EXPECTED: Inplay football widget should load successfully with live icon(inplay  live football)
        """
        pass

    def test_004_verify_inplay_widget_data(self):
        """
        DESCRIPTION: Verify inplay widget data
        EXPECTED: For Desktop:
        EXPECTED: Expandable/collapse chevron should be displayed on Inplay widget
        EXPECTED: -Football  league with event name
        EXPECTED: -teams names should be displayed
        EXPECTED: -Live/watch live labels
        EXPECTED: -Timer (time, HT, FT)
        EXPECTED: -both team Scores should be displayed
        EXPECTED: -market name of that inplay event
        EXPECTED: -Home draw, Away odd button should be displayed
        """
        pass
