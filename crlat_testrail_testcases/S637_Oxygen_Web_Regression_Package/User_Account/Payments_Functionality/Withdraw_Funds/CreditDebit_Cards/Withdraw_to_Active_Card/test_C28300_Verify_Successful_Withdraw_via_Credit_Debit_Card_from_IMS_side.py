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
class Test_C28300_Verify_Successful_Withdraw_via_Credit_Debit_Card_from_IMS_side(Common):
    """
    TR_ID: C28300
    NAME: Verify Successful Withdraw via Credit/Debit Card from IMS side
    DESCRIPTION: This test case verifies Successful Withdraw functionality via Credit/Debit Card from IMS side.
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   BMA-817 (Customer can withdraw funds from their Coral account)
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has at least one registered card
    PRECONDITIONS: *   Balance of account is enough for withdraw from
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_002_tap_withdraw_button(self):
        """
        DESCRIPTION: Tap 'Withdraw' button
        EXPECTED: *   'Withdraw Funds' page is opened
        EXPECTED: *   Drop-down list with existing registered Payment Methods is shown
        EXPECTED: *   Drop-down is collapsed by default
        """
        pass

    def test_003_select_creditdebit_card_from_drop_down_list(self):
        """
        DESCRIPTION: Select Credit/Debit Card from drop-down list
        EXPECTED: 
        """
        pass

    def test_004_enter_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter amount manually or using quick deposit buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_005_tap_withdraw_funds_button(self):
        """
        DESCRIPTION: Tap 'Withdraw Funds' button
        EXPECTED: *   Successfull message: **"Your withdrawal request has been successful. Reference: #XXXXXXX"** is shown
        EXPECTED: *   User stays on the 'Withdraw Funds' page (refreshed with clear form)
        """
        pass

    def test_006_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is decremented on amount set on step №4
        """
        pass

    def test_007_send_for_uat_team_the_following_info_after_successfull_transaction_for_verifying_that_record_was_created_in_ims___username___the_last_4_digits_of_card___reference_id_number_that_appears_on_the_successful_deposit_message___withdraw_amount(self):
        """
        DESCRIPTION: Send  for UAT team the following info after successfull transaction for verifying that record was created in IMS:
        DESCRIPTION: *   username
        DESCRIPTION: *   the last 4 digits of card
        DESCRIPTION: *   reference ID (number that appears on the successful deposit message)
        DESCRIPTION: *   withdraw amount
        EXPECTED: 
        """
        pass

    def test_008_ask_uat_to_send_you_info_from_created_record_from_ims(self):
        """
        DESCRIPTION: Ask UAT to send you info from created record from IMS
        EXPECTED: 
        """
        pass

    def test_009_verify_info_of_created_record(self):
        """
        DESCRIPTION: Verify info of created record
        EXPECTED: Date & time Account
        EXPECTED: credit card Type Client type
        EXPECTED: platform Merchant
        EXPECTED: method Amount Status Adjustment status Info
        EXPECTED: e.g.
        EXPECTED: 2015-03-30 12:49:55
        EXPECTED: 533336...9676 withdraw casino
        EXPECTED: mobile SC-Gala-3D
        EXPECTED: MasterCard/CFT £10.00 approved - Comment SC-Gala-3D
        """
        pass
