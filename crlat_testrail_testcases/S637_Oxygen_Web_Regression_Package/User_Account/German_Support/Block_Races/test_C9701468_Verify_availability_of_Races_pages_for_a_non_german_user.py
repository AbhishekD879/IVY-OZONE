import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C9701468_Verify_availability_of_Races_pages_for_a_non_german_user(Common):
    """
    TR_ID: C9701468
    NAME: Verify availability of <Races> pages for a non-german user
    DESCRIPTION: This test case verifies displaying 'Races' in Sports Ribbon (mobile), A-Z page, Header & Sub Header (desktop) & having access to 'Races' pages via url for a non German user
    DESCRIPTION: NOTE:
    DESCRIPTION: countryCode: "DE" attribute could be found in Application -> Local Storage -> OX.USER (this attribute countryCode: "DE" is cleared after Log Out)
    PRECONDITIONS: 1. Horse Racing/Greyhounds/International Totes is configured in CMS for:
    PRECONDITIONS: - Sport Pages > Sport Categories > Lotto > General Sport Configuration:  "Show in Sports Ribbon", "Show in AZ", "Is Top Sport" are checked; "Target URi": "/horse-racing", "/greyhound-racing", "/tote"
    PRECONDITIONS: - Menus > Header Menus > Horse Racing/Greyhounds/International Totes: "Target URi:" "/horse-racing", "/greyhound-racing", "/tote"
    PRECONDITIONS: - Header SubMenus > Horse Racing/Greyhounds/International Totes: "Target URi:" "/horse-racing", "/greyhound-racing", "/tote"
    PRECONDITIONS: 2. Ensure that there are GH, International Totes, and HR Featured with different 'Select Events by' drop-down items available:
    PRECONDITIONS: * EventsModule  (CMS > Featured Tab Modules > Active Featured Modules)
    PRECONDITIONS: * SurfaceBetModule (CMS > Main Navigation > Homepage > Surface Bet Module > Active Surface Bets)
    PRECONDITIONS: 3. A German user is registered (with "signupCountryCode: "DE" - select Germany as a country during registration)
    PRECONDITIONS: 4. A non-german user is registered
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - "signupCountryCode" is received in WS "openapi" response from IMS
    PRECONDITIONS: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    PRECONDITIONS: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
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

    def test_003_verify_availability_of_next_races_tab_on_home_page(self):
        """
        DESCRIPTION: Verify availability of 'Next Races' tab on Home page
        EXPECTED: 'Next Races' tab is available
        """
        pass

    def test_004_verify_availability_of_hr__gh_in_the_featured_module_on_homepage(self):
        """
        DESCRIPTION: Verify availability of HR & GH in the Featured module on Homepage
        EXPECTED: HR & GH are available in the Featured module
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
        EXPECTED: * GH and HR are available
        """
        pass

    def test_006_mobiletabletopen_in_play_module_on_the_featured_tabdesktopclick_upcoming_tab_in_in_play_module(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Open 'In Play' module on the 'Featured' tab
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Click 'Upcoming' tab in 'In-Play' module
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are available
        """
        pass

    def test_007_mobiletabletopen_in_play_tab_on_the_homepagedesktopfind_in_play_and_live_stream_tab_on_the_homepage(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Open 'In-Play' tab on the Homepage
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Find 'In-play and live stream' tab on the Homepage
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are available
        EXPECTED: * 'SHOW ALL HORSE RACING (X)' link is displayed
        """
        pass

    def test_008_mobiletabletfooter_menu__menu_item__tap_on_in_playdesktophomepage__a_z_sports_left_hand_menu__in_play(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Footer menu > 'Menu' item > Tap on ‘In Play’
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Homepage > 'A-Z sports' left-hand menu > 'In-Play'
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are available
        """
        pass

    def test_009_tap_on_next_races_tab_on_home_page(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab on Home page
        EXPECTED: 'Next Races' tab is opened
        """
        pass

    def test_010_verify_availability_of_horse_racing_greyhounds__international_tote_inmobilesports_menu_ribbondesktopheader_and_subheader_menus(self):
        """
        DESCRIPTION: Verify availability of 'Horse Racing', 'Greyhounds' & 'International Tote' in:
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Sports Menu Ribbon
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Header and subheader menus
        EXPECTED: 'Horse Racing', 'Greyhounds' & 'International Tote' are available
        """
        pass

    def test_011_navigate_to_horse_racing_pages_eg_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' pages e.g. landing page
        EXPECTED: 'Horse Racing' pages are opened
        """
        pass

    def test_012_navigate_to_greyhounds_pages_eg_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Greyhounds' pages e.g. landing page
        EXPECTED: 'Greyhounds' pages are opened
        """
        pass

    def test_013_navigate_to_international_totes_page(self):
        """
        DESCRIPTION: Navigate to 'International Totes' page
        EXPECTED: 'International Totes' page is opened
        """
        pass

    def test_014_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: - Non german user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        pass

    def test_015_repeat_steps_3_13(self):
        """
        DESCRIPTION: Repeat steps 3-13
        EXPECTED: 
        """
        pass
