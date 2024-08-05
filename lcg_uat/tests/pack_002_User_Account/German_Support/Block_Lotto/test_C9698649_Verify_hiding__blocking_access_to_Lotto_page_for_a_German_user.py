import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException


# @pytest.mark.lad_prod # VANO-1483, BMA-52554
# @pytest.mark.lad_hl
# @pytest.mark.lad_tst2
# @pytest.mark.lad_stg2
@pytest.mark.high
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C9698649_Verify_hiding__blocking_access_to_Lotto_page_for_a_German_user(Common):
    """
    TR_ID: C9698649
    NAME: Verify hiding & blocking access to 'Lotto' page for a German user
    DESCRIPTION: This test case verifies not displaying 'Lotto' in Sports Ribbon (mobile), A-Z page, Header & Sub Header (desktop) & blocking access to 'Lotto' page via url for a German user
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    """
    keep_browser_open = True
    dialog = None
    lotto_name = None

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Lotto is configured in CMS for:
        PRECONDITIONS: - Sport Pages > Sport Categories > Lotto > General Sport Configuration:  "Show in Sports Ribbon", "Show in AZ", "Is Top Sport" are checked; "Target URi": "/lotto"
        PRECONDITIONS: - Menus > Header Menus > Lotto: "Target URi:" "/lotto"
        PRECONDITIONS: - Header SubMenus > Lotto: "Target URi:" "/lotto"
        PRECONDITIONS: 2. A German user is registered (with "signupCountryCode": "DE" - select Germany as a country during registration)
        PRECONDITIONS: 3. Local storage is cleared (so no "OX.countryCode" is available)
        PRECONDITIONS: 4. A user is not logged in
        """
        all_sport_categories = self.cms_config.get_sport_categories()
        active_sports = []
        for sport in all_sport_categories:
            if not sport['disabled']:
                active_sports.append(sport['imageTitle'])
            if 'lotto' in sport['targetUri']:
                self.__class__.lotto_name = sport['imageTitle']

        if not self.lotto_name:
            raise CmsClientException('Lotto sport category is not configured in the CMS')

        self.__class__.is_mobile = False if self.device_type == 'desktop' else True
        if not self.is_mobile:
            all_header_menu_items = self.cms_config.get_cms_header_menu_items()
            for header_item in all_header_menu_items:
                if 'lotto' in header_item['targetUri']:
                    if header_item['disabled']:
                        raise CmsClientException('Lotto header menu is disabled in CMS')
                    self.__class__.desktop_lotto_name = header_item['linkTitle'].upper()

    def test_001_log_in_as_a_german_user(self):
        """
        DESCRIPTION: Log in as a German user
        EXPECTED: - German user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.site.login(username=tests.settings.german_betplacement_user, async_close_dialogs=False)
        key_value = self.get_local_storage_cookie_value_as_dict('OX.countryCode')
        self.assertEqual(key_value, 'DE', msg=f'Value of cookie "OX.countryCode" does not match expected result "DE". Actual value of "OX.countryCode" is {key_value}')

    def test_002_mobile_tablet_verify_availability_of_lotto_in_sports_menu_ribbon(self):
        """
        DESCRIPTION: **Mobile & Tablet**
        DESCRIPTION: Verify availability of 'Lotto' in 'Sports Menu Ribbon'
        EXPECTED: 'Lotto' is not available is 'Sports Menu Ribbon'
        """
        if self.is_mobile:
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertNotIn(self.lotto_name, all_items, msg=f'{self.lotto_name} is present in Sports Menu Ribbon')

    def test_003_mobile_tablet_navigate_to_all_sports_page_verify_availability_of_lotto_item_in_top_sports_a_z_sports_sections_desktop_verify_availability_of_lotto_item_in_a_z_sports_menu(self):
        """
        DESCRIPTION: **Mobile & Tablet**
        DESCRIPTION: - Navigate to 'All Sports' page
        DESCRIPTION: - Verify availability of 'Lotto' item in 'Top Sports' & 'A-Z Sports' sections
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Verify availability of 'Lotto' item in 'A-Z Sports' menu
        EXPECTED: **Mobile & Tablet**
        EXPECTED: 'Lotto' is not available in 'Top Sports' & 'A-Z Sports' sections
        EXPECTED: **Desktop:**
        EXPECTED: 'Lotto' is not available in 'A-Z Sports' menu
        """
        if self.is_mobile:
            # Top Sports
            self.site.open_sport(name='ALL SPORTS')
            sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
            self.assertNotIn(self.lotto_name, sports, msg=f'{self.lotto_name} is present in Top Sports')
            # A-Z Sports
            sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
            self.assertNotIn(self.lotto_name, sports, msg=f'{self.lotto_name} is present in A-Z Sports')
        else:
            # A - Z Sports
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertNotIn(self.lotto_name, sports, msg=f'{self.lotto_name} is present in A-Z Sports')

    def test_004_desktop_verify_availability_of_lotto_in_header_menu_and_sub_menu(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Verify availability of 'Lotto' in 'Header' menu & sub menu
        EXPECTED: 'Lotto' is not available in 'Header' menu & sub menu
        """
        if not self.is_mobile:
            # Header menu
            sports = self.site.header.top_menu.items_as_ordered_dict
            self.assertNotIn(self.desktop_lotto_name, sports, msg=f'{self.desktop_lotto_name} is present in Header menu')
            # Header sub menu
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertNotIn(self.lotto_name.upper(), sports, msg=f'{self.lotto_name} is present in Header sub menu')

    def test_005_add_lotto_route_to_an_app_url_and_press_enter(self):
        """
        DESCRIPTION: - Add "/lotto" route to an app url
        DESCRIPTION: - Press 'Enter'
        EXPECTED: - German user is navigated to home page
        EXPECTED: - ‘Country Restriction’ pop up appears with text: "We are unable to offer Lotto betting in your jurisdiction." and 'OK' button
        """
        self.device.navigate_to(url=f'{tests.HOSTNAME}/lotto')
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Homepage', timeout=10)
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.bma.COUNTRY_RESTRICTION.header)
        self.assertTrue(self.dialog.name, msg='Country Restriction dialog is not shown')
        pop_up_text = self.dialog.text
        expected_text = vec.bma.COUNTRY_RESTRICTION.lotto_message_body
        self.assertEquals(pop_up_text, expected_text, msg=f'Actual error message: "{pop_up_text}" is not equal to expected: "{expected_text}"')
        self.dialog.ok_button.is_displayed()

    def test_006_tap_ok_button_or_anywhere_outside_the_pop_up(self):
        """
        DESCRIPTION: Tap 'OK' button/anywhere outside the pop up
        EXPECTED: Pop up is closed
        """
        ok_button = self.dialog.ok_button
        ok_button.click()
        dialog_closed = self.dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg='Dialog is not closed after pressing OK button')

    def test_007_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.site.logout()
        key_value = self.get_local_storage_cookie_value_as_dict('OX.countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE". Actual value of "OX.countryCode" is "{key_value}"')

    def test_008_repeat_steps_2_6(self):
        """
        DESCRIPTION: Repeat steps 2-6
        """
        self.test_002_mobile_tablet_verify_availability_of_lotto_in_sports_menu_ribbon()
        self.test_003_mobile_tablet_navigate_to_all_sports_page_verify_availability_of_lotto_item_in_top_sports_a_z_sports_sections_desktop_verify_availability_of_lotto_item_in_a_z_sports_menu()
        self.test_004_desktop_verify_availability_of_lotto_in_header_menu_and_sub_menu()
        self.test_005_add_lotto_route_to_an_app_url_and_press_enter()
        self.test_006_tap_ok_button_or_anywhere_outside_the_pop_up()
