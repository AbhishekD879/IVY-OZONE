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
class Test_C44870351_Verify_the_availability_and_the_redemption_of_the_sports_and_gaming_voucher_code(Common):
    """
    TR_ID: C44870351
    NAME: Verify the availability and the redemption of the sports and gaming voucher code.
    DESCRIPTION: 
    PRECONDITIONS: 1. User is logged in the application.
    PRECONDITIONS: 2. User must have a valid sports and gaming voucher code.
    """
    keep_browser_open = True

    def test_001_click_on_the_avatar__offers__free_bets__voucher_codes(self):
        """
        DESCRIPTION: Click on the Avatar > Offers & Free bets > Voucher codes
        EXPECTED: A section for entering promotion code (sports voucher code) is displayed.
        """
        pass

    def test_002_enter_the_valid_voucher_code_for_sports_and_click_on_submit_verify(self):
        """
        DESCRIPTION: Enter the valid voucher code for sports and click on Submit. Verify.
        EXPECTED: The sports voucher code can be entered, submitted and is accepted.
        """
        pass

    def test_003_enter_an_invalid_voucher_code_for_sports_and_click_on_submit_verify(self):
        """
        DESCRIPTION: Enter an invalid voucher code for sports and click on Submit. Verify.
        EXPECTED: An appropriate error message is displayed and the invalid sports voucher code is not accepted.
        """
        pass

    def test_004_click_back_button(self):
        """
        DESCRIPTION: Click Back(<) button
        EXPECTED: The user is navigated to Home page (previous page)
        """
        pass

    def test_005_again_click_on_the_avatar__offers__free_bets__voucher_codes(self):
        """
        DESCRIPTION: Again Click on the Avatar > Offers & Free bets > Voucher codes
        EXPECTED: A section for entering promotion code (sports voucher code) is displayed.
        """
        pass

    def test_006_enter_the_valid_voucher_code_for_gaming_and_click_on_submit_verify(self):
        """
        DESCRIPTION: Enter the valid voucher code for gaming and click on Submit. Verify.
        EXPECTED: The gaming voucher code can be entered, submitted and is accepted.
        """
        pass

    def test_007_enter_an_invalid_voucher_code_for_gaming_and_click_on_submit_verify(self):
        """
        DESCRIPTION: Enter an invalid voucher code for gaming and click on Submit. Verify.
        EXPECTED: An appropriate error message is displayed and the invalid gaming voucher code is not accepted.
        """
        pass
