import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C28328_Redeem_Sports_Voucher_Code_for_an_offer_that_is_expired(Common):
    """
    TR_ID: C28328
    NAME: Redeem Sports Voucher Code for an offer that is expired
    DESCRIPTION: This test case verifies redemption of a Voucher Code related to the offer that is expired
    DESCRIPTION: Voucher Codes functionality is controlled by GVC side
    PRECONDITIONS: **JIRA Ticket** : BMA-1754 'As a User I wish to claim my Sports Voucher Code'
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
        DESCRIPTION: Tap on Right Menu icon
        EXPECTED: Right Menu is opened
        """
        pass

    def test_004_tap_offers__free_bets_button(self):
        """
        DESCRIPTION: Tap 'Offers & Free Bets' button
        EXPECTED: 'Offers & Free Bets' page is opened
        """
        pass

    def test_005_tap_voucher_codes_button(self):
        """
        DESCRIPTION: Tap 'Voucher Codes' button
        EXPECTED: 'Redeem Voucher' page is opened
        """
        pass

    def test_006_enter_an_expired_voucher_code_insports_voucher_codefield_and_tap_claim_now_button(self):
        """
        DESCRIPTION: Enter an expired Voucher Code in** 'Sports Voucher Code:' **field and tap 'Claim Now' button
        EXPECTED: Error message** 'The voucher code entered is expired.' **appears
        """
        pass
