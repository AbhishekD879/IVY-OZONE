import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C66007983_Verify_the_functionality_of_the_Market_Switcher_display_as_per_the_CMS_configuration_on_the_Snooker_sport_landing_page(Common):
    """
    TR_ID: C66007983
    NAME: Verify the functionality of the Market Switcher display as  per the  CMS configuration on the Snooker sport landing page.
    DESCRIPTION: This test case is to validate the
    DESCRIPTION: behaviour of Market Switcher on the Snooker sport landing page.
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: Snooker entry points
    PRECONDITIONS: 2.Navigate to Sport pages-&gt; Sport categories-&gt; Snooker -&gt; General sport configuration.
    PRECONDITIONS: 3.Enable all the check boxes present out there.
    PRECONDITIONS: 4.Enter all the mandatory fields.
    PRECONDITIONS: Note : Add primary markets there.
    PRECONDITIONS: 5.Scroll down and make sure to enable all the tabs(Matches,,Inplay, Specials, Outright's)
    PRECONDITIONS: 6.Click on any one of the tab shown below the tab name and enable the tabs and also make sure to add the market switcher labels.
    PRECONDITIONS: 7.Click on save changes button.
    PRECONDITIONS: 8.Navigate to system configuration&gt;structure&gt;click on search bar and enter market switcher .
    PRECONDITIONS: And make sure to enable active box for Snooker sport.
    """
    keep_browser_open = True

    def test_000_launch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes/Coral application.
        EXPECTED: Application should be loaded successfully. By default user is on home page
        """
        pass

    def test_000_desktop_navigate_to_sub_header_menu_and_click_on_snooker(self):
        """
        DESCRIPTION: Desktop: Navigate to sub header menu and click on Snooker.
        EXPECTED: User should be navigated to the  Snooker landing  page.
        """
        pass

    def test_000_mobile__navigate_to_sports_ribbon_and_click_on_click_on_snooker(self):
        """
        DESCRIPTION: Mobile : Navigate to sports ribbon and click on click on Snooker.
        EXPECTED: By default user is in Matches tab.
        """
        pass

    def test_000_then_navigate_to_other_tabs_present_out_there(self):
        """
        DESCRIPTION: Then navigate to other tabs present out there.
        EXPECTED: Events should be loaded successfully
        """
        pass

    def test_000_validate_the_market_switcher_behaviour_on_all_the_tabs(self):
        """
        DESCRIPTION: Validate the Market Switcher behaviour on all the tabs.
        EXPECTED: Market switcher with dropdown should be displayed.
        """
        pass

    def test_000_click_on_any_market_shown_in_the_market_switcher(self):
        """
        DESCRIPTION: Click on any market shown in the Market Switcher
        EXPECTED: Events with that particular market selected in dropdown should be loaded successfully
        """
        pass

    def test_000_navigate_back_to_the_home_page(self):
        """
        DESCRIPTION: Navigate back to the home page.
        EXPECTED: User should be navigated back to the home page.
        """
        pass

    def test_000_desktop__navigate_to_a_z_menu_and_click_on_snooker(self):
        """
        DESCRIPTION: Desktop : Navigate to A-Z menu and click on Snooker.
        EXPECTED: User should be navigated to the  Snooker landing  page.
        """
        pass

    def test_000_mobile__navigate_to_footer_menu_and_click_on_a_z_menu_and_click_on__snooker(self):
        """
        DESCRIPTION: Mobile : Navigate to footer menu and click on A-Z menu and click on  Snooker.
        EXPECTED: By default user should be in Matches tab.
        """
        pass

    def test_000_repeat_3_4_steps(self):
        """
        DESCRIPTION: Repeat 3-4 steps
        EXPECTED: Tabs should be loaded successfully. and market switcher should be displayed.
        """
        pass

    def test_000_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application.
        EXPECTED: Application should be loaded successfully. By default user is on home page
        """
        pass

    def test_000_repeat_all_the_above_steps(self):
        """
        DESCRIPTION: Repeat all the above steps.
        EXPECTED: It should work as expected.
        """
        pass
