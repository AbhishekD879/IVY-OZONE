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
class Test_C44870134_New_UK_regulation_states_that_users_must_accept_compact_version_of_terms_and_conditions_when_they_are_making_their_first_deposit(Common):
    """
    TR_ID: C44870134
    NAME: New UK regulation states that users must accept compact version of terms and conditions when they are making their first deposit.
    DESCRIPTION: 
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User is depositing for the first time
    """
    keep_browser_open = True

    def test_001_open_deposit_page(self):
        """
        DESCRIPTION: Open 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_002_update_all_required_fieldsenter_valid_cv2_into_cv2_fieldtap_amount_edit_fieldenter_valid_amount_manually(self):
        """
        DESCRIPTION: Update all required fields
        DESCRIPTION: Enter valid CV2 into CV2 field
        DESCRIPTION: Tap Amount edit field
        DESCRIPTION: Enter valid amount manually
        EXPECTED: All the data is showed correctly and Deposit button is active
        """
        pass

    def test_003_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: User sees 'set you deposit limits'
        EXPECTED: No limit/Daily/Weekly/Monthly
        EXPECTED: Check box for Fund Protection Policy (If not ticked: Error message stating 'Please confirm you have read the fund protection policy above'
        """
        pass

    def test_004_select_deposit_limits_and_tick_the_fund_protection_policy_and_submit(self):
        """
        DESCRIPTION: Select Deposit Limits and Tick the Fund Protection Policy and SUBMIT
        EXPECTED: User should not see the popup anymore.
        EXPECTED: Deposit should be successful
        """
        pass
