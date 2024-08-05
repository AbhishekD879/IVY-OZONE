import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C862149_Verify_tracking_of_Quick_Stake_buttons_in_Betslip(Common):
    """
    TR_ID: C862149
    NAME: Verify tracking of Quick Stake buttons in Betslip
    DESCRIPTION: This test case verifies Quick Stake buttons tracking in Betslip for 'Stake' field
    DESCRIPTION: ***JIRA ticket:***
    DESCRIPTION: BMA-22256 New betslip - quick stake GA
    PRECONDITIONS: - Test Case should be executed on mobile devices
    PRECONDITIONS: - Dev Tools -> Console should be opened
    PRECONDITIONS: - Instruction for mobile devices debugging: https://confluence.egalacoral.com/display/SPI/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: - User has account with positive balance
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Home page is opened
        """
        pass

    def test_002_log_in_with_account_with_positive_balance(self):
        """
        DESCRIPTION: Log in with account with positive balance
        EXPECTED: User is logged in
        """
        pass

    def test_003_open_sport_landing_page(self):
        """
        DESCRIPTION: Open <Sport> landing page
        EXPECTED: - 'Matches' tab is opened by default
        EXPECTED: - 'Today' tab is opened by default
        """
        pass

    def test_004_add_selections_to_the_betslip__open_betslip(self):
        """
        DESCRIPTION: Add selection(s) to the Betslip > Open Betslip
        EXPECTED: Selection(s) are available within Betslip
        """
        pass

    def test_005_set_cursor_over_any_stake_field(self):
        """
        DESCRIPTION: Set cursor over any 'Stake' field
        EXPECTED: Numeric keyboard with 'Quick Stake' buttons is opened
        """
        pass

    def test_006_tap_on_any_quick_stake_button_eg_pluscurrency_symbol5_10_50_100pluskr50_100_500_1000(self):
        """
        DESCRIPTION: Tap on any 'Quick Stake' button (e.g. +<currency symbol>5, 10, 50, 100/+kr50, 100, 500, 1000)
        EXPECTED: Quick Stake amount is shown in a corresponding 'Stake' field
        """
        pass

    def test_007_type_datalayer_in_browser_console__press_enter(self):
        """
        DESCRIPTION: Type "dataLayer" in browser console > press 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: ‘event’ : ‘trackEvent’,
        EXPECTED: ‘eventAction’ : ‘quick stake’,
        EXPECTED: ‘eventCategory’ : ‘quick deposit’,
        EXPECTED: ‘eventLabel’ : ‘<<quick stake value>>’
        EXPECTED: location: 'betslip'
        EXPECTED: });
        """
        pass
