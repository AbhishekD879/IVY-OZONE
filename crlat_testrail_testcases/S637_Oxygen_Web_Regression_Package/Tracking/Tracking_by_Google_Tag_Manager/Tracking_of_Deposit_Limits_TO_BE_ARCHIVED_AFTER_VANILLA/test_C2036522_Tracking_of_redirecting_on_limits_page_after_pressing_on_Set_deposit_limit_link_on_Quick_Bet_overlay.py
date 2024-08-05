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
class Test_C2036522_Tracking_of_redirecting_on_limits_page_after_pressing_on_Set_deposit_limit_link_on_Quick_Bet_overlay(Common):
    """
    TR_ID: C2036522
    NAME: Tracking of redirecting on limits page after pressing on 'Set deposit limit' link on Quick Bet overlay.
    DESCRIPTION: This test case verifies GA tracking of redirecting on limits page after pressing on 'Set deposit limit' link on Quick Bet overlay
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: * Browsers console should be opened
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User doesn't have deposit limits defined
    PRECONDITIONS: * User has registered all supported card types: Visa, Visa Electron, Master Card, Maestro
    PRECONDITIONS: * Balance of card is enough for deposit from
    PRECONDITIONS: In order to get number of credit card the following links can be used:
    PRECONDITIONS: http://www.getcreditcardnumbers.com/how-to-get-a-master-card-credit-card
    PRECONDITIONS: http://www.getcreditcardnumbers.com/how-to-get-a-visa-credit-card
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_sport_raceselection_to_quick_bet(self):
        """
        DESCRIPTION: Add <Sport>/ <Race>selection to Quick Bet
        EXPECTED: Quick bet appears at the bottom of the page
        """
        pass

    def test_003_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * 'Stake' field is pre-populated with value
        EXPECTED: * 'Funds needed for bet "<currency symbol>XX.XX' error message is displayed below 'QUICK BET' header immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A QUICK DEPOSIT' immediately and is enabled by default
        """
        pass

    def test_004_tap_make_a_quick_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A QUICK DEPOSIT' button
        EXPECTED: * Quick Deposit section is displayed over of Quick Bet
        EXPECTED: * 'MAKE A QUICK DEPOSIT' button becomes 'DEPOSIT & PLACE BET' immediately and is disabled by default
        EXPECTED: * 'ADD TO BETSLIP' button becomes 'BACK' immediately and is enabled by default
        """
        pass

    def test_005_clock_on__set_my_deposit_limits_link(self):
        """
        DESCRIPTION: Clock on  'Set my deposit limits' link
        EXPECTED: * 'My Limits' page is opened in the same window
        EXPECTED: * URL is: https://xxx.coral.co.uk/limits
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quick deposit',
        EXPECTED: 'eventAction' : 'set limits'
        EXPECTED: 'location': 'quick bet'
        """
        pass
