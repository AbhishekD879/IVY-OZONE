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
class Test_C65949630_Football_market_swithcer_display_as_per_cms_conig(Common):
    """
    TR_ID: C65949630
    NAME: Football market swithcer display as per cms conig.
    DESCRIPTION: This test case is to validate the behaviour of market switcher on football SLP..  .
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
    PRECONDITIONS: Click on any one of the tab shown below the tab name and enable the tabs and also make sure to add the market switcher labels.
    PRECONDITIONS: Click on save changes button.
    PRECONDITIONS: Navigate to system configuration>structure>click on search bar and enter market switcher .
    PRECONDITIONS: And make sure to enable active box for football sport.
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

    def test_003_then_navigate_to_other_tabs_present_out_there(self):
        """
        DESCRIPTION: Then navigate to other tabs present out there.
        EXPECTED: Events should be loaded successfully
        """
        pass

    def test_004_validate_the_market_switcher_behaviour_on_all_the_tabs(self):
        """
        DESCRIPTION: validate the market switcher behaviour on all the tabs.
        EXPECTED: Market switcher with dropdown should be displayed.
        """
        pass

    def test_005_click_on_any_market_shown_in_the_market_switcher(self):
        """
        DESCRIPTION: click on any market shown in the market switcher
        EXPECTED: Events with that particular market selected in dropdown should be loaded successfully
        """
        pass

    def test_006_navigate_back_to_the_home_page(self):
        """
        DESCRIPTION: Navigate back to the home page.
        EXPECTED: User should be navigated back to the home page.
        """
        pass

    def test_007_desktop__navigate_to_a_z_menu_and_click_on_footballmobile__navigate_to_footer_menu_and_click_on_a_z_menu_and_click_on__football(self):
        """
        DESCRIPTION: Desktop : Navigate to A-Z menu and click on football.
        DESCRIPTION: Mobile : navigate to footer menu and click on A-Z menu and click on  football.
        EXPECTED: User should be navigated to the  Football landing  page.
        EXPECTED: by default user is in matches tab.
        """
        pass

    def test_008_repeat_3_4_steps(self):
        """
        DESCRIPTION: Repeat 3-4 steps
        EXPECTED: tabs should be loaded successfully. and market switcher should be displayed.
        """
        pass

    def test_009_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application.
        EXPECTED: Application should be loaded successfully.By default user is on home page
        """
        pass

    def test_010_repeat_all_the_above_steps(self):
        """
        DESCRIPTION: Repeat all the above steps.
        EXPECTED: Should work as expected.
        """
        pass
