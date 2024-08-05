import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.lotto
@vtest
class Test_C9698649_Verify_hiding_blocking_access_to_Lotto_page_for_a_German_user(Common):
    """
    TR_ID: C9698649
    NAME: Verify hiding & blocking access to 'Lotto' page for a German user
    DESCRIPTION: This test case verifies not displaying 'Lotto' in Sports Ribbon (mobile), A-Z page, Header & Sub Header (desktop) & blocking access to 'Lotto' page via url for a German user
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS (Roxanne only)
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: Lotto is configured in CMS for:
    PRECONDITIONS: - Sport Pages > Sport Categories > Lotto > General Sport Configuration: "Show in Sports Ribbon", "Show in AZ", "Is Top Sport" are checked; "Target URi": "/lotto"
    PRECONDITIONS: - Menus > Header Menus > Lotto: "Target URi:" "/lotto"
    PRECONDITIONS: - Header SubMenus > Lotto: "Target URi:" "/lotto"
    PRECONDITIONS: - A German user is registered (with "signupCountryCode": "DE" - select Germany as a country during registration)
    PRECONDITIONS: - Local storage is cleared (so no "OX.countryCode" is available)
    PRECONDITIONS: - A user is not logged in
    """
    keep_browser_open = True

    def test_001_log_in_as_a_german_user(self):
        """
        DESCRIPTION: Log in as a German user
        EXPECTED: - German user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        pass

    def test_002_mobile__tabletverify_availability_of_lotto_in_sports_menu_ribbon(self):
        """
        DESCRIPTION: **Mobile & Tablet**
        DESCRIPTION: Verify availability of 'Lotto' in 'Sports Menu Ribbon'
        EXPECTED: 'Lotto' is not available is 'Sports Menu Ribbon'
        """
        pass

    def test_003_mobile__tablet__navigate_to_all_sports_page__verify_availability_of_lotto_item_in_top_sports__a_z_sports_sectionsdesktopverify_availability_of_lotto_item_in_a_z_sports_menu(self):
        """
        DESCRIPTION: **Mobile & Tablet**
        DESCRIPTION: - Navigate to 'All Sports' page
        DESCRIPTION: - Verify availability of 'Lotto' item in 'Top Sports' & 'A-Z Sports' sections
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Verify availability of 'Lotto' item in 'A-Z Sports' menu
        EXPECTED: **Mobile & Tablet**
        EXPECTED: 'Lotto' is not available in 'Top Sports' & 'A-Z Sports' sections
        EXPECTED: **Desktop:**
        EXPECTED: 'Lotto' is not available in 'A-Z Sports' menu
        """
        pass

    def test_004_desktopverify_availability_of_lotto_in_header_menu_if_available__sub_header_menu(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Verify availability of 'Lotto' in 'Header' menu (if available) & 'Sub header' menu
        EXPECTED: 'Lotto' is not available in 'Header' menu (if available) & 'Sub header' menu
        """
        pass

    def test_005___add_lotto_route_to_an_app_url__press_enter(self):
        """
        DESCRIPTION: - Add "/lotto" route to an app url
        DESCRIPTION: - Press 'Enter'
        EXPECTED: - German user is navigated to home page
        EXPECTED: - ‘Country Restriction’ pop up appears with text: "We are unable to offer Lotto betting in your jurisdiction." and 'OK' button
        """
        pass

    def test_006_tap_ok_buttonanywhere_outside_the_pop_up(self):
        """
        DESCRIPTION: Tap 'OK' button/anywhere outside the pop up
        EXPECTED: Pop up is closed
        """
        pass

    def test_007_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        pass

    def test_008_repeat_steps_2_6(self):
        """
        DESCRIPTION: Repeat steps 2-6
        EXPECTED: 
        """
        pass
