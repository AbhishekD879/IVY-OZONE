import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.promotions_banners_offers
@vtest
class Test_C28057_Offers_displaying_with_different_VIP_levels_when_Show_to_Existing_users_option_value(Common):
    """
    TR_ID: C28057
    NAME: Offers displaying with different VIP levels when 'Show to Existing users' option value
    DESCRIPTION: This test case verifies Offers displaying for users with different VIP levels when 'Show to Existing users' option value is set
    PRECONDITIONS: 1) To load CMS use the next links:
    PRECONDITIONS: DEV -  https://coral-cms-dev0.symphony-solutions.eu/login
    PRECONDITIONS: TST2 -  https://coral-cms-tst2.symphony-solutions.eu/login
    PRECONDITIONS: STG2 - https://coral-cms-stg2.symphony-solutions.eu/login
    PRECONDITIONS: HL -  https://coral-cms-hl.symphony-solutions.eu/login
    PRECONDITIONS: PROD -  https://coral-cms.symphony-solutions.eu/login
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 2) Create several Offer modules with Offer images inside via CMS using the next path:
    PRECONDITIONS: * Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: * Offers -> Offers -> Create Offer
    PRECONDITIONS: 3) 'Show to Existing Users' option value is set for Offers
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    no_vip_offer = 'offer with no vip C28057'
    vip_less_than_X_offer = 'offer with vip_less_X C28057'
    vip_X_offer = 'offer with vip_X C28057'
    vip_greater_than_X_offer = 'offer with vip_greater_X C28057'

    def get_right_column_items(self):
        self.device.refresh_page()
        sleep(2)
        right_column_items = self.site.right_column.items_as_ordered_dict
        self.assertTrue(right_column_items, msg='Right menu items not found')
        module = 'PROMOTIONS' if self.brand == 'ladbrokes' and tests.settings.backend_env == 'prod' else 'OFFER MODULES'
        offers = right_column_items.get(module).items_as_ordered_dict
        self.assertTrue(offers, msg='No Offer Modules found')
        self.__class__.offer_names = list(offers.keys())

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create offers
        EXPECTED: Created required offers
        """
        all_cms_offer_modules = self.cms_config.get_offer_modules()
        no_vip_offer_module = next(
            (module for module in all_cms_offer_modules if module.get('name') == f'{self.no_vip_offer}'), None)
        if not no_vip_offer_module:
            no_vip_offer_module = self.cms_config.create_offer_module(name=self.no_vip_offer)
        no_vip_offer_module_id = no_vip_offer_module.get('id')
        self.cms_config.add_offer(offer_module_id=no_vip_offer_module_id, showOfferTo='existing')

        vip_less_than_X_offer_module = next(
            (module for module in all_cms_offer_modules if module.get('name') == f'{self.vip_less_than_X_offer}'), None)
        if not vip_less_than_X_offer_module:
            vip_less_than_X_offer_module = self.cms_config.create_offer_module(name=self.vip_less_than_X_offer)
        vip_less_than_X_offer_module_id = vip_less_than_X_offer_module.get('id')
        vip_level = '11' if self.brand == 'bma' else '60'
        self.cms_config.add_offer(offer_module_id=vip_less_than_X_offer_module_id, vipLevelsInput=vip_level, showOfferTo='existing')

        vip_X_offer_module = next(
            (module for module in all_cms_offer_modules if module.get('name') == f'{self.vip_X_offer}'), None)
        if not vip_X_offer_module:
            vip_X_offer_module = self.cms_config.create_offer_module(name=self.vip_X_offer)
        vip_X_offer_module_id = vip_X_offer_module.get('id')
        vip_level = '13' if self.brand == 'bma' else '62'
        self.cms_config.add_offer(offer_module_id=vip_X_offer_module_id, vipLevelsInput=vip_level, showOfferTo='existing')

        vip_greater_than_X_offer_module = next(
            (module for module in all_cms_offer_modules if module.get('name') == f'{self.vip_greater_than_X_offer}'),
            None)
        if not vip_greater_than_X_offer_module:
            vip_greater_than_X_offer_module = self.cms_config.create_offer_module(name=self.vip_greater_than_X_offer)
        vip_greater_than_X_offer_module_id = vip_greater_than_X_offer_module.get('id')
        vip_level = '14' if self.brand == 'bma' else '77'
        self.cms_config.add_offer(offer_module_id=vip_greater_than_X_offer_module_id, vipLevelsInput=vip_level, showOfferTo='existing')

    def test_001_clear_all_cookies_and_load_oxygen_application(self):
        """
        DESCRIPTION: Clear all cookies and load Oxygen application
        EXPECTED: *   'viplevel' cookie is NOT present in browser
        EXPECTED: *   'Existing user:True' cookie is NOT present to browser
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_splash_to_hide()
        cookie_value = self.get_local_storage_cookie_value('OX.existingUser')
        self.assertFalse(cookie_value,
                         msg=f'"ExistingUser" cookie: "{cookie_value}", expected empty or not present')

    def test_002_select_offer_with_empty_include_vip_levels_option_value_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select offer with empty 'Include VIP Levels' option value and verify its displaying
        EXPECTED: Offer is NOT displayed in application
        """
        self.get_right_column_items()
        self.assertNotIn(self.no_vip_offer.upper(), self.offer_names,
                         msg=f'Offer: "{self.no_vip_offer.upper()}" option value is not displayed in "{self.offer_names}"')

    def test_003_select_offer_with_include_vip_levels__x_and_verify_offer_displaying(self):
        """
        DESCRIPTION: Select Offer with 'Include VIP levels'  = 'X' and verify Offer displaying
        EXPECTED: Offer is NOT displayed in application
        """
        self.assertNotIn(self.vip_X_offer.upper(), self.offer_names,
                         msg=f'Offer: "{self.vip_X_offer.upper()}" option value is not displayed in "{self.offer_names}"')

    def test_004_login_to_application_with_user_for_which_viplevel__x(self):
        """
        DESCRIPTION: Login to application with user for which 'viplevel' = 'X'
        EXPECTED:
        """
        username = tests.settings.gold_user_vip_level_13 if self.brand == 'bma' else tests.settings.gold_user_vip_level_62
        self.site.login(username=username)

    def test_005_select_offer_with_empty_include_vip_levels_option_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select Offer with empty 'Include VIP levels' option and verify its displaying
        EXPECTED: Offer is displayed in application
        """
        self.get_right_column_items()
        self.assertIn(self.no_vip_offer.upper(), self.offer_names,
                      msg=f'Offer: "{self.no_vip_offer.upper()}" option value is not displayed in "{self.offer_names}"')

    def test_006_select_offer_with_include_vip_levels__x_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Offer with 'Include VIP levels' = 'X' and verify its displaying in application
        EXPECTED: Offer is displayed in application
        """
        self.assertIn(self.vip_X_offer.upper(), self.offer_names,
                      msg=f'Offer: "{self.vip_X_offer.upper()}" option value is not displayed in "{self.offer_names}"')

    def test_007_select_offer_with_include_vip_levels__x_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Offer with 'Include VIP levels' <> 'X' and verify its displaying in application
        EXPECTED: Offer is NOT displayed in application
        """
        self.assertNotIn(self.vip_greater_than_X_offer.upper(), self.offer_names,
                         msg=f'Offer: "{self.vip_greater_than_X_offer.upper()}" option value is displayed in "{self.offer_names}"')
        self.assertNotIn(self.vip_less_than_X_offer.upper(), self.offer_names,
                         msg=f'Offer: "{self.vip_less_than_X_offer.upper()}" option value is displayed in "{self.offer_names}"')

    def test_008_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED:
        """
        self.site.logout()

    def test_009_repeat_steps_5_7(self):
        """
        DESCRIPTION: Repeat steps #5-7
        EXPECTED:
        """
        self.test_005_select_offer_with_empty_include_vip_levels_option_and_verify_its_displaying()
        self.test_006_select_offer_with_include_vip_levels__x_and_verify_its_displaying_in_application()
        self.test_007_select_offer_with_include_vip_levels__x_and_verify_its_displaying_in_application()
