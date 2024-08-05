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
class Test_C28320_Verify_Redeem_Voucher_page(Common):
    """
    TR_ID: C28320
    NAME: Verify 'Redeem Voucher' page
    DESCRIPTION: This test case verifies 'Redeem Voucher' page
    PRECONDITIONS: **JIRA Tickets** :
    PRECONDITIONS: BMA-1754 'As a User I wish to claim my Sports Voucher Code'
    PRECONDITIONS: BMA-6570 '"View all Offers" button should navigate a customer to 'Promotions' page'
    PRECONDITIONS: BMA-1755 'As a User I wish to claim my Gaming Voucher Code'
    PRECONDITIONS: **NOTE** :
    PRECONDITIONS: *   to generate Sports Voucher Codes for STG2 environment contact UAT team
    PRECONDITIONS: *   to generate Gaming Voucher Codes for TST2 and STG2 environments contact UAT team
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

    def test_005_tap_voucher_codes_button(self):
        """
        DESCRIPTION: Tap 'Voucher Codes' button
        EXPECTED: 1.  'Redeem Voucher' page is opened with Back button present
        EXPECTED: 2.  Two sections 'Sports Voucher Code' and 'Gaming Voucher Code' are expanded by default. It is possible to collapse each section
        EXPECTED: 3.  'Sports Voucher Code:' field, 'Claim Now' and 'View all Offers' buttons are present
        EXPECTED: 4.  Placeholder 'Enter Promo Code' should be present in 'Sports Voucher Code:' field
        EXPECTED: 5.  'Gaming Voucher Code:' field, 'Claim Now' and 'View all Offers' buttons are present (if available)
        EXPECTED: 6.  Placeholder 'Enter Promo Code' should be present in 'Gaming Voucher Code:' field
        """
        pass

    def test_006_verify_back_button(self):
        """
        DESCRIPTION: Verify Back button
        EXPECTED: User gets back to a previous page
        """
        pass

    def test_007_verify_claim_now_button_of_sports_voucher_code_section(self):
        """
        DESCRIPTION: Verify 'Claim Now' button of 'Sports Voucher Code' section
        EXPECTED: 'Claim Now' buttons is always disabled, only when a valid voucher code is entered it becomes enabled
        """
        pass

    def test_008_verify_claim_now_button_of_gaming_voucher_code_section_if_available(self):
        """
        DESCRIPTION: Verify 'Claim Now' button of 'Gaming Voucher Code' section (if available)
        EXPECTED: 'Claim Now' button becomes enabled if a user enters one or more characters into the input box
        """
        pass

    def test_009_verify_view_all_offers_buttons(self):
        """
        DESCRIPTION: Verify 'View all Offers' buttons
        EXPECTED: User is navigated to the 'Promotions' page after tapping on any of two 'View all Offers' buttons
        """
        pass
