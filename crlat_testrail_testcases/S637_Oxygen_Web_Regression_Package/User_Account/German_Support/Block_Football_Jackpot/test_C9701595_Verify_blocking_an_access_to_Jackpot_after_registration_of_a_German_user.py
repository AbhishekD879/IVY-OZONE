import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C9701595_Verify_blocking_an_access_to_Jackpot_after_registration_of_a_German_user(Common):
    """
    TR_ID: C9701595
    NAME: Verify blocking an access to Jackpot after registration of a German user
    DESCRIPTION: This test case verifies whether just registered German user doesn't have access to Football Jackpot
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: 1. devtool > Application tab > Local Storage > is cleared (so no "OX.countryCode" is available)
    PRECONDITIONS: 2. Login pop-up is opened on mobile
    """
    keep_browser_open = True

    def test_001___tap_join_now__fill_in_all_necessary_fields_to_register_user__select_country_germany__tap_open_account_save_my_preferences__close_deposit_page(self):
        """
        DESCRIPTION: - Tap 'Join now'
        DESCRIPTION: - Fill in all necessary fields to register user
        DESCRIPTION: - Select Country 'Germany'
        DESCRIPTION: - Tap 'Open account', 'Save my preferences'
        DESCRIPTION: - Close Deposit page
        EXPECTED: - German user is navigated back to an app
        EXPECTED: - German user is logged in
        EXPECTED: - German user is navigated to Home page
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        pass

    def test_002___go_to_football_landing_page__verify_availability_of_jackpot_tab(self):
        """
        DESCRIPTION: - Go to Football landing page
        DESCRIPTION: - Verify availability of 'Jackpot' tab
        EXPECTED: 'Jackpot' tab is NOT available
        """
        pass
