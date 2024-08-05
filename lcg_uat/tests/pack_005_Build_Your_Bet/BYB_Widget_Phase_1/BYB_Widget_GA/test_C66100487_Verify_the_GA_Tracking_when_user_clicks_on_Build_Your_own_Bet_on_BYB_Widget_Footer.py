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
class Test_C66100487_Verify_the_GA_Tracking_when_user_clicks_on_Build_Your_own_Bet_on_BYB_Widget_Footer(Common):
    """
    TR_ID: C66100487
    NAME: Verify the GA Tracking when user clicks on Build Your own Bet on BYB Widget Footer
    DESCRIPTION: This test case is to verify the GA Tracking when user clicks on Build Your own Bet on BYB Widget Footer
    PRECONDITIONS: 1. BYB Widget sub section should be created under BYB main section and active for the Football Home page
    PRECONDITIONS: 2. Navigation to go CMS -> BYB -> BYB Widget
    """
    keep_browser_open = True

    def test_000_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the application and login with valid credentials
        EXPECTED: Able to launch the application and login successfully
        """
        pass

    def test_000_navigate_to_the_football_home_page(self):
        """
        DESCRIPTION: Navigate to the Football Home page
        EXPECTED: User can able to navigate to the Football Home page successfully
        """
        pass

    def test_000_verify_the_display_of_byb_widget_on_the_byb_homepage(self):
        """
        DESCRIPTION: Verify the display of BYB Widget on the BYB Homepage
        EXPECTED: User can able to see the BYB Widget
        """
        pass

    def test_000_click_on_build_your_own_bet_on_byb_widget_footer(self):
        """
        DESCRIPTION: Click on Build Your own Bet on BYB Widget Footer
        EXPECTED: Uer can click on the Build Your own Bet on BYB Widget Footer
        """
        pass

    def test_000_verify_event_tracking_in_ga_tracking_console(self):
        """
        DESCRIPTION: Verify Event Tracking in GA Tracking console
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'widgets',
        EXPECTED: component.LabelEvent: 'build your own bet',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: {match name},
        EXPECTED: component.LocationEvent: {home,edp, etc},
        EXPECTED: component.EventDetails: {clicked item} ex:bulid your own bet,
        EXPECTED: component.URLClicked: {clicked url},
        EXPECTED: }]
        EXPECTED: });
        """
        pass

    def test_000_verify_page_view_in_ga_tracking_console(self):
        """
        DESCRIPTION: Verify page view in GA Tracking console
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'pageView',
        EXPECTED: [{
        EXPECTED: page.referrer : {page.referrer} ,ex: https://sports.ladbrokes.com/virtual-sports/football/world-cup
        EXPECTED: page.url : {page.url} ex: https://sports.ladbrokes.com/virtual-sports/womens-football/false-9-fields,
        EXPECTED: page.host : {page.host} , ex:sports.ladbrokes.com
        EXPECTED: page.pathQueryAndFragment : {page.pathQueryAndFragment} ex: en/virtual-sports/womens-football/false-9-fields
        EXPECTED: page.name : {page.name} ex: virtual-sports/womens-football/false-9-fields
        EXPECTED: }]
        EXPECTED: });
        """
        pass
