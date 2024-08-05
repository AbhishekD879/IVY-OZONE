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
class Test_C28321_Verify_Error_Message_if_no_Data_on_the_Sports_Voucher_Code_in_Response(Common):
    """
    TR_ID: C28321
    NAME: Verify Error Message if no Data on the Sports Voucher Code in Response
    DESCRIPTION: This test case verifies Error Message if no Data on the Sports Voucher Code in Response
    DESCRIPTION: The case is possible if a Sports Voucher Code is not generated in Open Bet for the applicable environment,
    DESCRIPTION: e.g. 1111-1111-1111-1111
    DESCRIPTION: Voucher Codes functionality is controlled by GVC side
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: BMA-1754 'As a User I wish to claim my Sports Voucher Code'
    PRECONDITIONS: BMA-6742 'Display Error message, if we get no data from Server while using voucher codes'
    PRECONDITIONS: **NOTE **:
    PRECONDITIONS: *   Response Information : VOUCHER\_NO\_DATA
    PRECONDITIONS: *   to generate Sports Voucher Codes for STG2 environment contact UAT team
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

    def test_006_enter_a_sports_voucher_code_see_preconditions_insports_voucher_codefield_and_tap_claim_now_button(self):
        """
        DESCRIPTION: Enter a Sports Voucher Code (see preconditions) in** 'Sports Voucher Code:' **field and tap 'Claim Now' button
        EXPECTED: Error message** 'Sorry there is a problem with the Voucher Code you have entered. Please try again and if the problem persists contact Customer Services.' **appears
        """
        pass
