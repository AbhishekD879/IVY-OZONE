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
class Test_C28322_Redeem_Valid_Sports_Voucher_Code(Common):
    """
    TR_ID: C28322
    NAME: Redeem Valid Sports Voucher Code
    DESCRIPTION: This test case verifies redemption of a valid Sports Voucher Code
    DESCRIPTION: Voucher Codes functionality is controlled by GVC side
    PRECONDITIONS: NOTE :
    PRECONDITIONS: to generate Sports Voucher Codes contact GVC team
    """
    keep_browser_open = True

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in(self):
        """
        DESCRIPTION: Log In
        EXPECTED: 
        """
        pass

    def test_003_tap_on_right_menu_icon(self):
        """
        DESCRIPTION: Tap on Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_004_tap_offers__free_bets_button(self):
        """
        DESCRIPTION: Tap 'Offers & Free Bets' button
        EXPECTED: 'Offers & Free Bets' page is opened
        """
        pass

    def test_005_tap_voucher_codes_buttonenter_in_sports_voucher_codefield_correct_valid_voucher_code_eg_24_digits_withhyphen_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_or_24_digits_withouthyphen_and_tap_claim_now_button(self):
        """
        DESCRIPTION: Tap 'Voucher Codes' button
        DESCRIPTION: Enter in 'Sports Voucher Code:' field correct valid Voucher Code (e.g. 24 digits with hyphen 'XXXX-XXXX-XXXX-XXXX-XXXX-XXXX' or 24 digits without hyphen) and tap 'Claim Now' button
        EXPECTED: Success message is displayed in two lines above the 'Enter Promo Code Field' :
        EXPECTED: 'XXXX-XXXX-XXXX-XXXX-XXXX-XXXX
        EXPECTED: Has been credited to your account.',
        EXPECTED: where XXXX-XXXX-XXXX-XXXX-XXXX-XXXX -
        EXPECTED: the voucher code
        """
        pass

    def test_006_enter_moreless_than_24_symbolsin_sports_voucher_codefield_and_tap_claim_now_button(self):
        """
        DESCRIPTION: Enter more/less than 24 symbols in** 'Sports Voucher Code:' **field and tap 'Claim Now' button
        EXPECTED: 'Claim Now' button is disabled
        """
        pass
