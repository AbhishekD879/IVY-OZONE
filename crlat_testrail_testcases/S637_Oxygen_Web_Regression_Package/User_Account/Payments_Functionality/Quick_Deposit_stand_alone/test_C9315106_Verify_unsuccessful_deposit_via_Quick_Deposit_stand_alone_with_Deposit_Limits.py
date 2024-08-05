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
class Test_C9315106_Verify_unsuccessful_deposit_via_Quick_Deposit_stand_alone_with_Deposit_Limits(Common):
    """
    TR_ID: C9315106
    NAME: Verify unsuccessful deposit via 'Quick Deposit' stand alone with 'Deposit Limits'
    DESCRIPTION: Verify unsuccessful deposit via 'Quick Deposit' stand alone with set Deposit Limits
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has credit cards added to his account
    PRECONDITIONS: 3. User has set 'Deposit Limits' in 'Account One' portal
    PRECONDITIONS: 4. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
    """
    keep_browser_open = True

    def test_001_enter_valid_cvv_in_cvv_field(self):
        """
        DESCRIPTION: Enter valid CVV in 'CVV' field
        EXPECTED: - 'CVV' field is populated with entered value
        EXPECTED: - 'Deposit' button remains disabled
        """
        pass

    def test_002_enter_value_in_deposit_amount_field_that_exceeds_set_deposit_limits_dailyweeklymonthly(self):
        """
        DESCRIPTION: Enter value in 'Deposit Amount' field that exceeds set Deposit limits (daily/weekly/monthly)
        EXPECTED: - 'Deposit Amount' field becomes populated with entered value
        EXPECTED: - 'Deposit' button becomes enabled
        """
        pass

    def test_003_tap_on_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Deposit' button
        EXPECTED: **'This deposit would exceed your self-imposed deposit limit. You can check your current limit *here*'** message and info (i) red icon are shown above the credit card placeholder/dropdown.
        EXPECTED: ![](index.php?/attachments/get/36323)
        EXPECTED: WHERE *here* is a tappable/clickable link-label, that redirects user to Account One - Responsible Gaming section, closing 'Quick Deposit' section once tapped/clicked.
        """
        pass
