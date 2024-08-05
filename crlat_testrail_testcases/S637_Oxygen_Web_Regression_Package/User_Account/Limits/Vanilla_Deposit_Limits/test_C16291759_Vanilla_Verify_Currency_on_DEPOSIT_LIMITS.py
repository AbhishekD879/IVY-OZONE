import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
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

    def test_001_log_in_as_a_user_with_gbp_currency(self):
        """
        DESCRIPTION: Log in as a user with **GBP** currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_002_tap_right_menu_icon____my_account_menu_item(self):
        """
        DESCRIPTION: Tap Right menu icon ->  'My Account' menu item
        EXPECTED: Account MENU is opened
        """
        pass

    def test_003_tap_gambling_controls(self):
        """
        DESCRIPTION: Tap GAMBLING CONTROLS
        EXPECTED: GAMBLING CONTROLS page is open
        """
        pass

    def test_004_check__deposit_limits__image_and_tap__choose__button(self):
        """
        DESCRIPTION: Check  'Deposit Limits ' image and tap  'CHOOSE ' button
        EXPECTED: *   DEPOSIT LIMITS page is open
        EXPECTED: *   In deposit limit section there are 3 text fields with limits: Daily/Weekly/Monthly
        EXPECTED: *   Under the limit text fields there is a current limit displayed with amount and currency
        """
        pass

    def test_005_verify_currency_under_deposit_limit_section_under_limit_text_fields(self):
        """
        DESCRIPTION: Verify currency under deposit limit section under limit text fields
        EXPECTED: Currency matches user's currency - **GBR**
        """
        pass

    def test_006_log_in_as_a_user_with_eur_currency_and_repeat_steps_2_6(self):
        """
        DESCRIPTION: Log in as a user with **EUR** currency and repeat steps 2-6
        EXPECTED: After step 6: Currency matches user's currency - **EUR**
        """
        pass

    def test_007_log_in_as_a_user_with_usd_currency_and_repeat_steps_2_6(self):
        """
        DESCRIPTION: Log in as a user with **USD** currency and repeat steps 2-6
        EXPECTED: After step 6: Currency matches user's currency - **USD**
        """
        pass
