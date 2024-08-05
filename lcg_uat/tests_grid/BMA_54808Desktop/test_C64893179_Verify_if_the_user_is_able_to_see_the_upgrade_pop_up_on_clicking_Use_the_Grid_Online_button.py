import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893179_Verify_if_the_user_is_able_to_see_the_upgrade_pop_up_on_clicking_Use_the_Grid_Online_button(Common):
    """
    TR_ID: C64893179
    NAME: Verify if the user is able to see the upgrade pop-up on clicking "Use the Grid Online" button
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports web app URL.
    PRECONDITIONS: 2.User should have valid inshop user credentials.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_app2click_on_grid_tab_from_sports_main_header3click_on_login_button_and_move_to_the_grid_tab_and_enter_valid_inshop_user_credentials_and_click_on_login4use_the_grid_online_must_be_seen_on_the_home_page5click_on_use_the_grid_online_button6verify_upgrade_pop_up_is_shown_with_two_options1upgrade2no_thanksexpected_result1sports_application_should_be_launch_successfully2user_should_be_able_to_open_grid_tab_from_sports_main_header3user_should_be_navigated_to_login_page_and_clicking_on_the_grid_inshop_login_page_is_opened_enter_the_credentials_and_user_is_logged_in4user_must_be_able_to_see_use_the_grid_online_button_on_the_grid_home_page5user_must_be_able_to_start_the_upgrade_journey_on_clicking_use_the_grid_online_button6user_must_be_able_to_see_the_upgrade_pop_up_with_no_thanks_and_upgrade_buttons(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web app.
        DESCRIPTION: 2.Click on grid tab from sports main header.
        DESCRIPTION: 3.Click on login button and move to "The Grid" tab and enter valid inshop user credentials and click on login.
        DESCRIPTION: 4."Use the Grid Online" must be seen on the home page.
        DESCRIPTION: 5.Click on "Use the Grid Online" button.
        DESCRIPTION: 6.Verify Upgrade pop-up is shown with two options
        DESCRIPTION: 1.upgrade
        DESCRIPTION: 2.No thanks
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab from sports main header.
        DESCRIPTION: 3.User should be navigated to login page and clicking on "The grid" inshop login page is opened, enter the credentials and user is logged in.
        DESCRIPTION: 4.User must be able to see "Use the Grid Online" button on the Grid Home Page.
        DESCRIPTION: 5.User must be able to start the upgrade journey on clicking "Use the Grid Online" button.
        DESCRIPTION: 6.User must be able to see the "Upgrade pop-up" with "No, THANKS" and "UPGRADE" buttons.
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab from sports main header.
        EXPECTED: 3.User should be navigated to login page and clicking on "The grid" inshop login page is opened, enter the credentials and user is logged in.
        EXPECTED: 4.User must be able to see "Use the Grid Online" button on the Grid Home Page.
        EXPECTED: 5.User must be able to start the upgrade journey on clicking "Use the Grid Online" button.
        EXPECTED: 6.User must be able to see the "Upgrade pop-up" with "No, THANKS" and "UPGRADE" buttons.
        """
        self.site.wait_content_state('Homepage')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid', timeout=30)
        self.site.grid_connect_login()
        if self.site.upgrade_your_account.is_displayed(timeout=60):
            self.site.upgrade_your_account.no_thanks_button.click()
        self.site.wait_splash_to_hide(timeout=30)
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        self.device.driver.implicitly_wait(5)
        self.site.grid.scroll_to_top()
        self.assertTrue(self.site.grid.upgrade_account.is_displayed(),
                        msg=f'"{vec.retail.USE_THE_GRID_ONLINE_BUTTON}" button is not displayed')
        actual_text = self.site.grid.upgrade_account.text
        self.assertEqual(actual_text, vec.retail.USE_THE_GRID_ONLINE_BUTTON,
                         msg=f'Actual text: "{actual_text}" is not same as Expected text: "{vec.retail.USE_THE_GRID_ONLINE_BUTTON}"')
        self.site.grid.upgrade_account.click()
        no_thanks = self.site.upgrade_your_account.no_thanks_button.name
        self.assertEqual(no_thanks, vec.retail.NO_THANKS_BUTTON.upper(),
                         msg=f'Actual text: "{no_thanks}" is not same as Expected text: "{vec.retail.NO_THANKS_BUTTON.upper()}"')
        upgrade = self.site.upgrade_your_account.upgrade_button.name
        self.assertEqual(upgrade, vec.retail.UPGRADE.upper(),
                         msg=f'Actual text: "{upgrade}" is not same as Expected text: "{vec.retail.UPGRADE.upper()}"')
