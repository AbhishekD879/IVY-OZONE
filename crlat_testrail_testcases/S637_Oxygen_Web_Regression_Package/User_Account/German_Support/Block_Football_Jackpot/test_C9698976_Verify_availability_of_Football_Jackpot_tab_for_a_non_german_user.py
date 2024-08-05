import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C9698976_Verify_availability_of_Football_Jackpot_tab_for_a_non_german_user(Common):
    """
    TR_ID: C9698976
    NAME: Verify availability of 'Football Jackpot' tab for a non german user
    DESCRIPTION: This test case verifies displaying 'Football Jackpot' tab & having access to 'Football Jackpot' page via url for a non German user
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: 1. A German user is registered (with "signupCountryCode: "DE" - select Germany as a country during registration)
    PRECONDITIONS: 2. A non-german user is registered
    """
    keep_browser_open = True

    def test_001_log_in_as_a_german_user__log_out(self):
        """
        DESCRIPTION: Log in as a german user > Log out
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        pass

    def test_002_log_in_as_a_non_german_user(self):
        """
        DESCRIPTION: Log in as a non german user
        EXPECTED: - Non german user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        pass

    def test_003___navigate_to_football_landing_page__verify_availability_of_jackpot_tab(self):
        """
        DESCRIPTION: - Navigate to Football landing page
        DESCRIPTION: - Verify availability of 'Jackpot' tab
        EXPECTED: - Football landing page is opened
        EXPECTED: - 'Jackpot' tab is available
        """
        pass

    def test_004_tap_on_football_jackpot_tab(self):
        """
        DESCRIPTION: Tap on 'Football Jackpot' tab
        EXPECTED: 'Football Jackpot' is opened
        """
        pass

    def test_005_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: - Non german user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        pass

    def test_006_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass
