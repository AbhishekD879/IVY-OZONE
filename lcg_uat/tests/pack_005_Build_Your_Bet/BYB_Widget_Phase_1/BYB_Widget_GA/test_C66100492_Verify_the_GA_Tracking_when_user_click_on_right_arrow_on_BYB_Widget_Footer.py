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
class Test_C66100492_Verify_the_GA_Tracking_when_user_click_on_right_arrow_on_BYB_Widget_Footer(Common):
    """
    TR_ID: C66100492
    NAME: Verify the GA Tracking when user click on right arrow on BYB Widget Footer
    DESCRIPTION: This test case is to verify the GA Tracking when user click on right arrow on BYB Widget Footer
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

    def test_000_click_on_the_right_arrow_on_byb_widget_footer(self):
        """
        DESCRIPTION: Click on the right arrow on BYB widget footer
        EXPECTED: User can able to click on the right arrow
        """
        pass

    def test_000_verify_ga_tracking(self):
        """
        DESCRIPTION: Verify GA Tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'widgets',
        EXPECTED: component.LabelEvent: 'build your own bet',
        EXPECTED: component.ActionEvent: {right/left},
        EXPECTED: component.PositionEvent: {page of page no)ex: 1 of 3,
        EXPECTED: component.LocationEvent: {home,edp, etc},
        EXPECTED: component.EventDetails: {match name} ,
        EXPECTED: component.URLClicked: {clicked url/ not applicable}
        EXPECTED: }]
        EXPECTED: });
        """
        pass
