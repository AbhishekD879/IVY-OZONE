import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.lotto
@vtest
class Test_C9698959_Verify_availability_of_Lotto_pages_for_a_non_german_user(Common):
    """
    TR_ID: C9698959
    NAME: Verify availability of 'Lotto' pages for a non german user
    DESCRIPTION: This test case verifies displaying 'Lotto' in Sports Ribbon (mobile), A-Z page, Header & Sub Header (desktop) & having access to 'Lotto' page via url for a non German user
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: 1. Lotto is configured in CMS for:
    PRECONDITIONS: - Sport Pages > Sport Categories > Lotto > General Sport Configuration: "Show in Sports Ribbon", "Show in AZ", "Is Top Sport" are checked; "Target URi": "/lotto"
    PRECONDITIONS: - Menus > Header Menus > Lotto: "Target URi:" "/lotto" (Control by GVC)
    PRECONDITIONS: - Header SubMenus > Lotto: "Target URi:" "/lotto"
    PRECONDITIONS: - A German user is registered (with "signupCountryCode": "DE" - select Germany as a country during registration)
    PRECONDITIONS: - Local storage is cleared (so no "OX.countryCode" is available)
    PRECONDITIONS: 2. A German user is registered (with "signupCountryCode: "DE" - select Germany as a country during registration)
    PRECONDITIONS: 3. A non-german user is registered
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

    def test_003_mobile__tabletverify_availability_of_lotto_in_sports_menu_ribbon(self):
        """
        DESCRIPTION: **Mobile & Tablet:**
        DESCRIPTION: Verify availability of 'Lotto' in 'Sports Menu Ribbon'
        EXPECTED: 'Lotto' is available is 'Sports Menu Ribbon'
        """
        pass

    def test_004_mobile__tablet__navigate_to_all_sports_page__verify_availability_of_lotto_item_in_top_sports__a_z_sports_sectionsdesktopverify_availability_of_lotto_item_in_a_z_sports_menu(self):
        """
        DESCRIPTION: **Mobile & Tablet:**
        DESCRIPTION: - Navigate to 'All Sports' page
        DESCRIPTION: - Verify availability of 'Lotto' item in 'Top Sports' & 'A-Z Sports' sections
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Verify availability of 'Lotto' item in 'A-Z Sports' menu
        EXPECTED: **Mobile & Tablet:**
        EXPECTED: 'Lotto' is available in 'Top Sports' & 'A-Z Sports' sections
        EXPECTED: **Desktop:**
        EXPECTED: 'Lotto' is available in 'A-Z Sports' menu
        """
        pass

    def test_005_desktopverify_availability_of_lotto_in_header_menu_if_available__sub_header_menu(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Verify availability of 'Lotto' in 'Header' menu (if available) & 'Sub header' menu
        EXPECTED: 'Lotto' is available in 'Header' menu (if available) & 'Sub header' menu
        """
        pass

    def test_006_navigate_to_lotto_page(self):
        """
        DESCRIPTION: Navigate to 'Lotto' page
        EXPECTED: 'Lotto' page is opened
        """
        pass

    def test_007_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: - Non german user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        pass

    def test_008_repeat_steps_3_6(self):
        """
        DESCRIPTION: Repeat steps 3-6
        EXPECTED: 
        """
        pass
