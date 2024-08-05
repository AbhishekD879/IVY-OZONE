import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C16291759_Vanilla_Verify_Currency_on_DEPOSIT_LIMITS(Common):
    """
    TR_ID: C16291759
    NAME: [Vanilla| Verify Currency on DEPOSIT LIMITS
    DESCRIPTION: This test case verifies Currency on 'DEPOSIT LIMITS' page for users with different currency settings
    PRECONDITIONS: Make sure you have 3 registered users with different currency settings: GBP, EUR, USD and there are Daily/Weekly/Monthly limits set up.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: setting up daily/weekly/monthly limits to an user
        """
        self.__class__.gbp_user = tests.settings.user_with_deposit_limits
        self.__class__.usd_user = tests.settings.user_with_usd_currency_and_card
        self.__class__.euro_user = tests.settings.user_with_euro_currency_and_card

    def test_001_log_in_as_a_user_with_gbp_currency(self, username=None):
        """
        DESCRIPTION: Log in as a user with **GBP** currency
        EXPECTED: User is logged in successfully
        """
        if username is None:
            self.site.login(username=self.gbp_user)
        else:
            self.site.login(username=username)

    def test_002_tap_right_menu_icon____my_account_menu_item(self):
        """
        DESCRIPTION: Tap Right menu icon ->  'My Account' menu item
        EXPECTED: Account MENU is opened
        """
        self.site.header.right_menu_button.click()

    def test_003_tap_gambling_controls(self):
        """
        DESCRIPTION: Tap GAMBLING CONTROLS
        EXPECTED: GAMBLING CONTROLS page is open
        """
        self.site.right_menu.click_item('Gambling Controls')
        wait_for_result(lambda: self.site.gambling_controls_page.is_displayed(), timeout=20)
        self.assertTrue(self.site.gambling_controls.is_displayed(timeout=20),
                        msg=f'"Gambling Controls" page is not opened')

    def test_004_check__deposit_limits__image_and_tap__choose__button(self):
        """
        DESCRIPTION: Check  'Deposit Limits ' image and tap  'CHOOSE ' button
        EXPECTED: *   DEPOSIT LIMITS page is open
        EXPECTED: *   In deposit limit section there are 3 text fields with limits: Daily/Weekly/Monthly
        EXPECTED: *   Under the limit text fields there is a current limit displayed with amount and currency
        """
        self.site.gambling_controls.choose_button.click()
        self.site.wait_content_state_changed()
        set_deposit_limits_page = self.site.set_deposit_limits
        self.assertTrue(set_deposit_limits_page.is_displayed(), msg='"Set deposit limits" page is not displayed')
        self.__class__.daily_field = set_deposit_limits_page.daily_field
        self.assertTrue(self.daily_field.is_displayed(), msg='"Daily" deposit limit textfield is not displayed')
        self.assertTrue(self.daily_field.current_limit.is_displayed(),
                        msg='"Current Limit" value for "Daily" deposit limit field is not displayed')

        self.__class__.weekly_field = set_deposit_limits_page.weekly_field
        self.assertTrue(self.weekly_field.is_displayed(), msg='"Weekly" deposit limit textfield is not displayed')
        self.assertTrue(self.weekly_field.current_limit.is_displayed(),
                        msg='"Current Limit" value for "Weekly" deposit limit field is not displayed')

        self.__class__.monthly_field = set_deposit_limits_page.monthly_field
        self.assertTrue(self.monthly_field.is_displayed(), msg='"Monthly" deposit limit textfield is not displayed')
        self.assertTrue(self.monthly_field.current_limit.is_displayed(),
                        msg='"Current Limit" value for "Monthly" deposit limit field is not displayed')

    def test_005_verify_currency_under_deposit_limit_section_under_limit_text_fields(self, currency_value='GBP'):
        """
        DESCRIPTION: Verify currency under deposit limit section under limit text fields
        EXPECTED: Currency matches user's currency - **GBR**
        """
        self.assertIn(currency_value, self.daily_field.current_limit.text)
        self.assertIn(currency_value, self.weekly_field.current_limit.text)
        self.assertIn(currency_value, self.monthly_field.current_limit.text)
        self.navigate_to_page('/')
        self.site.wait_content_state('Homepage')
        self.site.logout()

    def test_006_log_in_as_a_user_with_eur_currency_and_repeat_steps_2_6(self):
        """
        DESCRIPTION: Log in as a user with **EUR** currency and repeat steps 2-6
        EXPECTED: After step 6: Currency matches user's currency - **EUR**
        """
        self.test_001_log_in_as_a_user_with_gbp_currency(username=self.euro_user)
        self.test_002_tap_right_menu_icon____my_account_menu_item()
        self.test_003_tap_gambling_controls()
        self.test_004_check__deposit_limits__image_and_tap__choose__button()
        self.test_005_verify_currency_under_deposit_limit_section_under_limit_text_fields(currency_value="EUR")

    def test_007_log_in_as_a_user_with_usd_currency_and_repeat_steps_2_6(self):
        """
        DESCRIPTION: Log in as a user with **USD** currency and repeat steps 2-6
        EXPECTED: After step 6: Currency matches user's currency - **USD**
        """
        self.test_001_log_in_as_a_user_with_gbp_currency(username=self.usd_user)
        self.test_002_tap_right_menu_icon____my_account_menu_item()
        self.test_003_tap_gambling_controls()
        self.test_004_check__deposit_limits__image_and_tap__choose__button()
        self.test_005_verify_currency_under_deposit_limit_section_under_limit_text_fields(currency_value="USD")
