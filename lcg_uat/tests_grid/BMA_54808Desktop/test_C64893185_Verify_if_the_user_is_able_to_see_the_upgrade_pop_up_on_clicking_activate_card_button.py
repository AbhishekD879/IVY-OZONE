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
class Test_C64893185_Verify_if_the_user_is_able_to_see_the_upgrade_pop_up_on_clicking_activate_card_button(Common):
    """
    TR_ID: C64893185
    NAME: Verify if the user is able to see the upgrade pop-up on clicking "activate card" button
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports web app URL.
    PRECONDITIONS: 2.User should have valid Digital user credentials.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_app2click_on_grid_tab_from_sports_main_header3click_on_login_button_and_move_to_the_grid_tab_and_enter_valid_digital_user_credentials_and_click_on_login4activate_card_must_be_seen_on_the_home_page5click_on_activate_card_button6generate_grid_card_pop_up_is_shownexpected_result1sports_application_should_be_launch_successfully2user_should_be_able_to_open_grid_tab_from_sports_main_header3user_should_be_navigated_to_login_page_and_clicking_on_the_grid_inshop_login_page_is_opened_enter_the_credentials_and_user_is_logged_in4user_must_be_able_to_see_activate_card_button_on_the_grid_home_page5user_must_be_able_to_start_the_upgrade_journey_on_clicking_activate_card_button6user_must_be_able_to_see_the_generate_grid_card_pop_up_with_no_thanks_and_generate(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web app.
        DESCRIPTION: 2.Click on grid tab from sports main header.
        DESCRIPTION: 3.Click on login button and move to "The Grid" tab and enter valid Digital user credentials and click on login.
        DESCRIPTION: 4."activate card" must be seen on the home page.
        DESCRIPTION: 5.Click on "activate card" button.
        DESCRIPTION: 6."GENERATE GRID CARD" pop-up is shown.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab from sports main header.
        DESCRIPTION: 3.User should be navigated to login page and clicking on "The grid" inshop login page is opened, enter the credentials and user is logged in.
        DESCRIPTION: 4.User must be able to see "activate card" button on the Grid Home Page.
        DESCRIPTION: 5.User must be able to start the upgrade journey on clicking "activate card" button.
        DESCRIPTION: 6.User must be able to see the "GENERATE GRID CARD" pop-up with "NO THANKS" and "GENERATE".
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab from sports main header.
        EXPECTED: 3.User should be navigated to login page and clicking on "The grid" inshop login page is opened, enter the credentials and user is logged in.
        EXPECTED: 4.User must be able to see "activate card" button on the Grid Home Page.
        EXPECTED: 5.User must be able to start the upgrade journey on clicking "activate card" button.
        EXPECTED: 6.User must be able to see the "GENERATE GRID CARD" pop-up with "NO THANKS" and "GENERATE".
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
        self.site.grid.upgrade_account.click()
        generate_grid_card_title = self.site.generate_grid_card.generate_grid_card_title
        self.assertEqual(generate_grid_card_title, vec.retail.GENERATE_GRID_CARD,
                         msg=f'Actual text: "{generate_grid_card_title}" is not same as Expected text: "{vec.retail.GENERATE_GRID_CARD}"')

        No_thanks_button = self.site.generate_grid_card.no_thanks_button.text
        self.assertEqual(No_thanks_button, vec.retail.NO_THANKS_BUTTON.upper(),
                         msg=f'Actual text: "{No_thanks_button}" is not same as Expected text: "{vec.retail.NO_THANKS_BUTTON.upper()}"')
        Generate_button = self.site.generate_grid_card.generate_button.text
        self.assertEqual(Generate_button, vec.retail.GENERATE_BUTTON,
                         msg=f'Actual text: "{Generate_button}" is not same as Expected text: "{vec.retail.GENERATE_BUTTON}"')
