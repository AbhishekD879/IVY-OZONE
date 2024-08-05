import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893187_Verify_if_the_user_upgrades_from_Digital_to_MC_user_User_should_come_back_to_the_Grid_Home_Page_and_activate_card_button_is_not_shown(Common):
    """
    TR_ID: C64893187
    NAME: Verify if the user upgrades from Digital to MC user, User should come back to the Grid Home Page and  "activate card " button is not shown.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports web app URL.
    PRECONDITIONS: 2.User should have valid Digital user credentials.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_app2click_on_grid_tab_from_sports_main_header3click_on_login_button_and_move_to_the_grid_tab_and_enter_valid_inshop_user_credentials_and_click_on_login4activate_card_must_be_seen_on_the_home_page5click_on_activate_card_button6generate_grid_card_pop_up_is_shown7enter_pin_and_click_on_generate_card8verify_if_the_user_is_able_to_come_back_to_the_grid_homepage_after_upgrade_and_is_not_able_to_see_activate_card_buttonexpected_result1sports_application_should_be_launch_successfully2user_should_be_able_to_open_grid_tab_from_sports_main_header3user_should_be_navigated_to_login_page_and_clicking_on_the_grid_digital_login_page_is_opened_enter_the_credentials_and_user_is_logged_in4user_must_be_able_to_see_activate_card_button_on_the_grid_home_page5user_must_be_able_see_the_upgrade_journey_on_clicking_activate_card_button6user_must_be_able_to_see_the_generate_grid_card_pop_up7user_is_navigated_to_complete_your_grid_card_sign_up_and_enter_the_4_digit_pin_and_click_on_submit8user_should_be_able_to_see_grid_card_details_and_clicking_on_continue_or_close_should_take_the_user_to_grid_home_page(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web app.
        DESCRIPTION: 2.Click on grid tab from sports main header.
        DESCRIPTION: 3.Click on login button and move to "The Grid" tab and enter valid inshop user credentials and click on login.
        DESCRIPTION: 4."activate card" must be seen on the home page.
        DESCRIPTION: 5.Click on "activate card" button.
        DESCRIPTION: 6."GENERATE GRID CARD" pop-up is shown.
        DESCRIPTION: 7.enter pin and click on generate card
        DESCRIPTION: 8.verify if the user is able to come back to the grid homepage after upgrade and is not able to see activate card button
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab from sports main header.
        DESCRIPTION: 3.User should be navigated to login page and clicking on "The grid" digital login page is opened, enter the credentials and user is logged in.
        DESCRIPTION: 4.User must be able to see "activate card" button on the Grid Home Page.
        DESCRIPTION: 5.User must be able see the upgrade journey on clicking "activate card" button.
        DESCRIPTION: 6.User must be able to see the "GENERATE GRID CARD" pop-up.
        DESCRIPTION: 7.User is navigated to complete your Grid card sign up and enter the 4 digit pin and click on "Submit".
        DESCRIPTION: 8.User should be able to see grid card details and clicking on continue or close should take the user to grid home page
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab from sports main header.
        EXPECTED: 3.User should be navigated to login page and clicking on "The grid" digital login page is opened, enter the credentials and user is logged in.
        EXPECTED: 4.User must be able to see "activate card" button on the Grid Home Page.
        EXPECTED: 5.User must be able see the upgrade journey on clicking "activate card" button.
        EXPECTED: 6.User must be able to see the "GENERATE GRID CARD" pop-up.
        EXPECTED: 7.User is navigated to complete your Grid card sign up and enter the 4 digit pin and click on "Submit".
        EXPECTED: 8.User should be able to see grid card details and clicking on continue or close should take the user to grid home page
        """
        self.site.wait_content_state('Homepage')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.assertTrue(self.site.grid.upgrade_account.is_displayed(),
                        msg=f'"{vec.retail.ACTIVATE_CARD_BUTTON}" button is not displayed')
        actual_text = self.site.grid.upgrade_account.text
        self.assertEqual(actual_text, vec.retail.ACTIVATE_CARD_BUTTON,
                         msg=f'Actual text: "{actual_text}" is not same as Expected text: "{vec.retail.ACTIVATE_CARD_BUTTON}"')
        self.site.grid.upgrade_account.click()
        sleep(2)
        generate_grid_card_title = self.site.generate_grid_card.generate_grid_card_title
        self.assertEqual(generate_grid_card_title, vec.retail.GENERATE_GRID_CARD,
                         msg=f'Actual text: "{generate_grid_card_title}" is not same as Expected text: "{vec.retail.GENERATE_GRID_CARD}"')
        self.site.generate_grid_card.generate_button.click()
        self.site.generate_grid_card.setpincode.enter_pin.value = tests.settings.in_shop_pin
        self.site.generate_grid_card.setpincode.confirm_pin.value = tests.settings.in_shop_pin
        self.site.generate_grid_card.setpincode.submit_button.click()
        sleep(4)
        mygrid_card = self.site.generate_grid_card.my_grid_card.header
        self.assertEqual(mygrid_card, vec.retail.MY_GRID_CARD,
                         msg=f'Actual text: "{mygrid_card}" is not same as Expected text: "{vec.retail.MY_GRID_CARD}"')
        self.assertTrue(self.site.generate_grid_card.my_grid_card.has_grid_virtual_card,
                        msg='Virtaul Grid card is not displayed')
        finish_button = self.site.generate_grid_card.my_grid_card.finish_button
        self.site.contents.scroll_to_we(finish_button)
        finish_button.click()
        self.site.wait_content_state(state_name='thegrid')
