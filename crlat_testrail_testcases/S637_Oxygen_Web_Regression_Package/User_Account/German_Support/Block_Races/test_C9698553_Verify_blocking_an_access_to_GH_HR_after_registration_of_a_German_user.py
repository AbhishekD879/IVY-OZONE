import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C9698553_Verify_blocking_an_access_to_GH_HR_after_registration_of_a_German_user(Common):
    """
    TR_ID: C9698553
    NAME: Verify blocking an access to GH & HR after registration of a German user
    DESCRIPTION: This test case verifies whether just registered German user doesn't have access to Greyhound (GH) and Horse Racing (HR)
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: 1. Horse Racing/Greyhounds/International Totes is configured in CMS for:
    PRECONDITIONS: - Sport Pages > Sport Categories > Horse Racing/Greyhounds/International Totes: > General Sport Configuration:  "Show in Sports Ribbon", "Show in AZ", "Is Top Sport" are checked; "Target URi": "/horse-racing", "/greyhound-racing", "/tote"
    PRECONDITIONS: - Menus > Header Menus > Horse Racing/Greyhounds/International Totes: "Target URi:" "/horse-racing", "/greyhound-racing", "/tote"
    PRECONDITIONS: - Header SubMenus > Horse Racing/Greyhounds/International Totes: "Target URi:" "/horse-racing", "/greyhound-racing", "/tote"
    PRECONDITIONS: 2. Ensure that there are GH, International Totes, and HR Featured with different 'Select Events by' drop-down items available:
    PRECONDITIONS: * EventsModule  (CMS > Featured Tab Modules > Active Featured Modules)
    PRECONDITIONS: * SurfaceBetModule (CMS > Main Navigation > Homepage > Surface Bet Module > Active Surface Bets)
    PRECONDITIONS: 3. Featured with categoryId in (19, 21, 161) are not displayed for german users (Console > Network > WS > find '?EIO=3&transport=websoket' > Frames > 42/0,["FEATURED_STRUCTURE_CHANGED",…]
    PRECONDITIONS: 4. devtool > Application tab > Local Storage >  is cleared (so no "OX.countryCode" is available)
    PRECONDITIONS: 5. Login pop-up is opened on mobile
    """
    keep_browser_open = True

    def test_001__tap_join_now_fill_in_all_necessary_fields_to_register_user_select_country_germany_tap_open_account_save_my_preferences_close_deposit_page(self):
        """
        DESCRIPTION: * Tap 'Join now'
        DESCRIPTION: * Fill in all necessary fields to register user
        DESCRIPTION: * **Select Country 'Germany'**
        DESCRIPTION: * Tap 'Open account', 'Save my preferences'
        DESCRIPTION: * Close Deposit page
        EXPECTED: * German user is navigated back to an app
        EXPECTED: * German user is logged in with registered credentials
        EXPECTED: * German user is navigated to Home page
        """
        pass

    def test_002_verify_availability_of_horse_racing_greyhounds__international_tote_inmobilesports_menu_ribbondesktopheader_and_subheader_menus(self):
        """
        DESCRIPTION: Verify availability of 'Horse Racing', 'Greyhounds' & 'International Tote' in:
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Sports Menu Ribbon
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Header and subheader menus
        EXPECTED: 'Horse Racing', 'Greyhounds' & 'International Tote' are NOT available
        """
        pass

    def test_003_verify_availability_of_next_races_tab_on_home_page(self):
        """
        DESCRIPTION: Verify availability of 'Next Races' tab on Home page
        EXPECTED: 'Next Races' tab is NOT available
        """
        pass

    def test_004_verify_availability_of_ghhr_in_featured_tab_on_home_page(self):
        """
        DESCRIPTION: Verify availability of GH/HR in Featured tab on Home page
        EXPECTED: GH/HR is NOT available in Featured tab
        """
        pass

    def test_005_open_in_play_pagemobiletablettap_in_play_icon_on_the_sports_menu_ribbon_on_the_homepagedesktopclick_in_play_icon_on_the_header_menussubheader_menus(self):
        """
        DESCRIPTION: Open 'In-Play' Page:
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon on the homepage
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Click 'In-Play' icon on the Header Menus/SubHeader Menus
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports but racing are available
        """
        pass

    def test_006_mobiletabletopen_in_play_module_on_the_featured_tabdesktopclick_upcoming_tab_in_in_play_module(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Open 'In Play' module on the 'Featured' tab
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Click 'Upcoming' tab in 'In-Play' module
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports but racing are available
        """
        pass

    def test_007_mobiletabletopen_in_play_tab_on_the_homepagedesktopfind_in_play_and_live_stream_tab_on_the_homepage(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Open 'In-Play' tab on the Homepage
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Find 'In-play and live stream' tab on the Homepage.
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * 'View all in-play [racing]' button is not displayed
        EXPECTED: * All other sports but racing are available
        """
        pass

    def test_008_mobiletabletfooter_menu__menu_item__tap_on_in_playdesktophomepage__a_z_sports_left_hand_menu__in_play(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Footer menu > 'Menu' item > Tap on ‘In Play’
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Homepage > 'A-Z sports' left-hand menu > 'In-Play'
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports but racing are available
        """
        pass
