import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException


# @pytest.mark.lad_prod  # VANO-1483, BMA-52554
# @pytest.mark.lad_hl
# @pytest.mark.lad_tst2
# @pytest.mark.lad_stg2
@pytest.mark.medium
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C9698959_Verify_availability_of_Lotto_pages_for_a_non_german_user(Common):
    """
    TR_ID: C9698959
    NAME: Verify availability of 'Lotto' pages for a non german user
    DESCRIPTION: This test case verifies displaying 'Lotto' in Sports Ribbon (mobile), A-Z page, Header & Sub Header (desktop) & having access to 'Lotto' page via url for a non German user
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    """
    keep_browser_open = True
    lotto_name = None

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Lotto is configured in CMS for:
        PRECONDITIONS: - Sport Pages > Sport Categories > Lotto > General Sport Configuration: "Show in Sports Ribbon", "Show in AZ", "Is Top Sport" are checked; "Target URi": "/lotto"
        PRECONDITIONS: - Menus > Header Menus > Lotto: "Target URi:" "/lotto"
        PRECONDITIONS: - Header SubMenus > Lotto: "Target URi:" "/lotto"
        PRECONDITIONS: - A German user is registered (with "signupCountryCode": "DE" - select Germany as a country during registration)
        PRECONDITIONS: - Local storage is cleared (so no "OX.countryCode" is available)
        PRECONDITIONS: 2. A German user is registered (with "signupCountryCode: "DE" - select Germany as a country during registration)
        PRECONDITIONS: 3. A non-german user is registered
        """
        all_sport_categories = self.cms_config.get_sport_categories()
        for sport in all_sport_categories:
            if 'lotto' in sport['targetUri']:
                if sport['disabled']:
                    raise CmsClientException('Lotto sport category is disabled in CMS')
                if not sport['showInHome']:
                    raise CmsClientException('Lotto sport category is not configured in the CMS to be shown in Sports Ribbon')
                if not sport['isTopSport']:
                    raise CmsClientException('Lotto sport category display is disabled for Top Sport menu')
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

    def test_001_log_in_as_a_german_user__log_out(self):
        """
        DESCRIPTION: Log in as a german user > Log out
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.site.login(username=tests.settings.german_betplacement_user)
        self.site.logout(timeout=10)
        key_value = self.get_local_storage_cookie_value_as_dict('OX.countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "0".'f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_002_log_in_as_a_non_german_user(self):
        """
        DESCRIPTION: Log in as a non german user
        EXPECTED: - Non german user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        self.site.login()
        key_value = self.get_local_storage_cookie_value_as_dict('OX.countryCode')
        self.assertEqual(key_value, 'GB',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "GB".'f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_003_mobile__tabletverify_availability_of_lotto_in_sports_menu_ribbon(self):
        """
        DESCRIPTION: **Mobile & Tablet:**
        DESCRIPTION: Verify availability of 'Lotto' in 'Sports Menu Ribbon'
        EXPECTED: 'Lotto' is available is 'Sports Menu Ribbon'
        """
        if self.is_mobile:
            all_items = self.site.home.menu_carousel.items_as_ordered_dict.keys()
            self.assertIn(self.lotto_name, all_items,
                          msg=f'"{self.lotto_name}" is not present in Sports Menu Ribbon "{all_items}"')

    def test_004_mobile__tablet__navigate_to_all_sports_page__verify_availability_of_lotto_item_in_top_sports__a_z_sports_sectionsdesktopverify_availability_of_lotto_item_in_a_z_sports_menu(
            self):
        """
        DESCRIPTION: **Mobile & Tablet:**
        DESCRIPTION: - Navigate to 'All Sports' page
        DESCRIPTION: - Verify availability of 'Lotto' item in 'Top Sports' & 'A-Z Sports' sections
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Verify availability of 'Lotto' item in 'A-Z Sports' menu
        EXPECTED: **Mobile & Tablet:**
        EXPECTED: 'Lotto' is available in 'Top Sports' & 'A-Z Sports' sections
        EXPECTED: **Desktop:**
        EXPECTED: 'Lotto' is available in 'A-Z Sports' menu
        """
        if self.is_mobile:
            # ** Mobile - 'Top Sports' & 'A-Z Sports'**
            self.site.open_sport(name='All Sports')
            sports = self.site.all_sports.top_sports_section.items_as_ordered_dict.keys()
            self.assertIn(self.lotto_name, sports, msg=f'"{self.lotto_name}" is not present in Top Sports"{sports}"')
            sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
            self.assertIn(self.lotto_name, sports,
                          msg=f'"{self.lotto_name}" is not present in A-Z Sports "{sports.keys()}"')
            # **Desktop - 'A-Z Sports'**
        else:
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict.keys()
            self.assertIn(self.lotto_name, sports, msg=f'"{self.lotto_name}" is not present in Top Sports "{sports}"')

    def test_005_desktopverify_availability_of_lotto_in_header_menu__sub_menu(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Verify availability of 'Lotto' in 'Header' menu & sub menu
        EXPECTED: 'Lotto' is available in 'Header' menu & sub menu
        """
        if self.device_type == 'desktop':
            # Header sub menu
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn(self.lotto_name.upper(), sports,
                          msg=f'"{self.lotto_name.upper()}" is not present in Header sub menu "{sports.keys()}"')

    def test_006_navigate_to_lotto_page(self):
        """
        DESCRIPTION: Navigate to 'Lotto' page
        EXPECTED: 'Lotto' page is opened
        """
        self.navigate_to_page(name='/lotto')
        self.site.wait_content_state(state_name='Lotto')

    def test_007_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: - Non german user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        self.site.back_button.click()
        self.site.logout(timeout=10)
        key_value = self.get_local_storage_cookie_value_as_dict('OX.countryCode')
        self.assertEqual(key_value, 'GB',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "".'f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_008_repeat_steps__3_6(self):
        """
        DESCRIPTION: Repeat steps  3-6
        """
        self.test_003_mobile__tabletverify_availability_of_lotto_in_sports_menu_ribbon()
        self.test_004_mobile__tablet__navigate_to_all_sports_page__verify_availability_of_lotto_item_in_top_sports__a_z_sports_sectionsdesktopverify_availability_of_lotto_item_in_a_z_sports_menu()
        self.test_005_desktopverify_availability_of_lotto_in_header_menu__sub_menu()
        self.test_006_navigate_to_lotto_page()
