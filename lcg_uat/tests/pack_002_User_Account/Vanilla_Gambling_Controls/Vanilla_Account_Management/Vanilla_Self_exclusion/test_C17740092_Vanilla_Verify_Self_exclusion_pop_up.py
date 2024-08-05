import pytest
import tests
import datetime
from tests.base_test import vtest
from voltron.environments import constants as vec
from selenium.webdriver.support.select import Select
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.js_functions import click


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C17740092_Vanilla_Verify_Self_exclusion_pop_up(BaseBetSlipTest):
    """
    TR_ID: C17740092
    NAME: [Vanilla] Verify Self-exclusion pop-up
    DESCRIPTION:
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: My Account -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects the 'Id like to take an irreversible time-out or exclude myself from gaming' option
    PRECONDITIONS: User clicks the 'Self-exclusion' link (bottom of the page) and proceeds with self exclusion
    PRECONDITIONS: User selects the self-exclusion duration, the reason and proceeds to the next page (**remember the selected duration**)
    PRECONDITIONS: User enters the correct password
    """
    keep_browser_open = True
    deposit_amount = 20.00
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: App is loaded
        PRECONDITIONS: User is logged in
        PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
        PRECONDITIONS: User selects the 'Id like to take an irreversible time-out or exclude myself from gaming' option
        PRECONDITIONS: User clicks the 'Self-exclusion' link (bottom of the page) and proceeds with self exclusion
        PRECONDITIONS: User selects the self-exclusion duration, the reason and proceeds to the next page (**remember the selected duration**)
        PRECONDITIONS: User enters the correct password
        """
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_payment_card_and_deposit(amount=self.deposit_amount,
                                                                 card_number=tests.settings.master_card,
                                                                 card_type='mastercard', expiry_month=self.expiry_month,
                                                                 expiry_year=self.expiry_year,
                                                                 cvv=tests.settings.master_card_cvv)
        self.site.login(username=user_name)
        self.site.wait_content_state("Homepage")
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.GAMBLING_CONTROLS.upper())
        self.site.wait_splash_to_hide(10)
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        self.site.account_closure.click_item(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_2)
        self.site.account_closure.continue_button.click()
        self.site.contents.scroll_to_bottom()
        self.site.self_exclusion.self_exclusion_link.scroll_to()
        self_exclusion_link = self.site.self_exclusion.self_exclusion_link
        self.assertTrue(self_exclusion_link.is_displayed(), msg=f'"Self Exclusion" link is not displayed')
        self_exclusion_link.click()
        self.site.wait_splash_to_hide(3)
        self.site.self_exclusion_selection.choose_button.click()
        duration = self.site.self_exclusion_options.duration_options
        self.assertTrue(duration, msg='"Duration options" are not available')
        reason = self.site.self_exclusion_options.reason_options
        self.assertTrue(duration, msg='"Reason options" are not available')
        brands = Select(self.site.self_exclusion_options.brand)
        self.assertTrue(brands, msg='"Brand" is not available')
        brands.select_by_index("1")
        duration[0].click()
        click(reason[0])
        self.assertTrue(self.site.self_exclusion_options.continue_button.is_enabled(),
                        msg=f'"{vec.account.CONTINUE}" button is not enabled')
        self.site.self_exclusion_options.continue_button.click()
        self_exclusion_options = self.site.self_exclusion_options
        self.assertTrue(self_exclusion_options.self_exclude_button.is_displayed(), msg='none')
        self.assertTrue(self_exclusion_options.password_field.is_displayed(), msg='none')
        self_exclusion_options.password_input(tests.settings.default_password)
        self.assertTrue(self_exclusion_options.self_exclude_button.is_enabled(), msg='None')

    def test_001_click_the_self_exclude_button(self):
        """
        DESCRIPTION: Click the 'Self exclude' button
        EXPECTED: Self Exclusion pop-up appears with 2 tickboxes:
        EXPECTED: - confirmation of self-exclusion until selected time and no possibilities of accessing/reactivation account before that time,
        EXPECTED: - confirmation of understanding that it won't be possible to open new accounts during this period
        EXPECTED: - 'No' button is present
        EXPECTED: - 'Yes' button is present
        EXPECTED: ![](index.php?/attachments/get/35871)
        """
        self.site.self_exclusion_options.self_exclude_button.click()
        self.assertTrue(self.site.self_exclusion_options.info_message.is_displayed(), msg='None')
        actual_text = self.site.self_exclusion_options.info_message.text
        self.assertEqual(actual_text, vec.bma.SELF_EXCLUDED_INFO_MESSAGE,
                         msg=f'Actual self-excluded message: "{actual_text}" is not same as Expected self-excluded message: "{vec.bma.SELF_EXCLUDED_INFO_MESSAGE}"')

    def test_002_verify_self_exclusion_time(self):
        """
        DESCRIPTION: Verify self-exclusion time
        EXPECTED: Date is the same as the one selected as self-exclusion duration
        """
        # step to be removed

    def test_003_verify_yes_button(self):
        """
        DESCRIPTION: Verify 'YES' button
        EXPECTED: 'YES' button is disabled
        """
        # step to be removed

    def test_004_check_one_tickbox(self):
        """
        DESCRIPTION: Check one tickbox
        EXPECTED: 'YES' button is disabled
        """
        # step to be removed

    def test_005_check_the_second_tickbox(self):
        """
        DESCRIPTION: Check the second tickbox
        EXPECTED: 'YES' button is enabled
        """
        # step to be removed

    def test_006_click_the_no_button(self):
        """
        DESCRIPTION: Click the 'NO' button
        EXPECTED: Pop-up closes.
        EXPECTED: User stays on 'Self-exclusion' page
        """
        # step to be removed
