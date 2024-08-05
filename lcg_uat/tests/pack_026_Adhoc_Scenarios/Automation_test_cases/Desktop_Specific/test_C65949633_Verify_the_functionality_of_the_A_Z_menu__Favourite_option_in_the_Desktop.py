import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments.constants.base.football import Football
from voltron.utils.waiters import wait_for_haul


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.cms
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.nark.desktop_specific
@vtest
class Test_C65949633_Verify_the_functionality_of_the_A_Z_menu__Favourite_option_in_the_Desktop(Common):
    """
    TR_ID: C65949633
    NAME: Verify the functionality of the
    A-Z menu - Favourite option in the Desktop.
    DESCRIPTION: This test case is to validate the functionality of the
    DESCRIPTION: A-Z menu - Favourite option in the Desktop.
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    username = tests.settings.betplacement_user
    selected_sports_list = []
    sport_name = Football.FOOTBALL_TITLE
    expected_favourite_checkbox_color = 'rgb(255, 205, 0)'  # Yellow color rgb code


    def get_color_of_before_pseudo_element(self, web_element):
        """
           Get the color of the ::before pseudo-element of a web element using JavaScript.

           Args:
               web_element (WebElement): The web element for which you want to retrieve the color of the ::before pseudo-element.

           Returns:
               str: The color of the ::before pseudo-element in CSS format (e.g., "rgb(255, 0, 0)" or "#FF0000").

           Explanation:
           This method uses JavaScript to access the color of the ::before pseudo-element of a web element. The ::before pseudo-element is a
           CSS concept used to add content before an element. To access its properties, JavaScript is used because Selenium itself
           doesn't provide direct access to pseudo-elements.

           The JavaScript code within the method does the following:
           - It uses the `window.getComputedStyle` function, which retrieves the computed style of an element.
           - `arguments[0]` refers to the `web_element` parameter passed to the script.
           - `"::before"` is used as the pseudo-element selector.
           - `getPropertyValue("color")` is used to extract the color property of the ::before pseudo-element.

           The color is returned as a string in CSS format, such as "rgb(255, 0, 0)"

           """
        return self.device.driver.execute_script(
                    'return window.getComputedStyle(arguments[0], "::before").getPropertyValue("color");', web_element
                )

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. User should have access to oxygen CMS
        PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
        PRECONDITIONS: 2. Login with valid credentials
        PRECONDITIONS: 3.Navigate to  System Configuration and click on the Structure option.
        PRECONDITIONS: 4.Under the 'FavouriteCount' group check the property 'maxFavourites'.
        PRECONDITIONS: 5.Field value should be a number greater than zero.(If value is 0 increment it and click on save option)
        PRECONDITIONS: Note: The number against the 'maxFavourites' property is the maximum number of sports the user can select and add as favourites from the A-Z menu.
        """
        self.__class__.max_favourites = int(self.get_initial_data_system_configuration().
                                            get('FavouriteCount').get('maxFavourites')
                                            )
        if self.max_favourites <= 0:
            self.__class__.max_favourites = int(self.cms_config.update_system_configuration_structure(
                config_item='FavouriteCount', field_name='maxFavourites', field_value=3).
                                                get('structure').get('FavouriteCount').get('maxFavourites')
                                                )

    def test_001_launch_the__ladbrokescoral_application(self):
        """
        DESCRIPTION: launch the  Ladbrokes/Coral application.
        EXPECTED: Application should be  Launched successfully.
        """
        self.navigate_to_page(name=tests.HOSTNAME)
        self.site.wait_content_state(state_name='HomePage')

    def test_002_on_to_the_left_hand_side_of_the_application_a_z_menu_can_be_seen_hover_the_mouse_pointer_across_the_sports_that_are_available(
            self):
        """
        DESCRIPTION: On to the left hand side of the application A-Z menu can be seen, hover the mouse pointer across the sports that are available.
        EXPECTED: On hovering the mouse pointer star option should
        EXPECTED: not be seen against any of the sport.
        """
        # A - Z Sports
        a_to_z_sports_menu_items = self.site.sport_menu.sport_menu_items_group('AZ').items_as_ordered_dict
        for sport in a_to_z_sports_menu_items:
            # hover the mouse pointer over the sport
            a_to_z_sports_menu_items[sport].mouse_over()
            # check if the sport does not have favourite checkbox before login
            self.assertFalse(a_to_z_sports_menu_items[sport].has_favourite_checkbox(expected_result=False),
                             msg=f'{sport} has favourite checkbox even after mouse over and before login')

    def test_003_login_to_the_application_with_valid_credentials_from_the_log_in_buttonenter_valid_user_credentials_and_click_on_login_in_button(
            self):
        """
        DESCRIPTION: Login to the application with valid credentials from the 'Log In' button.Enter valid user credentials and click on 'Login In' button.
        EXPECTED: User should be successfully logged in.
        """
        self.site.login(username=self.username)

        # Making sure after the login, that the user does not have any favourite sport
        if self.site.sport_menu.has_favourite_sport_menu_items_group():
            already_favourite_sport_frontend = self.site.sport_menu.favourite_sport_menu_items_group.items_as_ordered_dict.values()
            # if there are any favourites sport then remove them all
            for favourite_sport_object in already_favourite_sport_frontend:
                favourite_sport_object.scroll_to_we()
                favourite_sport_object.favourite_checkbox.click()

    def test_004_on_to_the_left_hand_side_of_the_application_a_z_menu_can_be_seen_hover_the_mouse_pointer_across_the_various_sports_that_are_available_in_the_list(
            self):
        """
        DESCRIPTION: On to the left hand side of the application A-Z menu can be seen, hover the mouse pointer across the various sports that are available in the list.
        EXPECTED: On hovering the mouse pointer star option should be seen against all the sports available under A-Z menu.
        """
        # A - Z Sports
        a_to_z_sports_menu_items = self.site.sport_menu.sport_menu_items_group('AZ').items_as_ordered_dict
        for sport in a_to_z_sports_menu_items:
            # hover the mouse pointer over the sport
            a_to_z_sports_menu_items[sport].mouse_over()
            # check if the sport hase favourite checkbox after login
            self.assertTrue(a_to_z_sports_menu_items[sport].has_favourite_checkbox(expected_result=True), msg=f'{sport} does not have favourite checkbox after mouse over')

    def test_005_select_the_star_option_against_a_particular_sportavailable_under_a_z_menufootball_is_selected(self):
        """
        DESCRIPTION: Select the star option against a particular sport
        DESCRIPTION: available under A-Z menu.(Football is selected)
        EXPECTED: 1.The star against the Football sport is
        EXPECTED: highlighted in yellow colour indicating that it has
        EXPECTED: been selected as a favourite.
        EXPECTED: 2.Favourite section gets added above the A-Z menu with the selected sport (Football) displayed in that section with a yellow star against it.
        EXPECTED: 3.The same selected favourite sport will be displayed under the A-Z menu as well with the yellow star against it.
        """
        a_to_z_sports_menu_items = self.site.sport_menu.sport_menu_items_group('AZ').items_as_ordered_dict

        # check if sport is available A-Z menu
        self.assertTrue(a_to_z_sports_menu_items[self.sport_name], msg=f'{self.sport_name} sport is not present in A-Z menu')

        # add that sport to favourite
        a_to_z_sports_menu_items[self.sport_name].scroll_to_we()
        a_to_z_sports_menu_items[self.sport_name].mouse_over()
        a_to_z_sports_menu_items[self.sport_name].favourite_checkbox.click()
        self.selected_sports_list.append(self.sport_name)

        # check if sport has favourite checkbox in A-Z menu
        self.assertTrue(a_to_z_sports_menu_items[self.sport_name].has_favourite_checkbox,
                        msg=f'{self.sport_name} sport does not have favourite checkbox even after clicking on favourite checkbox')

        # check favourite checkbox color in A-Z menu
        actual_favourite_checkbox_color = self.get_color_of_before_pseudo_element(
            web_element=a_to_z_sports_menu_items[self.sport_name].favourite_checkbox._we
        )
        self.assertEqual(actual_favourite_checkbox_color, self.expected_favourite_checkbox_color,
                         msg=f'actual favourite checkbox color: {actual_favourite_checkbox_color} does not match '
                             f'expected favourite checkbox color: {self.expected_favourite_checkbox_color}')

        # check favourite title in favourite menu
        actual_favourite_menu_title_frontend = self.site.sport_menu.favourite_sport_menu_items_group.name
        expected_favourite_menu_title_frontend = 'Favourite'
        self.assertEqual(actual_favourite_menu_title_frontend, expected_favourite_menu_title_frontend,
                         msg=f'actual favourite menu title: {actual_favourite_menu_title_frontend} does not match '
                             f'expected favourite menu title: {expected_favourite_menu_title_frontend}')

        favourite_sport_sport_menu_items = self.site.sport_menu.favourite_sport_menu_items_group.items_as_ordered_dict

        # check if sport is available in favourite menu
        self.assertTrue(favourite_sport_sport_menu_items[self.sport_name],
                        msg=f'{self.sport_name} sport is not present in favourite sport menu')

        # check favourite checkbox is present sports of favourite menu
        self.assertTrue(favourite_sport_sport_menu_items[self.sport_name].has_favourite_checkbox(),
                        msg=f'{self.sport_name} sport does not have favourite checkbox even after clicking on favourite checkbox')

        # check favourite checkbox color in favourite menu
        actual_favourite_checkbox_color = self.get_color_of_before_pseudo_element(
            web_element=favourite_sport_sport_menu_items[self.sport_name].favourite_checkbox._we
        )
        self.assertEqual(actual_favourite_checkbox_color, self.expected_favourite_checkbox_color,
                         msg=f'actual favourite checkbox color: {actual_favourite_checkbox_color} does not match '
                             f'expected favourite checkbox color: {self.expected_favourite_checkbox_color}')

    def test_006_try_to_select_multiple_sports_under_thea_z_menu_unti_reaching_the_maxfavouritesproperty_value_set_in_the_cmscurrent_value_set_in_cms_is_2_try_selecting_3sports_under_the_a_z_menu(self):
        """
        DESCRIPTION: Try to select multiple Sports under the
        DESCRIPTION: A-Z menu unti reaching the 'maxFavourites'
        DESCRIPTION: property value set in the CMS.
        DESCRIPTION: (Current value set in CMS is 2 try selecting 3
        DESCRIPTION: sports under the A-Z menu)
        EXPECTED: 1.User should be able to select only 2 sports from the A-Z menu as in CMS only 'Max favourites' is given as "2".
        EXPECTED: 2.After user selecting "2" sports, the star option will not be available against other sports under the A-Z menu. As user has already reached the max favourites value set in CMS.
        """
        a_to_z_sports_menu_items = self.site.sport_menu.sport_menu_items_group('AZ').items_as_ordered_dict

        # select multiple Sports under the A-Z menu until reaching the 'maxFavourites' property value set in the CMS.
        for sports_menu_item_key in a_to_z_sports_menu_items:
            if len(self.selected_sports_list) == self.max_favourites:
                break
            if sports_menu_item_key in self.selected_sports_list:
                continue
            a_to_z_sports_menu_items[sports_menu_item_key].scroll_to_we()
            a_to_z_sports_menu_items[sports_menu_item_key].mouse_over()
            a_to_z_sports_menu_items[sports_menu_item_key].favourite_checkbox.click()
            self.selected_sports_list.append(sports_menu_item_key)
            a_to_z_sports_menu_items = self.site.sport_menu.sport_menu_items_group('AZ').items_as_ordered_dict

        # Verify the behavior of sports menu items after reaching the 'maxFavourites' limit.
        for sports_menu_item_key in a_to_z_sports_menu_items:
            a_to_z_sports_menu_items[sports_menu_item_key].scroll_to_we()
            if sports_menu_item_key in self.selected_sports_list:
                # Ensure that selected sports have a favorite checkbox
                self.assertTrue(a_to_z_sports_menu_items[sports_menu_item_key].has_favourite_checkbox(),
                                msg=f'{sports_menu_item_key} sport does not have favourite checkbox even after clicking on favourite checkbox')
            else:
                # Check that unselected sports do not have a favorite checkbox after the mouse hover
                a_to_z_sports_menu_items[sports_menu_item_key].mouse_over()
                self.assertFalse(a_to_z_sports_menu_items[sports_menu_item_key].has_favourite_checkbox(expected_result=False),
                                 msg=f'{sports_menu_item_key} sport has favourite checkbox, as the script did not clicking on favourite checkbox')

    def test_007_now_try_to_log_out_and_re_login_with_the_sameuser_credentials_and_check_the_favourites_section(self):
        """
        DESCRIPTION: Now try to Log out and re-login with the same
        DESCRIPTION: user credentials and check the favourites section.
        EXPECTED: On re-login the previously selected favourite sports
        EXPECTED: should be retained and displayed under the
        EXPECTED: favourites section.
        """
        self.site.logout()
        self.site.login(username=self.username)

        # After re-login, verifying the previously selected favourite sports are retained and displayed under the favourites section.
        actual_favourite_sport_menu_items = sorted(list(self.site.sport_menu.favourite_sport_menu_items_group.items_as_ordered_dict.keys()))
        expected_selected_sports_list = sorted(self.selected_sports_list)
        self.assertListEqual(actual_favourite_sport_menu_items, expected_selected_sports_list,
                             msg=f'actual favourite sport menu items: {expected_selected_sports_list} does not match '
                                 f'expected selected sports list: {expected_selected_sports_list}')

    def test_008_try_to_deselect_the_sport_thatacirceurotrades_been_selected_as_a_favourite_sport_or_else_by_clicking_on_the_star_option_against_the_sport_from_the_favourite_selection_or_from_the_a_z_menu(
            self):
        """
        DESCRIPTION: Try to deselect the sport that&acirc;&euro;&trade;s been selected as a favourite sport or else by clicking on the star option against the sport from the Favourite selection or from the A-Z menu.
        EXPECTED: 1.The deselected sport should be removed from the Favourite section.
        EXPECTED: 2.The star against the deselected sport should not be highlighted in yellow and user should be able to select it as favourite again incase they wish to.
        EXPECTED: 3.User should be able to select and deselect various sports under A-Z menu within the Max value set up in the CMS.
        """
        favourite_sport_sport_menu_items = self.site.sport_menu.favourite_sport_menu_items_group.items_as_ordered_dict

        # Deselect the sport by clicking on the favorite checkbox against the sports from the favorite menu
        favourite_sport_sport_menu_items[self.sport_name].scroll_to_we()
        favourite_sport_sport_menu_items[self.sport_name].favourite_checkbox.click()
        self.selected_sports_list.remove(self.sport_name)

        wait_for_haul(3)  # Wait for a second for the action to complete.

        # Verify that the sport is removed from the favorite sport menu
        favourite_sport_sport_menu_items = list(self.site.sport_menu.favourite_sport_menu_items_group.items_as_ordered_dict.keys())
        self.assertNotIn(self.sport_name, favourite_sport_sport_menu_items,
                         msg=f'{self.sport_name} sport is available in favourite sport menu, which is not expected after unfavourite it')

        a_to_z_sports_menu_items = self.site.sport_menu.sport_menu_items_group('AZ').items_as_ordered_dict

        # Scroll to the sport, verify it has a favorite checkbox
        a_to_z_sports_menu_items[self.sport_name].scroll_to_we()
        a_to_z_sports_menu_items[self.sport_name].mouse_over()
        self.assertTrue(a_to_z_sports_menu_items[self.sport_name].has_favourite_checkbox(),
                        msg=f'{self.sport_name} sport does not have favourite checkbox')

        # check the color of the favorite checkbox to be white colour
        actual_favourite_checkbox_color = self.get_color_of_before_pseudo_element(
            web_element=a_to_z_sports_menu_items[self.sport_name].favourite_checkbox._we
        )
        expected_favourite_checkbox_color = 'rgb(255, 255, 255)'  # white colour
        self.assertEqual(actual_favourite_checkbox_color, expected_favourite_checkbox_color,
                         msg=f'actual favourite checkbox color: {actual_favourite_checkbox_color} does not match '
                             f'expected favourite checkbox color: {self.expected_favourite_checkbox_color}')

        a_to_z_sports_menu_items = self.site.sport_menu.sport_menu_items_group('AZ').items_as_ordered_dict

        # Loop to deselect selected sports(self.selected_sports_list) by clicking on the star option against the sports from the A-Z menu.
        for favourite_sport in a_to_z_sports_menu_items:
            if favourite_sport in self.selected_sports_list:
                a_to_z_sports_menu_items[favourite_sport].scroll_to_we()
                a_to_z_sports_menu_items[favourite_sport].favourite_checkbox.click()
                self.selected_sports_list.remove(favourite_sport)
                a_to_z_sports_menu_items = self.site.sport_menu.sport_menu_items_group('AZ').items_as_ordered_dict

        wait_for_haul(3)  # Wait for a second for the action to complete.
        self.assertFalse(self.site.sport_menu.has_favourite_sport_menu_items_group(),
                         msg='favourite sport menu items should not be displayed after removing all the selections')

        # verifying that user should be able to select the star option against the sports as favourite again incase they wish to.
        self.test_005_select_the_star_option_against_a_particular_sportavailable_under_a_z_menufootball_is_selected()

        favourite_sport_sport_menu_items = self.site.sport_menu.favourite_sport_menu_items_group.items_as_ordered_dict

        # Deselect all the sport from the favorite menu that the script selected in the earlier steps
        favourite_sport_sport_menu_items[self.sport_name].scroll_to_we()
        favourite_sport_sport_menu_items[self.sport_name].favourite_checkbox.click()
        self.selected_sports_list.remove(self.sport_name)
