import pytest
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.lad_prod  # VANO-1483, BMA-52554
# @pytest.mark.lad_hl
# @pytest.mark.lad_tst2
# @pytest.mark.lad_stg2
@pytest.mark.high
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_C9701594_Verify_blocking_an_access_to_Lotto_after_registration_of_a_German_user(Common):
    """
    TR_ID: C9701594
    NAME: Verify blocking an access to Lotto after registration of a German user
    DESCRIPTION: This test case verifies whether just registered German user doesn't have access to Lotto
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS (for Roxanne only, not valid for OX102 Ladbrokes Wallet)
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Lotto is configured in CMS for:
        DESCRIPTION: - Sport Pages > Sport Categories > Lotto > General Sport Configuration:  "Show in Sports Ribbon", "Show in AZ", "Is Top Sport" are checked; "Target URi": "/lotto"
        DESCRIPTION: - Menus > Header Menus > Lotto: "Target URi:" "/lotto"
        DESCRIPTION: - Header SubMenus > Lotto: "Target URi:" "/lotto"
        DESCRIPTION: 2. devtools > Application tab > Local Storage > is cleared (so no "OX.countryCode" is available)
        DESCRIPTION: 3. Login pop-up is opened on mobile
        """
        all_sport_categories = self.cms_config.get_sport_categories()
        active_sports = []
        for sport in all_sport_categories:
            if not sport['disabled']:
                active_sports.append(sport['imageTitle'])
        self.assertIn('Lotto', active_sports, msg='Lotto is not present in list of active_sports')
        self.__class__.is_mobile = False if self.device_type == 'desktop' else True

    def test_001_register_new_user_with_germany_as_selected_country_of_residence(self):
        """
        DESCRIPTION: - Tap 'Join now'
        DESCRIPTION: - Fill in all necessary fields to register user
        DESCRIPTION: - Select Country 'Germany'
        DESCRIPTION: - Tap 'Open account', 'Save my preferences'
        DESCRIPTION: - Close Deposit page
        EXPECTED: - German user is navigated back to an app
        EXPECTED: - German user is logged in
        EXPECTED: - German user is navigated to Home page
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.site.register_new_user(country='Germany',
                                    mobile='+4915902935946',
                                    city='Berlin',
                                    post_code='10115',
                                    currency='EUR')
        key_value = self.get_local_storage_cookie_value_as_dict('OX.countryCode')
        self.assertEqual(key_value, 'DE', msg=f'Value of cookie "OX.countryCode" 'f'does not match expected result "DE".'f'Actual value of "OX.countryCode" is {key_value}')

    def test_002_verify_availability_of_lotto_in_sports_menu_ribbon(self):
        """
        DESCRIPTION: **Mobile & Tablet:**
        DESCRIPTION: Verify availability of 'Lotto' in 'Sports Menu Ribbon'
        EXPECTED: 'Lotto' is not available is 'Sports Menu Ribbon'
        """
        if self.is_mobile:
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertNotIn('Lotto', all_items, msg='Lotto is present in Sports Menu Ribbon')

    def test_003_navigate_to_all_sports_page_and_verify_availability_of_lotto_item_in_top_sports_and_a_z_sports_sections(self):
        """
        DESCRIPTION: **Mobile & Tablet*f*
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
            self.assertNotIn('Lotto', sports, msg='Lotto is present in Top Sports')
            # A-Z Sports
            sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
            self.assertNotIn('Lotto', sports, msg='Lotto is present in A-Z Sports')
        if not self.is_mobile:
            # A - Z Sports
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertNotIn('Lotto', sports, msg='Lotto is present in A-Z Sports')

    def test_004_verify_availability_of_lotto_in_header_menu__sub_menu(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Verify availability of 'Lotto' in 'Header' menu & sub menu
        EXPECTED: 'Lotto' is not available in 'Header' menu & sub menu
        """
        if not self.is_mobile:
            # Header menu
            sports = self.site.header.top_menu.items_as_ordered_dict
            self.assertNotIn('LOTTERY', sports, msg='Lottery is present in Header menu')
            # Header sub menu
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertNotIn('LOTTO', sports, msg='Lotto is present in Header sub menu')
