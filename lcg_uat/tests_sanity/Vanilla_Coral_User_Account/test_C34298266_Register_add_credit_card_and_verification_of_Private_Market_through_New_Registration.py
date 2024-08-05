import pytest
import datetime
import tests
import voltron.environments.constants as vec
from crlat_ob_client.offer import Offer
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Private_Markets.BasePrivateMarketsTest import BasePrivateMarketsTest


# @pytest.mark.tst2
# @pytest.mark.stg2 Removed tst2, stg2 markers for NA test case
# @pytest.mark.prod # Private markets can not be configured on prod
# @pytest.mark.hl # Private markets can not be configured on hl
@pytest.mark.medium
@pytest.mark.private_markets
@pytest.mark.user_account
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.na  # VANO-1395-There is No automated deposit notification triggered to Ladbrokes,this feature is removed
@vtest
class Test_C34298266_Register_add_credit_card_and_verification_of_Private_Market_through_New_Registration(BasePrivateMarketsTest):
    """
    TR_ID: C34298266
    NAME: Register, add credit card and verification of Private Market through New Registration
    DESCRIPTION: Verify that the customer can see Private Markets through New Registration journey.
    DESCRIPTION: * NOTE: TC requires backoffice modifications. If no access/offers created in PROD backoffice, case could be run on TST envs
    PRECONDITIONS: * Make sure that the Private Markets Offer is created and trigger is set for newly registered users ('First deposit' trigger type).
    PRECONDITIONS: * Register new valid user without first deposit
    PRECONDITIONS: General Private Market instruction: https://confluence.egalacoral.com/display/SPI/How+to+Setup+and+Use+Private+Markets
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Register new valid user
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=self.username)
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        self.__class__.card_date = f'{now.month:02d}/{shifted_year[:-2]}'

    def test_001_press_tap_on_deposit_button(self):
        """
        DESCRIPTION: Press/tap on 'Deposit' button
        EXPECTED: User is navigated to Deposit screen
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open Right Menu')
        self.site.right_menu.click_item(item_name=self.site.window_client_config.cashier_menu_title)
        self.site.right_menu.click_item(item_name=self.site.window_client_config.deposit_menu_title)
        self.assertTrue(self.site.deposit.is_displayed(scroll_to=False), msg='"Deposit" menu is not displayed')

    def test_002_choose_any_of_the_available_credit_card_deposit_methods_and_fill_in_the_required_data(self):
        """
        DESCRIPTION: Choose any of the available credit card deposit methods and fill in the required data on the next page:
        DESCRIPTION: * Amount of deposit
        DESCRIPTION: * Credit card number
        DESCRIPTION: * Expiry Date - any valid date in the future
        DESCRIPTION: * CVV2 code
        DESCRIPTION: And click "Deposit" button
        EXPECTED: * "Your deposit of XX.XX GBR has been successfully" message is displayed on green background.
        EXPECTED: * Transaction details are displayed
        EXPECTED: * 'OK' and 'Make another deposit' buttons are displayed
        EXPECTED: where XX.XX - amount entered;
        EXPECTED: GBR - any currency type chosen
        """
        deposit_amount = 5
        self.site.select_deposit_method.master_card_button.click()
        self.assertTrue(self.site.deposit.is_displayed(), msg='"Deposit page" is not displayed')
        self.site.deposit.add_new_card_and_deposit(amount=deposit_amount,
                                                   cvv_2=tests.settings.master_card_cvv,
                                                   card_number=tests.settings.visa_card,
                                                   expiry_date=self.card_date)
        expected = vec.gvc.DEPOSIT_SUCCESSFUL_MESSAGE.format(deposit_amount)
        self.__class__.transaction_details = self.site.deposit_transaction_details
        actual = self.transaction_details.successful_message
        self.assertEqual(actual, expected,
                         msg=f'Actual message "{actual}" != Expected "{expected}"')
        ok_button = self.transaction_details.ok_button.is_displayed()
        self.assertTrue(ok_button, msg='"OK" button is not present')
        another_deposit_btn = self.transaction_details.make_another_deposit_button.is_displayed()
        self.assertTrue(another_deposit_btn, msg='"Make Another Deposit" button is not present')

    def test_003_click_ok_button(self):
        """
        DESCRIPTION: Click 'OK' button
        EXPECTED: * User is redirected to Homepage
        EXPECTED: * The customer can see the Private Market at the first tab selected by default
        """
        self.transaction_details.ok_button.click()
        self.site.wait_content_state(state_name='HomePage')

        offer_id = self.ob_config.backend.ob.first_deposit_offer.default_offer.id
        # give offer manually because the offer cannot be triggered automatically on tst2
        offer = Offer(env=tests.settings.backend_env, brand=self.brand)
        offer.give_offer(username=self.username, offer_id=offer_id)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        tab_name = self.expected_sport_tabs.private_market
        if self.device_type == 'mobile':
            tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.assertTrue(tabs, msg='No tabs are displayed at the Home page')
            first_tab_name, _ = list(tabs.items())[0]
            self.assertEqual(tab_name, first_tab_name,
                             msg=f'Tab "{tab_name}" is not in the first place in list of tabs: "{tabs.keys()}"')
            self.assertTrue(tabs[tab_name].is_selected(), msg=f'"{tab_name}" tab is not selected by default')
        else:
            self.assertTrue(self.site.home.get_module_content(self.expected_sport_tabs.private_market),
                            msg=f'Module "{self.expected_sport_tabs.private_market}" is not present')
