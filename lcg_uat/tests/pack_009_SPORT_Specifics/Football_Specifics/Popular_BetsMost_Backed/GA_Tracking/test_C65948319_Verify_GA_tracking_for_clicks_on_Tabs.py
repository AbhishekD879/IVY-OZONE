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
class Test_C65948319_Verify_GA_tracking_for_clicks_on_Tabs(Common):
    """
    TR_ID: C65948319
    NAME: Verify GA tracking for clicks on Tabs
    DESCRIPTION: This test case verifies GA tracking for clicks on Tabs
    PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
    PRECONDITIONS: Should have Football events
    """
    keep_browser_open = True

    def test_000_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: User should launch the Application Successfully
        """
        pass

    def test_000_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        pass

    def test_000_click_on_popular_bets_section(self):
        """
        DESCRIPTION: Click on Popular Bets section
        EXPECTED: Able to navigate to the Popular Bets section successfully
        """
        pass

    def test_000_observe_ga_tracking(self):
        """
        DESCRIPTION: Observe GA tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'navigation',
        EXPECTED: component.LabelEvent: 'sub navigation',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: '{from tab name} ex:matches',
        EXPECTED: component.LocationEvent: '{sport name} ex:football,cricket',
        EXPECTED: component.EventDetails: '{to tab name} ex: popular bets',
        EXPECTED: component.URLClicked: '{clicked url} ex:https://sports.coral.co.uk/sport/football/popularbets'
        EXPECTED: }]
        EXPECTED: });
        """
        pass
