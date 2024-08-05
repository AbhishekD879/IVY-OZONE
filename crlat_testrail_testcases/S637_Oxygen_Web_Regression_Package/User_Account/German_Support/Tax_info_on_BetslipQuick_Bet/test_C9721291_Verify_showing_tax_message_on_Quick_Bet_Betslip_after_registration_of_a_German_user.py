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
class Test_C9721291_Verify_showing_tax_message_on_Quick_Bet_Betslip_after_registration_of_a_German_user(Common):
    """
    TR_ID: C9721291
    NAME: Verify showing tax message on Quick Bet/Betslip after registration of a German user
    DESCRIPTION: This test case verifies displaying of a tax message on 'Betslip' for a German user after registration
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: 1. devtool > Application tab > Local Storage > is cleared (so no "OX.countryCode" is available)
    PRECONDITIONS: 2. Login pop-up is opened on mobile
    """
    keep_browser_open = True

    def test_001_tap_join_now(self):
        """
        DESCRIPTION: Tap 'Join now'
        EXPECTED: User is redirected to Account One
        """
        pass

    def test_002_in_account_one__fill_in_all_necessary_fields_to_register_user__select_country_germany__tap_open_account_save_my_preferences__add_credit_cards_on_deposit_page__deposit_money_to_added_credit_card__close_deposit_page(self):
        """
        DESCRIPTION: In Account One:
        DESCRIPTION: - Fill in all necessary fields to register user
        DESCRIPTION: - Select Country 'Germany'
        DESCRIPTION: - Tap 'Open account', 'Save my preferences'
        DESCRIPTION: - Add credit cards on Deposit page
        DESCRIPTION: - Deposit money to added credit card
        DESCRIPTION: - Close Deposit page
        EXPECTED: - German user is navigated back to an app
        EXPECTED: - German user is logged in
        EXPECTED: - German user is navigated to Home page
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        pass

    def test_003_mobileadd_any_selection_to_quick_bet(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Add any selection to 'Quick Bet'
        EXPECTED: - 'Quick Bet' appears with an added selection
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        pass

    def test_004_mobileenter_valid_stake_amount__tap_bet_now(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Enter valid Stake amount > Tap 'Bet Now'
        EXPECTED: - Bet is successfully placed
        EXPECTED: - Bet Receipt is displayed on 'Quick Bet'
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        pass

    def test_005___add_selections_to_betslip__open_betslip(self):
        """
        DESCRIPTION: - Add selection(s) to 'Betslip'
        DESCRIPTION: - Open 'Betslip'
        EXPECTED: - Added selection(s) is(are) available in the 'Betslip'
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        pass

    def test_006_enter_valid_stake_amount__tap_bet_now(self):
        """
        DESCRIPTION: Enter valid Stake amount > Tap 'Bet Now'
        EXPECTED: - Bet is successfully placed
        EXPECTED: - Bet Receipt is displayed on 'Betslip'
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        pass
