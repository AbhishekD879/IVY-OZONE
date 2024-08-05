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
class Test_C9701594_Verify_blocking_an_access_to_Lotto_after_registration_of_a_German_user(Common):
    """
    TR_ID: C9701594
    NAME: Verify blocking an access to Lotto after registration of a German user
    DESCRIPTION: This test case verifies whether just registered German user doesn't have access to Lotto
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS (for Roxanne only, not valid for OX102 Ladbrokes Wallet)
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: 1. Lotto is configured in CMS for:
    PRECONDITIONS: - Sport Pages > Sport Categories > Lotto > General Sport Configuration: "Show in Sports Ribbon", "Show in AZ", "Is Top Sport" are checked; "Target URi": "/lotto"
    PRECONDITIONS: - Menus > Header Menus > Lotto: "Target URi:" "/lotto"
    PRECONDITIONS: - Header SubMenus > Lotto: "Target URi:" "/lotto"
    PRECONDITIONS: 2. devtool > Application tab > Local Storage > is cleared (so "countryCode" = 'null' is available in Application -> Local Storage -> OX.USER)
    PRECONDITIONS: 3. Login pop-up is opened on mobile
    """
    keep_browser_open = True

    def test_001___tap_join__fill_in_all_necessary_fields_to_register_user__select_country_germany__tap_open_account_save_my_preferences__close_deposit_page(self):
        """
        DESCRIPTION: - Tap 'Join'
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

    def test_002_mobile__tabletverify_availability_of_lotto_in_sports_menu_ribbon(self):
        """
        DESCRIPTION: **Mobile & Tablet:**
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
