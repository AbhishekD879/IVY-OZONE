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
class Test_C9489629_Verify_blocking_of_access_to_GH_HR_pages_events_for_German_accounts_logged_in_out_user(Common):
    """
    TR_ID: C9489629
    NAME: Verify blocking of access to GH & HR pages/events for German accounts (logged-in/out user)
    DESCRIPTION: This test case verifies whether the German user doesn't have access to Greyhound (GH) and Horse Racing (HR) nevertheless he is a logged-in or logged-out user
    DESCRIPTION: AUTOTEST MOBILE : [C17261983]
    DESCRIPTION: AUTOTEST DESKTOP: [C17728073]
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: 1. Horse Racing/Greyhounds/International Totes is configured in CMS for:
    PRECONDITIONS: - Sport Pages > Sport Categories > Lotto > General Sport Configuration:  "Show in Sports Ribbon", "Show in AZ", "Is Top Sport" are checked; "Target URi": "/horse-racing", "/greyhound-racing", "/tote"
    PRECONDITIONS: - Menus > Header Menus > Horse Racing/Greyhounds/International Totes: "Target URi:" "/horse-racing", "/greyhound-racing", "/tote" (Control by GVC)
    PRECONDITIONS: - Header SubMenus > Horse Racing/Greyhounds/International Totes: "Target URi:" "/horse-racing", "/greyhound-racing", "/tote"
    PRECONDITIONS: 2. Ensure that there are GH, International Totes, and HR Featured with different 'Select Events by' drop-down items available for not German user:
    PRECONDITIONS: * EventsModule  (CMS > Featured Tab Modules > Active Featured Modules)
    PRECONDITIONS: * SurfaceBetModule (CMS > Main Navigation > Homepage > Surface Bet Module > Active Surface Bets)
    PRECONDITIONS: 3. devtool > Application tab > Local Storage > is cleared (so no "OX.countryCode" is available)
    PRECONDITIONS: 4. Login pop-up is opened on mobile
    """
    keep_browser_open = True

    def test_001_log_in_to_the_app_as_german_user(self):
        """
        DESCRIPTION: Log in to the app as German user
        EXPECTED: - German user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
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

    def test_004_mobiletap_all_sports__a_z_menu_in_the_header_ribbonortap_menu_item_in_the_footerdesktopfind_a_z_sports_on_the_left_hand_side_of_the_homepage(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Tap 'All Sports'  (A-Z menu) in the header ribbon
        DESCRIPTION: OR
        DESCRIPTION: Tap 'Menu' item in the footer
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Find 'A-Z Sports' on the left-hand side of the Homepage
        EXPECTED: 'Horse Racing', 'Greyhounds' & 'International Tote' are NOT available
        """
        pass

    def test_005_verify_availability_horse_racing_greyhounds__international_tote_on_featured_tab_on_home_page(self):
        """
        DESCRIPTION: Verify availability 'Horse Racing', 'Greyhounds' & 'International Tote' on 'Featured' tab on Home page
        EXPECTED: 'Horse Racing', 'Greyhounds'& 'International Tote' are NOT available
        """
        pass

    def test_006_open_in_play_pagemobiletablettap_in_play_icon_on_the_sports_menu_ribbon_on_the_homepagedesktopclick_in_play_icon_on_the_header_menussubheader_menus(self):
        """
        DESCRIPTION: Open 'In-Play' Page:
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon on the homepage
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Click 'In-Play' icon on the Header Menus/SubHeader Menus
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports except racing are available
        """
        pass

    def test_007_mobiletabletopen_in_play_module_on_the_featured_tab(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Open 'In Play' module on the 'Featured' tab
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports except racing are available
        """
        pass

    def test_008_mobiletabletopen_in_play_tab_on_the_homepagedesktopfind_in_play_and_live_stream_tab_on_the_homepage(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Open 'In-Play' tab on the Homepage
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Find 'In-play and live stream' tab on the Homepage.
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * 'View all in-play [racing]' button is not displayed
        EXPECTED: * All other sports except racing are available
        """
        pass

    def test_009_mobiletabletfooter_menu__menu_item__tap_on_in_playdesktophomepage__a_z_sports_left_hand_menu__in_play(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Footer menu > 'Menu' item > Tap on ‘In Play’
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Homepage > 'A-Z sports' left-hand menu > 'In-Play'
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports except racing are available
        """
        pass

    def test_010___add_horse_racing_route_to_the_url__press_enter(self):
        """
        DESCRIPTION: - Add "/horse-racing" route to the url
        DESCRIPTION: - Press 'Enter'
        EXPECTED: * Homepage is opened
        EXPECTED: * The standard error popup is displayed with:
        EXPECTED: Header: 'Country Restriction'
        EXPECTED: Text: 'We are unable to offer Horse Racing or Greyhound betting in your jurisdiction.'
        """
        pass

    def test_011___add_greyhound_racing_route_to_the_url__press_enter(self):
        """
        DESCRIPTION: - Add "/greyhound-racing" route to the url
        DESCRIPTION: - Press 'Enter'
        EXPECTED: * Homepage is opened
        EXPECTED: * The standard error popup is displayed with:
        EXPECTED: Header: 'Country Restriction'
        EXPECTED: Text: 'We are unable to offer Horse Racing or Greyhound betting in your jurisdiction.'
        """
        pass

    def test_012___add_tote_route_to_the_url__press_enter(self):
        """
        DESCRIPTION: - Add "tote" route to the url
        DESCRIPTION: - Press 'Enter'
        EXPECTED: * Homepage is opened
        EXPECTED: * The standard error popup is displayed with:
        EXPECTED: Header: 'Country Restriction'
        EXPECTED: Text: 'We are unable to offer Horse Racing or Greyhound betting in your jurisdiction.'
        """
        pass

    def test_013___add_homenext_races__press_enter(self):
        """
        DESCRIPTION: - Add "home/next-races"
        DESCRIPTION: - Press 'Enter'
        EXPECTED: * Homepage is opened
        EXPECTED: * The standard error popup is displayed with:
        EXPECTED: Header: 'Country Restriction'
        EXPECTED: Text: 'We are unable to offer Horse Racing or Greyhound betting in your jurisdiction.'
        """
        pass

    def test_014_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        pass

    def test_015_repeat_steps_2_8(self):
        """
        DESCRIPTION: Repeat steps 2-8
        EXPECTED: 
        """
        pass
