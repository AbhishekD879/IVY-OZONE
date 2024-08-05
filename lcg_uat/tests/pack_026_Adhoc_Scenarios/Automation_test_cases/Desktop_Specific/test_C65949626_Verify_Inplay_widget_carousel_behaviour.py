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
class Test_C65949626_Verify_Inplay_widget_carousel_behaviour(Common):
    """
    TR_ID: C65949626
    NAME: Verify Inplay widget carousel behaviour
    DESCRIPTION: This Test case verifies Inplay widget carousel behaviour
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

    def test_004_verify_scrollability_of_inplay_widget(self):
        """
        DESCRIPTION: Verify scrollability of inplay widget
        EXPECTED: User should be able to scroll Right side , when more than one inplay football event is present
        """
        pass

    def test_005_verify__navigation_of_view_all__inplay_events_link_on_widget(self):
        """
        DESCRIPTION: Verify  navigation of View all  inplay events link on widget
        EXPECTED: User should be navigated to inplay -football SLP page(https://beta-sports.coral.co.uk/in-play/football)
        """
        pass

    def test_006_verify_navigation_of_event_edp_page_from_inplay_widget(self):
        """
        DESCRIPTION: Verify navigation of event EDP page from inplay widget
        EXPECTED: When clicked on inplay widget, user should be navigated to EDP page of football event
        """
        pass

    def test_007_verify_favourite_icon_and_signpostings(self):
        """
        DESCRIPTION: Verify Favourite icon and signpostings
        EXPECTED: Favourite star icon and sign postings Cash out,build your bet, price boost etc should be displayed
        """
        pass
