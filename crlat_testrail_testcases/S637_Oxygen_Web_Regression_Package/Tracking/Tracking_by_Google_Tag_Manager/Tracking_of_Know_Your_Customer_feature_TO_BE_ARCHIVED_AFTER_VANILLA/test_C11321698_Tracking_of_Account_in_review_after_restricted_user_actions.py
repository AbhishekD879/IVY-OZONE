import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C11321698_Tracking_of_Account_in_review_after_restricted_user_actions(Common):
    """
    TR_ID: C11321698
    NAME: Tracking of Account in review after restricted user actions
    DESCRIPTION: Test case verifies Account in Review overlay display when user performs deposit / place bet / freebet/ withdraw and Account in Review closure
    PRECONDITIONS: KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: Note: After deposit / place bet / freebet/ withdraw action user is supposed to have "Verification_Review" IMS tag and receive “unverified error” in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: **User with IMS Age verification status = Active grace period AND Player tag** = AGP_Success_Upload **with digit<5 as a value AND Player tag** "Verification_Review" **is logged in**
    """
    keep_browser_open = True

    def test_001_in_right_user_menu_click_on_depositand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: In right user menu click on Deposit,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: - Account in Review with restriction message is shown
        EXPECTED: - trackPageview event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/account-review-error'
        EXPECTED: })
        """
        pass

    def test_002_tap_on_close_buttonand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on Close button,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: Closure Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'account review error',
        EXPECTED: 'eventLabel' : 'close'
        EXPECTED: })
        """
        pass

    def test_003_add_any_selection_to_betslip_enter_stake_and_hit_bet_now_buttonand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Add any selection to betslip, enter stake and hit 'Bet Now' button,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: - Account in Review with restriction message is shown
        EXPECTED: - trackPageview event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/account-review-error'
        EXPECTED: })
        """
        pass

    def test_004_close_overlay_and_add_any_selection_to_quick_bet_enter_stake_and_hit_bet_now_buttonand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Close overlay and add any selection to Quick bet, enter stake and hit 'Bet Now' button,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: - Closure Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'account review error',
        EXPECTED: 'eventLabel' : 'close'
        EXPECTED: })
        EXPECTED: - Account in Review with restriction message is shown
        EXPECTED: - trackPageview event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/account-review-error'
        EXPECTED: })
        """
        pass

    def test_005_close_the_overlay_and_click_on_withdraw_in_right_user_menuand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Close the overlay and click on 'Withdraw' in right user menu,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: - Closure Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'account review error',
        EXPECTED: 'eventLabel' : 'close'
        EXPECTED: })
        EXPECTED: - Account in Review with restriction message is shown
        EXPECTED: - trackPageview event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/account-review-error'
        EXPECTED: })
        """
        pass

    def test_006_close_the_overlay_and_withdraw_menu_and_click_on_my_freebets__bonuses_in_right_user_menuin_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Close the overlay and withdraw menu and click on 'My Freebets & Bonuses' in right user menu.
        DESCRIPTION: In Console type "dataLayer" and press Enter
        EXPECTED: - Closure Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'account review error',
        EXPECTED: 'eventLabel' : 'close'
        EXPECTED: })
        EXPECTED: - Account in Review with restriction message is shown
        EXPECTED: - trackPageview event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/account-review-error'
        EXPECTED: })
        """
        pass

    def test_007_add_any_selection_to_betslip_select_freebet_if_available_hit_bet_now_buttonin_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Add any selection to betslip, select Freebet (if available), hit 'Bet Now' button.
        DESCRIPTION: In Console type "dataLayer" and press Enter
        EXPECTED: - Closure Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'account review error',
        EXPECTED: 'eventLabel' : 'close'
        EXPECTED: })
        EXPECTED: - Account in Review with restriction message is shown
        EXPECTED: - trackPageview event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/account-review-error'
        EXPECTED: })
        """
        pass
