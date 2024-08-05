import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C9315086_Verify_numeric_keyboard_displaying_on_Quick_Deposit_stand_alone_section(Common):
    """
    TR_ID: C9315086
    NAME: Verify numeric keyboard displaying on 'Quick Deposit' stand alone section
    DESCRIPTION: This test case verifies numeric keyboard displaying on 'Quick Deposit' stand alone section
    DESCRIPTION: AUTOTEST
    DESCRIPTION: Mobile: [C16473748]
    DESCRIPTION: Desktop : [C16976044]
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. User has credit cards added to his account in 'Account One' portal;
    PRECONDITIONS: 3. User is logged in;
    PRECONDITIONS: 4. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
    """
    keep_browser_open = True

    def test_001___________tap_in_cvv_field(self):
        """
        DESCRIPTION: *          Tap in 'CVV' field
        EXPECTED: *          - 'CVV' field becomes focused
        EXPECTED: *          - Numeric keyboard without 'Quick stakes' buttons appears
        EXPECTED: *          - '.' button is disabled on a numeric keyboard
        """
        pass

    def test_002___________tap_in_deposit_amount_field(self):
        """
        DESCRIPTION: *          Tap in 'Deposit Amount' field
        EXPECTED: *          - 'CVV' field becomes unfocused
        EXPECTED: *          - 'Deposit Amount' field becomes focused
        EXPECTED: *          - Numeric keyboard without 'Quick Stakes' buttons remains being shown
        EXPECTED: *          - '.' button becomes enabled on a numeric keyboard
        """
        pass

    def test_003___________tap_anywhere_outside_the_cvv_or_deposit_amount_fields__tap_enter_on_the_keyboard__tap_on___plus___or_______button(self):
        """
        DESCRIPTION: *          Tap anywhere outside the 'CVV' or 'Deposit Amount' fields / tap 'Enter' on the keyboard / tap on   '+'   or   '-'   button
        EXPECTED: *          Keyboard is closed
        """
        pass
