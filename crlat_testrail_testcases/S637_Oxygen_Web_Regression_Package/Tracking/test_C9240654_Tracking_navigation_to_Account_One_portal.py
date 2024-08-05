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
class Test_C9240654_Tracking_navigation_to_Account_One_portal(Common):
    """
    TR_ID: C9240654
    NAME: Tracking navigation to 'Account One' portal
    DESCRIPTION: This test case verifies GA tracking of navigating to 'Account One' pages
    PRECONDITIONS: 1. In CMS > System Configuration > Structure: 'ExternalUrls' section with 'Field Name' & 'Field Value' are set up
    PRECONDITIONS: 2. Roxanne app is loaded
    PRECONDITIONS: 3. Login pop-up is opened
    PRECONDITIONS: NOTE: To be able to test tracked GA parameters in Console, ask a developer to 'block' navigation to 'Account One' portal by hatching out an external navigation url to the browser Console.
    """
    keep_browser_open = True

    def test_001_tap_on_forgot_password_link_on_log_in_pop_up(self):
        """
        DESCRIPTION: Tap on 'Forgot password?' link on 'Log In' pop up
        EXPECTED: User is navigated to Account One portal
        EXPECTED: (corresponding 'Account One' navigation url is displayed in Console)
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present:
        EXPECTED: {dataLayer.push( { }
        EXPECTED: }
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'navigation',
        EXPECTED: 'eventAction' : 'my account',
        EXPECTED: 'eventLabel' : '<< LINK NAME >>' e.g. "/personal-details"
        EXPECTED: })
        """
        pass

    def test_003_repeat_steps_1__2_by_tapping_on__forgot_username_link__join_us_here_button(self):
        """
        DESCRIPTION: Repeat Steps 1 -2 by tapping on:
        DESCRIPTION: - 'Forgot username?' link
        DESCRIPTION: - 'Join us here' button
        EXPECTED: 
        """
        pass

    def test_004_log_into_an_app_with_a_user_that_does_not_have_credit_cards(self):
        """
        DESCRIPTION: Log into an app with a user that does not have credit cards
        EXPECTED: User is logged in
        """
        pass

    def test_005_mobiletablettap_on_right_menu_tap_on_deposit_menu_itemdesktoptap_on_right_menu__any_menu_item_that_navigates_to_account_one_eg_deposit(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on Right menu >tap on 'Deposit' menu item
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Tap on Right menu > any menu item that navigates to Account One e.g. Deposit
        EXPECTED: User is navigated to Account One portal
        EXPECTED: (corresponding 'Account One' navigation url is displayed in Console)
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present:
        EXPECTED: {dataLayer.push( { }
        EXPECTED: }
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'navigation',
        EXPECTED: 'eventAction' : 'my account',
        EXPECTED: 'eventLabel' : '<< LINK NAME >>' e.g. "/deposit"
        EXPECTED: })
        """
        pass

    def test_007_repeat_steps_1___2_by_tapping_on_the_next_menu_items__transfer__withdraw__banking_history__view_balance__change_password__redeem_free_bets__personal_details__responsible_gambling__deposit_limits(self):
        """
        DESCRIPTION: Repeat Steps 1 - 2 by tapping on the next menu items:
        DESCRIPTION: - 'Transfer'
        DESCRIPTION: - 'Withdraw'
        DESCRIPTION: - 'Banking History'
        DESCRIPTION: - 'View Balance'
        DESCRIPTION: - 'Change Password'
        DESCRIPTION: - 'Redeem Free Bets'
        DESCRIPTION: - 'Personal Details'
        DESCRIPTION: - 'Responsible Gambling'
        DESCRIPTION: - 'Deposit Limits'
        EXPECTED: 
        """
        pass

    def test_008_mobiletap_on_right_menu__tap_on_deposit_button(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Tap on Right menu > Tap on 'Deposit' button
        EXPECTED: User is navigated to Account One portal
        EXPECTED: (corresponding 'Account One' navigation url is displayed in Console)
        """
        pass

    def test_009_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present:
        EXPECTED: {dataLayer.push( { }
        EXPECTED: }
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'navigation',
        EXPECTED: 'eventAction' : 'my account',
        EXPECTED: 'eventLabel' : '<< LINK NAME >>' e.g. "/responsible-gambling"
        EXPECTED: })
        """
        pass

    def test_010_mobile__add_any_selection_to_quick_bet__enter_stake_higher_than_users_balance__open_quick_deposit__on_quick_deposit_tap_on_set_my_deposit_limits_link(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: - Add any selection to 'Quick Bet'
        DESCRIPTION: - Enter 'Stake' higher than user's 'Balance'
        DESCRIPTION: - Open 'Quick Deposit'
        DESCRIPTION: - On 'Quick Deposit': Tap on 'Set my deposit limits' link
        EXPECTED: User is navigated to Account One portal
        EXPECTED: (corresponding 'Account One' navigation url is displayed in Console)
        """
        pass

    def test_011_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present:
        EXPECTED: {dataLayer.push( { }
        EXPECTED: }
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'navigation',
        EXPECTED: 'eventAction' : 'my account',
        EXPECTED: 'eventLabel' : '<< LINK NAME >>' e.g. "/responsible-gambling"
        EXPECTED: })
        """
        pass

    def test_012_mobile__add_selections_to_the_betslip__open_betslip__tap_on_quick_deposit_link_in_the_right_upper_corner_of_the_betslip(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: - Add selection(s) to the 'Betslip'
        DESCRIPTION: - Open 'Betslip'
        DESCRIPTION: - Tap on 'Quick Deposit' link in the right upper corner of the 'Betslip'
        EXPECTED: User is navigated to Account One portal
        EXPECTED: (corresponding 'Account One' navigation url is displayed in Console)
        """
        pass

    def test_013_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present:
        EXPECTED: {dataLayer.push( { }
        EXPECTED: }
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'navigation',
        EXPECTED: 'eventAction' : 'my account',
        EXPECTED: 'eventLabel' : '<< LINK NAME >>' e.g. "/deposit"
        EXPECTED: })
        """
        pass

    def test_014___add_selections_to_the_betslip__enter_stake_higher_than_users_balance__open_quick_deposit__on_quick_deposit_tap_on_set_my_deposit_limits_link(self):
        """
        DESCRIPTION: - Add selection(s) to the 'Betslip'
        DESCRIPTION: - Enter 'Stake' higher than user's 'Balance'
        DESCRIPTION: - Open 'Quick Deposit'
        DESCRIPTION: - On 'Quick Deposit': Tap on 'Set my deposit limits' link
        EXPECTED: User is navigated to Account One portal
        EXPECTED: (corresponding 'Account One' navigation url is displayed in Console)
        """
        pass

    def test_015_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present:
        EXPECTED: {dataLayer.push( { }
        EXPECTED: }
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'navigation',
        EXPECTED: 'eventAction' : 'my account',
        EXPECTED: 'eventLabel' : '<< LINK NAME >>' e.g. "/responsible-gambling"
        EXPECTED: })
        """
        pass
