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
class Test_C65948322_Verify_GA_tracking_for_clicks_on_filters(Common):
    """
    TR_ID: C65948322
    NAME: Verify GA tracking for clicks on filters
    DESCRIPTION: This test case verifies GA tracking for clicks on filters
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

    def test_000_click_on_filters_observe_ga_tracking(self):
        """
        DESCRIPTION: Click on filters ,Observe GA tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betting',
        EXPECTED: component.LabelEvent: 'popular bets',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'not applicable',
        EXPECTED: component.LocationEvent: 'popular bets',
        EXPECTED: component.EventDetails: '{clicked filter} ex:30mins, 1hr etc',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        pass
