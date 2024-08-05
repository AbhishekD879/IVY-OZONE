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
class Test_C65949631_Verify_displaying_of_time_and_league_filters_on_football_SLP(Common):
    """
    TR_ID: C65949631
    NAME: Verify displaying of time and league filters on football SLP
    DESCRIPTION: This test case is to validate the displaying of time and league filters.
    PRECONDITIONS: User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: Football entry points
    PRECONDITIONS: Navigate to     menus>subheadermenus>Football.
    PRECONDITIONS: Click on Football.
    PRECONDITIONS: Make the active check box and in app check box as active.
    PRECONDITIONS: Click on save changes button.
    PRECONDITIONS: Navigate to sport pages>sport categories>football>Genral sport configuration.
    PRECONDITIONS: Enable all the check boxes present out there.
    PRECONDITIONS: Enter all the mandatory fields.
    PRECONDITIONS: Note : Add primary markets there.
    PRECONDITIONS: Scroll down amd make sure to enable all the tabs(matches,,inplay,Specials,Outrights) .
    PRECONDITIONS: Click on each tab and make sure to add time and league filters.
    PRECONDITIONS: click on save changes button.
    """
    keep_browser_open = True

    def test_001_lauch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Lauch the Ladbrokes/Coral application.
        EXPECTED: Application should be loaded successfully.By default user is on home page
        """
        pass

    def test_002_desktop_navigate_to_sub_header_menu_and_click_on_footballmobile__navigate_to_sports_ribbon_and_click_on_click_on_football(self):
        """
        DESCRIPTION: Desktop: navigate to sub header menu and click on football.
        DESCRIPTION: Mobile : navigate to sports ribbon and click on click on football.
        EXPECTED: User should be navigated to the  Football landing  page.
        EXPECTED: by default user is in matches tab.
        """
        pass

    def test_003_validate_the_time_and_league_filters(self):
        """
        DESCRIPTION: validate the time and league filters.
        EXPECTED: Time and league filters should be displayed as per cms.
        """
        pass

    def test_004_navigate_to_other_tabs_present_out_there(self):
        """
        DESCRIPTION: Navigate to other tabs present out there.
        EXPECTED: Time and league filters should be displayed as per cms.
        """
        pass

    def test_005_click_on_time_and_league_filters(self):
        """
        DESCRIPTION: Click on time and league filters.
        EXPECTED: The events with the selected filters should be loaded successfully.
        """
        pass

    def test_006_refresh_the_application(self):
        """
        DESCRIPTION: Refresh the application.
        EXPECTED: The user should be displayed with the same results without any changes.
        """
        pass

    def test_007_navigate_back_to_the_home_page(self):
        """
        DESCRIPTION: Navigate back to the home page.
        EXPECTED: User should be navigated back to the home page.
        """
        pass

    def test_008_desktop__navigate_to_a_z_menu_and_click_on_footballmobile__navigate_to_footer_menu_and_click_on_a_z_menu_and_click_on__football(self):
        """
        DESCRIPTION: Desktop : Navigate to A-Z menu and click on football.
        DESCRIPTION: Mobile : navigate to footer menu and click on A-Z menu and click on  football.
        EXPECTED: User should be navigated to the  Football landing  page.
        EXPECTED: by default user is in matches tab.
        """
        pass

    def test_009_repeat_3_4_steps(self):
        """
        DESCRIPTION: Repeat 3-4 steps
        EXPECTED: tabs should be loaded successfully  with time and league filters
        """
        pass

    def test_010_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application.
        EXPECTED: Application should be loaded successfully.By default user is on home page
        """
        pass

    def test_011_repeat_all_the_above_steps(self):
        """
        DESCRIPTION: Repeat all the above steps.
        EXPECTED: Should work as expected.
        """
        pass
