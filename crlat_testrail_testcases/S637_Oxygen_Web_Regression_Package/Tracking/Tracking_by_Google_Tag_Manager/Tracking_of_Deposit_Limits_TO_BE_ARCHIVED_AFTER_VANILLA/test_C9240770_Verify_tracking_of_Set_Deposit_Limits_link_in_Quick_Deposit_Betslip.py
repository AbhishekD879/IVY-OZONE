import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C9240770_Verify_tracking_of_Set_Deposit_Limits_link_in_Quick_Deposit_Betslip(Common):
    """
    TR_ID: C9240770
    NAME: Verify tracking of 'Set Deposit Limits' link in 'Quick Deposit' (Betslip)
    DESCRIPTION: This test case verifies tracking of 'Set Deposit Limits' link on 'Quick Deposit' section in the Betslip
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. User is logged in
    PRECONDITIONS: 3. User has credit cards added to his account
    """
    keep_browser_open = True

    def test_001_add_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add selection(s) to the Betslip
        EXPECTED: Selections are added to the Betslip
        """
        pass

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: - Betslip is opened
        EXPECTED: - Added selections are available within the Betslip
        """
        pass

    def test_003_open_quick_deposit__mobile_tap_on_quick_deposit_link_in_the_upper_right_corner_of_the_betslip__tabletdesktop_enter_stake_amount_higher_than_users_limit__tap_on_funds_needed_message(self):
        """
        DESCRIPTION: Open 'Quick Deposit':
        DESCRIPTION: - **Mobile:** Tap on 'Quick Deposit' link in the upper right corner of the Betslip
        DESCRIPTION: - **Tablet&Desktop:** Enter 'Stake' amount higher than user's limit > tap on 'Funds needed..' message
        EXPECTED: 'Quick Deposit' section is opened
        """
        pass

    def test_004_tapclick_on_set_deposit_limits_link(self):
        """
        DESCRIPTION: Tap/click on 'Set Deposit Limits' link
        EXPECTED: **Coral:**
        EXPECTED: User is navigated to 'Limits' page
        EXPECTED: **Ladbrokes:**
        EXPECTED: User is navigated to 'Account One' portal
        """
        pass

    def test_005_type_datalayer_in_browser_console__press_enter(self):
        """
        DESCRIPTION: Type 'datalayer' in browser Console > press 'Enter'
        EXPECTED: DataLayer object is available:
        EXPECTED: {{dataLayer.push( { }
        EXPECTED: }
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quick deposit',
        EXPECTED: 'eventAction' : 'set limits',
        EXPECTED: 'location' : 'betslip'
        EXPECTED: })
        """
        pass
