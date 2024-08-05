import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.promotions_banners_offers
@vtest
class Test_C28049_Offers_displaying_to_New_or_Existing_or_Both_users(Common):
    """
    TR_ID: C28049
    NAME: Offers displaying to New or Existing or Both users
    DESCRIPTION: This test case verifies Offers displaying to New or Existing or Both users
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
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    offer_for_both = 'Show for both C28049'
    offer_for_existing = 'Show for existing C28049'
    offer_for_new = 'Show for new C28049'

    def test_000_preconditions(self):
        """
         DESCRIPTION: Create offers
         EXPECTED: Created offers
        """
        all_cms_offer_modules = self.cms_config.get_offer_modules()
        both_offer_module = next((module for module in all_cms_offer_modules if module.get('name') == f'{self.offer_for_both}'), None)
        if not both_offer_module:
            both_offer_module = self.cms_config.create_offer_module(name=self.offer_for_both)
        existing_offer_module = next((module for module in all_cms_offer_modules if module.get('name') == f'{self.offer_for_existing}'), None)
        if not existing_offer_module:
            existing_offer_module = self.cms_config.create_offer_module(name=self.offer_for_existing)
        new_offer_module = next((module for module in all_cms_offer_modules if module.get('name') == f'{self.offer_for_new}'), None)
        if not new_offer_module:
            new_offer_module = self.cms_config.create_offer_module(name=self.offer_for_new)

        both_offer_module_id = both_offer_module.get('id')
        existing_offer_module_id = existing_offer_module.get('id')
        new_offer_module_id = new_offer_module.get('id')
        self.cms_config.add_offer(offer_module_id=both_offer_module_id)
        self.cms_config.add_offer(showOfferTo='existing', offer_module_id=existing_offer_module_id)
        self.cms_config.add_offer(showOfferTo='new', offer_module_id=new_offer_module_id)

    def test_001_clear_browser_cookies_and_load_oxygen_applicationdo_not_log_in_to_the_application_and_verify_offers_displaying(self):
        """
        DESCRIPTION: Clear browser cookies and load Oxygen application.
        DESCRIPTION: Do not log in to the application and verify Offers displaying.
        EXPECTED: *   Offers with 'Show for Both' option value are displayed
        EXPECTED: *   Offers with 'Show for New Users' are displayed
        EXPECTED: *   Offers with 'Show for Existing Users' option value are NOT displayed
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_splash_to_hide()

        right_column_items = self.site.right_column.items_as_ordered_dict
        self.assertTrue(right_column_items, msg='Right menu items not found')
        offers = right_column_items.get('OFFER MODULES').items_as_ordered_dict
        self.assertTrue(offers, msg='No Offer Modules found')
        offer_names = list(offers.keys())
        self.assertIn(self.offer_for_both.upper(), offer_names, msg=f'Offer with Show for Both: "{self.offer_for_both}" option value is not displayed in "{offer_names}"')
        self.assertIn(self.offer_for_new.upper(), offer_names, msg=f'Offer with Show for New user: "{self.offer_for_new}" option value is not displayed in "{offer_names}"')
        self.assertNotIn(self.offer_for_existing.upper(), offer_names, msg=f'Offer with Show for Existing user: "{self.offer_for_existing}" option value is displayed')

    def test_002_log_in_to_the_application_for_the_first_time_using_the_browser_with_cleared_cookiesverify_cookie_creation_in_resources___cookies(self):
        """
        DESCRIPTION: Log in to the application for the first time using the browser with cleared cookies.
        DESCRIPTION: Verify cookie creation in Resources -> Cookies.
        EXPECTED: *   'ExistingUser: True' cookie is added
        """
        self.site.login()
        cookie_value = self.get_local_storage_cookie_value('OX.existingUser')
        self.assertTrue(cookie_value,
                        msg=f'"ExistingUser" cookie: "{cookie_value}", is not present')

    def test_003_verify_offers_displaying_after_cookie_existinguser_true_cookie_was_added(self):
        """
        DESCRIPTION: Verify Offers displaying after cookie 'ExistingUser: True' cookie was added
        EXPECTED: *   Offers with 'Show for Existing Users' option value are displayed
        EXPECTED: *   Offers with 'Show for Both' option value are displayed
        EXPECTED: *   Offers with 'Show for New Users' are NOT displayed
        """
        right_column_items = self.site.right_column.items_as_ordered_dict
        self.assertTrue(right_column_items, msg='Right menu items not found')
        offers = right_column_items.get('OFFER MODULES').items_as_ordered_dict
        self.assertTrue(offers, msg='No Offer Modules found')

        offer_names = list(offers.keys())
        self.assertIn(self.offer_for_existing.upper(), offer_names,
                      msg=f'Offer with Show for Existing user: "{self.offer_for_existing}" option value is not displayed in "{offer_names}"')
        self.assertIn(self.offer_for_both.upper(), offer_names,
                      msg=f'Offer with Show for Both: "{self.offer_for_both}" option value is not displayed in "{offer_names}"')
        self.assertNotIn(self.offer_for_new.upper(), offer_names,
                         msg=f'Offer with Show for New user: "{self.offer_for_new}" option value is displayed')

    def test_004_log_out_from_the_application_the_cookie_is_already_added_to_the_browserverify_offers_displaying_in_the_application(self):
        """
        DESCRIPTION: Log out from the application (the cookie is already added to the browser).
        DESCRIPTION: Verify Offers displaying in the application.
        EXPECTED: *   Offers with 'Show for Existing Users' option value are displayed
        EXPECTED: *   Offers with 'Show for Both' option value are displayed
        EXPECTED: *   Offers with 'Show for New Users' are NOT displayed
        """
        self.site.logout()
        right_column_items = self.site.right_column.items_as_ordered_dict
        self.assertTrue(right_column_items, msg='Right menu items not found')
        offers = right_column_items.get('OFFER MODULES').items_as_ordered_dict
        self.assertTrue(offers, msg='No Offer Modules found')

        offer_names = list(offers.keys())
        self.assertIn(self.offer_for_existing.upper(), offer_names,
                      msg=f'Offer with Show for Existing user: "{self.offer_for_existing.upper()}" option value is not displayed in "{offer_names}"')
        self.assertIn(self.offer_for_both.upper(), offer_names,
                      msg=f'Offer with Show for Both: "{self.offer_for_both}" option value is not displayed in "{offer_names}"')
        self.assertNotIn(self.offer_for_new.upper(), offer_names,
                         msg=f'Offer with Show for New user: "{self.offer_for_new}" option value is displayed')
