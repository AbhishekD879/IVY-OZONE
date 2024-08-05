import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C28085_Verify_Currency_on_the_Global_Header_for_Desktop(Common):
    """
    TR_ID: C28085
    NAME: Verify Currency on the Global Header for Desktop
    DESCRIPTION: This test case verifies Currency on the Universal Header for Desktop.
    DESCRIPTION: Need to check on Windows ( IE, Edge, Chrome, FireFox ) and Mac OS (Safari).
    PRECONDITIONS: *   Make sure you have 4 registered users with different currency settings: **GBP**, **EUR**, **USD**, **SEK**
    PRECONDITIONS: In order to verify currency symbol use:
    PRECONDITIONS: CORAL:
    PRECONDITIONS: *   'GBP': symbol = ' **£** ';
    PRECONDITIONS: *   'USD': symbol = ' **$** ';
    PRECONDITIONS: *   'EUR': symbol = ' **€** ';
    PRECONDITIONS: *   'SEK': symbol = ' **Kr** ';
    PRECONDITIONS: LADBROKES:
    PRECONDITIONS: GBP currency
    PRECONDITIONS: AUD currency
    PRECONDITIONS: EUR currency
    PRECONDITIONS: NOK currency
    PRECONDITIONS: NZD currency
    PRECONDITIONS: CHF currency
    PRECONDITIONS: USD currency
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_log_in_user_withgbp_currency(self):
        """
        DESCRIPTION: Log in user with **GBP** currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_003_verify_currency_symbol_near_the_user_balance(self):
        """
        DESCRIPTION: Verify currency symbol near the user balance
        EXPECTED: Currency symbol displayed matches users' currency
        """
        pass

    def test_004_log_out_from_application(self):
        """
        DESCRIPTION: Log out from application
        EXPECTED: 
        """
        pass

    def test_005_log_in_user_with_eur__currency(self):
        """
        DESCRIPTION: Log in user with ' **EUR** ' currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_006_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: The same as on the steps 3-4
        """
        pass

    def test_007_log_in_user_with__usd__currency(self):
        """
        DESCRIPTION: Log in user with ' **USD** ' currency
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: The same as on the steps 3-4
        """
        pass

    def test_009_log_in_user_with_sek__currency(self):
        """
        DESCRIPTION: Log in user with ' **SEK** ' currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_010_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: The same as on the steps 3-4
        """
        pass
