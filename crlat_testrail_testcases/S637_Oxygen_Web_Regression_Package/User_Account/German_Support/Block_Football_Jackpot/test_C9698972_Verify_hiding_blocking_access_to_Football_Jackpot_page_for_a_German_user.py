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
class Test_C9698972_Verify_hiding_blocking_access_to_Football_Jackpot_page_for_a_German_user(Common):
    """
    TR_ID: C9698972
    NAME: Verify hiding & blocking access to 'Football Jackpot' page for a German user
    DESCRIPTION: This test case verifies not displaying 'Jackpot' tab on 'Football' landing page & blocking access to 'Jackpot' tab via url for a German user.
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    DESCRIPTION: AUTOTEST
    DESCRIPTION: Mobile [C17489457]
    DESCRIPTION: Desktop [C17505272]
    PRECONDITIONS: 1. Football Jackpot is available
    PRECONDITIONS: 2. A German user is registered (with "signupCountryCode": "DE" - select Germany as a country during registration)
    PRECONDITIONS: 3. Local storage is cleared (so no "OX.countryCode" is available)
    PRECONDITIONS: 4. A user is not logged in
    """
    keep_browser_open = True

    def test_001_log_in_as_a_german_user(self):
        """
        DESCRIPTION: Log in as a German user
        EXPECTED: - German user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        pass

    def test_002___navigate_to_football_landing_page__verify_availability_of_jackpot_tab(self):
        """
        DESCRIPTION: - Navigate to Football landing page
        DESCRIPTION: - Verify availability of 'Jackpot' tab
        EXPECTED: - Football landing page is opened
        EXPECTED: - 'Jackpot' tab is not available
        """
        pass

    def test_003___add_sportfootballjackpot_route_to_an_app_url__press_enter(self):
        """
        DESCRIPTION: - Add "/sport/football/jackpot" route to an app url
        DESCRIPTION: - Press 'Enter'
        EXPECTED: - German user is navigated to home page
        EXPECTED: - ‘Country Restriction’ pop up appears with text: "We are unable to offer Football Jackpot betting in your jurisdiction." and 'OK' button
        """
        pass

    def test_004_tap_ok_buttonanywhere_outside_the_pop_up(self):
        """
        DESCRIPTION: Tap 'OK' button/anywhere outside the pop up
        EXPECTED: Pop up is closed
        """
        pass

    def test_005_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        pass

    def test_006_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps 2-4
        EXPECTED: 
        """
        pass
