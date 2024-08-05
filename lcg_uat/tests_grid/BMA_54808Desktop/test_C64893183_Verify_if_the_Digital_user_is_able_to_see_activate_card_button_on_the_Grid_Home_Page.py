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
class Test_C64893183_Verify_if_the_Digital_user_is_able_to_see_activate_card_button_on_the_Grid_Home_Page(Common):
    """
    TR_ID: C64893183
    NAME: Verify if the Digital user is able to see "activate card" button on the Grid Home Page.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports web app URL.
    PRECONDITIONS: 2.User should have valid Digital user credentials.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_app2click_on_grid_tab_from_sports_main_header3click_on_login_button_and_move_to_the_grid_tab_and_enter_valid_digital_user_credentials_and_click_on_login4activate_card_must_be_seen_on_the_home_pageexpected_result1sports_application_should_be_launch_successfully2user_should_be_able_to_open_grid_tab_from_sports_main_header3user_should_be_navigated_to_login_page_and_clicking_on_the_grid_digital_login_page_is_opened_and_enter_the_credentials_and_user_is_logged_in4user_must_be_able_to_see_activate_card_button_on_the_grid_home_page(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web app.
        DESCRIPTION: 2.Click on grid tab from sports main header.
        DESCRIPTION: 3.Click on login button and move to "The Grid" tab and enter valid Digital user credentials and click on login.
        DESCRIPTION: 4."activate card" must be seen on the home page.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab from sports main header.
        DESCRIPTION: 3.User should be navigated to login page and clicking on "The grid" digital login page is opened and enter the credentials and user is logged in.
        DESCRIPTION: 4.User must be able to see "activate card" button on the Grid Home Page.
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab from sports main header.
        EXPECTED: 3.User should be navigated to login page and clicking on "The grid" digital login page is opened and enter the credentials and user is logged in.
        EXPECTED: 4.User must be able to see "activate card" button on the Grid Home Page.
        """
        self.site.wait_content_state('Homepage')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        self.site.login()
        self.assertTrue(self.site.grid.upgrade_account.is_displayed(),
                        msg=f'"{vec.retail.ACTIVATE_CARD_BUTTON}" button is not displayed')
        actual_text = self.site.grid.upgrade_account.text
        self.assertEqual(actual_text, vec.retail.ACTIVATE_CARD_BUTTON,
                         msg=f'Actual text: "{actual_text}" is not same as Expected text: "{vec.retail.ACTIVATE_CARD_BUTTON}"')
