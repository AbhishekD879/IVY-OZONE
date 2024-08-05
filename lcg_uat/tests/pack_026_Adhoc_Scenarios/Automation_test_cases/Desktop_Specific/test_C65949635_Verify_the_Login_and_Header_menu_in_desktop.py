import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul
from voltron.environments.constants.base.football import Football


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.desktop_specific
@pytest.mark.adhoc_suite
@vtest
class Test_C65949635_Verify_the_Login_and_Header_menu_in_desktop(Common):
    """
    TR_ID: C65949635
    NAME: Verify the Login and Header menu in desktop.
    DESCRIPTION: This test case is to validate the Login and Header
    DESCRIPTION: menu in desktop.
    PRECONDITIONS: CMS configuration:
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2. Login with valid credentials
    PRECONDITIONS: 3.Navigate to Menus - Header Menus
    """
    keep_browser_open = True
    sport_name = Football.FOOTBALL_TITLE
    device_name = tests.desktop_default

    def test_001_launch_the__ladbrokescoral_application(self):
        """
        DESCRIPTION: launch the  Ladbrokes/Coral application.
        EXPECTED: Application should be  Launched successfully and by default user is in sports Home page.
        """
        #covered in step 2

    def test_002_click_on_login_cta__from_header_menu_enter_valid_credentials_and_click_on_log_in(self):
        """
        DESCRIPTION: Click on login CTA  from Header Menu, enter valid credentials and click on log in.
        EXPECTED: User must be logged in sucessfully and user must be able to see the Deposit CTA, inbox and avatar menu.
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username, amount='5',
                                                                     card_number='5137651100600001',
                                                                     card_type='mastercard',
                                                                     expiry_month='12',
                                                                     expiry_year='2080',
                                                                     cvv='123'
                                                                     )
        self.site.login(username=username)

    def test_003_verify_the_user_balance_under_account_header(self):
        """
        DESCRIPTION: Verify the user balance under account header.
        EXPECTED: User must be able to see the balance under
        EXPECTED: the user avatar.
        """
        user_balance = float(self.site.header.user_balance)
        self.assertTrue(user_balance,
                        msg='Balance is not displayed at the top right corner')

    def test_004_click_on_inbox_notification_box_next_to_deposit_cta(self):
        """
        DESCRIPTION: Click on inbox notification box next to Deposit CTA.
        EXPECTED: User must be able to see the user email
        EXPECTED: notifications.
        """
        inbox_button =self.site.header.user_panel.my_inbox_button
        self.assertTrue(inbox_button.is_displayed(),
                        msg='"My Inbox" window is not displayed')
        self.site.header.user_panel.my_inbox_button.click()

        if self.site.messages.no_messages_text is not None:
            actual_title_text = self.site.messages.no_messages_text.text
            self.assertEqual(actual_title_text, vec.bma.NO_MESSAGES,
                             msg=f'Actual text: "{actual_title_text}" is not equal with the'
                                 f'Expected text: "{vec.bma.NO_MESSAGES}"')
        else:
            self.assertTrue(self.site.messages.message_details.is_displayed(), msg="Message is not displayed")
        self.site.messages.close_button.click()

    def test_005_verify_the_deposit_cta(self):
        """
        DESCRIPTION: Verify the Deposit CTA.
        EXPECTED: Click on Deposit button.
        EXPECTED: Quick Deposit pop-up should be displayed.
        EXPECTED: Enter the Required amount in the Amount filed and enter CVV.
        EXPECTED: Click on Deposit.
        EXPECTED: Deposited amount must be added to the user wallet.
        """
        # covered in C65949636

    def test_006_verify_the_ladbrokes_logo_on_the_header_menu(self):
        """
        DESCRIPTION: Verify the Ladbrokes logo on the Header Menu.
        EXPECTED: Navigate to any of the sport pages.
        EXPECTED: Now click on Ladbrokes logo on the header menu, user must be navigated back to the sports homepage.
        """
        brand_logo = self.site.header.brand_logo
        self.assertTrue(brand_logo, 'brand_logo not found in Global_header')
        az_links = self.site.sport_menu.sport_menu_items_group('AZ').items_as_ordered_dict
        az_links[self.sport_name].click()
        wait_for_haul(5)
        self.site.header.brand_logo.click()
        actual_url = self.device.get_current_url()
        expected_url = f'https://{tests.HOSTNAME}/'
        self.assertEqual(actual_url, expected_url, msg=f'actual url: {actual_url} is not as expected url: {expected_url}')