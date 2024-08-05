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
class Test_C44870204_Verify_that_the_german_User_has_no_horse_racing_OR_greyhound_betting_is_displayed__this_includesthe_folowing_locations_A_Z_links_Sports_carousel_links_respective_accordions_Horse_racing_and_greyhound_landing_page_Events_on_the_site_International(Common):
    """
    TR_ID: C44870204
    NAME: "Verify that the german User has no horse racing OR greyhound betting is displayed - this includes:the folowing locations  A-Z links Sports carousel links respective accordions Horse racing and greyhound landing page Events on the site International
    DESCRIPTION: "Verify that the german User has no horse racing OR greyhound betting is displayed - this includes:the folowing locations
    DESCRIPTION: A-Z links
    DESCRIPTION: Sports carousel links
    DESCRIPTION: respective accordions
    DESCRIPTION: Horse racing and greyhound landing page
    DESCRIPTION: Events on the site
    DESCRIPTION: International tote
    DESCRIPTION: Desktop widgets
    DESCRIPTION: When attempted ""standard page not found error (404 error)"" should be displayed."
    PRECONDITIONS: 1) User has German account and when logged in
    """
    keep_browser_open = True

    def test_001_log_in_to_the_app_as_german_user(self):
        """
        DESCRIPTION: Log in to the app as German user
        EXPECTED: German user is logged in
        """
        pass

    def test_002_verify_availability_of_horse_racing_greyhounds__international_tote_inmobilesports_menu_ribbondesktopheader_and_subheader_menus(self):
        """
        DESCRIPTION: Verify availability of 'Horse Racing', 'Greyhounds' & 'International Tote' in:
        DESCRIPTION: Mobile:
        DESCRIPTION: Sports Menu Ribbon
        DESCRIPTION: Desktop:
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

    def test_004_mobiletap_all_sports_a_z_menu_in_the_header_ribbonortap_menu_item_in_the_footerdesktopfind_a_z_sports_on_the_left_hand_side_of_the_homepage(self):
        """
        DESCRIPTION: Mobile:
        DESCRIPTION: Tap 'All Sports' (A-Z menu) in the header ribbon
        DESCRIPTION: OR
        DESCRIPTION: Tap 'Menu' item in the footer
        DESCRIPTION: Desktop:
        DESCRIPTION: Find 'A-Z Sports' on the left-hand side of the Homepage
        EXPECTED: Horse Racing', 'Greyhounds' & 'International Tote' are NOT available
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
        DESCRIPTION: Mobile/Tablet:
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon on the homepage
        DESCRIPTION: Desktop:
        DESCRIPTION: Click 'In-Play' icon on the Header Menus/SubHeader Menus
        EXPECTED: The page is opened
        EXPECTED: GH and HR are not shown
        EXPECTED: All other sports but racing are available
        """
        pass

    def test_007_mobiletabletopen_in_play_module_on_the_featured_tab(self):
        """
        DESCRIPTION: Mobile/Tablet:
        DESCRIPTION: Open 'In Play' module on the 'Featured' tab
        EXPECTED: The page is opened
        EXPECTED: GH and HR are not shown
        EXPECTED: All other sports but racing are available
        """
        pass

    def test_008_mobiletabletopen_in_play_tab_on_the_homepagedesktopfind_in_play_and_live_stream_tab_on_the_homepage(self):
        """
        DESCRIPTION: Mobile/Tablet:
        DESCRIPTION: Open 'In-Play' tab on the Homepage
        DESCRIPTION: Desktop:
        DESCRIPTION: Find 'In-play and live stream' tab on the Homepage.
        EXPECTED: The page is opened
        EXPECTED: GH and HR are not shown
        EXPECTED: 'View all in-play [racing]' button is not displayed
        EXPECTED: All other sports but racing are available
        """
        pass

    def test_009_mobiletabletfooter_menu__menu_item__tap_on_in_playdesktophomepage__a_z_sports_left_hand_menu__in_play(self):
        """
        DESCRIPTION: Mobile/Tablet:
        DESCRIPTION: Footer menu > 'Menu' item > Tap on ‘In Play’
        DESCRIPTION: Desktop:
        DESCRIPTION: Homepage > 'A-Z sports' left-hand menu > 'In-Play'
        EXPECTED: The page is opened
        EXPECTED: GH and HR are not shown
        EXPECTED: All other sports but racing are available
        """
        pass

    def test_010_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: German user is logged out
        """
        pass

    def test_011_repeat_steps_2_9(self):
        """
        DESCRIPTION: Repeat steps 2-9
        EXPECTED: 
        """
        pass
