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
class Test_C2987471_Verify_Favourites_enabling_in_the_CMS(Common):
    """
    TR_ID: C2987471
    NAME: Verify Favourites enabling in the CMS
    DESCRIPTION: This test case needs to be edited according to new changes - step 5 (on betslip, for mobile platform "Favourite All"
    PRECONDITIONS: Add a configuration to the CMS:
    PRECONDITIONS: 1. Login to the corresponding CMS
    PRECONDITIONS: 2. Select brand
    PRECONDITIONS: 3. Go to System Configuration -> Config
    PRECONDITIONS: 4. Create new group "Favourites"
    PRECONDITIONS: 5. Add properties "displayOnMobile", "displayOnTablet", "displayOnDesktop" with field type "checkbox"
    PRECONDITIONS: 6. Go to System Configuration -> Structure
    PRECONDITIONS: 7. Define properties in the Favourites group:
    PRECONDITIONS: displayOnMobile: true
    PRECONDITIONS: displayOnTablet: false
    PRECONDITIONS: displayOnDesktop: false
    PRECONDITIONS: **NOTE:** Favourites always should be turned off for Ladbrokes
    """
    keep_browser_open = True

    def test_001_open_the_football_landing_page_verify_the_icon_is_shown_in_the_mobile_versionverify_the_icon_isnt_shown_in_the_tablet_and_desktop_versions(self):
        """
        DESCRIPTION: Open the Football Landing page. Verify the icon is shown in the mobile version
        DESCRIPTION: Verify the icon isn't shown in the tablet and desktop versions
        EXPECTED: Icon is shown for mobile and not for other versions
        """
        pass

    def test_002_open_the_football__in_play_tab_verify_the_icon_is_shown_in_the_mobile_versionverify_the_icon_isnt_shown_in_the_tablet_and_desktop_versions(self):
        """
        DESCRIPTION: Open the Football > In-Play tab. Verify the icon is shown in the mobile version
        DESCRIPTION: Verify the icon isn't shown in the tablet and desktop versions
        EXPECTED: Icon is shown for mobile and not for other versions
        """
        pass

    def test_003_open_the_football__coupons__coupons_details_page_verify_the_icon_is_shown_in_the_mobile_versionverify_the_icon_isnt_shown_in_the_tablet_and_desktop_versions(self):
        """
        DESCRIPTION: Open the Football > Coupons > Coupons Details page. Verify the icon is shown in the mobile version
        DESCRIPTION: Verify the icon isn't shown in the tablet and desktop versions
        EXPECTED: Icon is shown for mobile and not for other versions
        """
        pass

    def test_004_open_the_football_match_edp_verify_the_icon_is_shown_in_the_mobile_versionverify_the_icon_isnt_shown_in_the_tablet_and_desktop_versions(self):
        """
        DESCRIPTION: Open the Football match EDP. Verify the icon is shown in the mobile version
        DESCRIPTION: Verify the icon isn't shown in the tablet and desktop versions
        EXPECTED: Icon is shown for mobile and not for other versions
        """
        pass

    def test_005_to_be_editedmake_a_bet_for_a_football_event_to_open_bet_receipt_verify_the_icons_are_shown_in_the_mobile_version_add_all_to_favorites_above_the_bets_favourite_icon_for_the_particular_betverify_the_icons_arent_shown_in_the_tablet_and_desktop_versions(self):
        """
        DESCRIPTION: [TO BE EDITED]Make a bet for a football event to open Bet Receipt. Verify the icons are shown in the mobile version:
        DESCRIPTION: * "Add all to favorites" above the bets
        DESCRIPTION: * Favourite icon for the particular bet
        DESCRIPTION: Verify the icons aren't shown in the tablet and desktop versions
        EXPECTED: Icons are shown for mobile and not for other versions
        """
        pass

    def test_006__mobile_version_set_displayonmobile_to_trueverify_favourites_icon_is_shown_on_the_football_headerverify_url_httpsenvurlfavourites_leads_to_the_favourite_matches_page(self):
        """
        DESCRIPTION: _Mobile version_
        DESCRIPTION: Set "displayOnMobile" to true.
        DESCRIPTION: Verify Favourites icon is shown on the Football Header.
        DESCRIPTION: Verify url https://envURL/favourites leads to the Favourite Matches page
        EXPECTED: * Favourites icon is shown on the Football Header
        EXPECTED: * Favourite Matches page is opened when follow the https://envURL/favourites link
        """
        pass

    def test_007__mobile_version_set_displayonmobile_to_falseverify_favourites_icon_isnt_shown_on_the_football_headerverify_url_httpsenvurlfavourites_leads_to_the_home_page(self):
        """
        DESCRIPTION: _Mobile version_
        DESCRIPTION: Set "displayOnMobile" to false.
        DESCRIPTION: Verify Favourites icon isn't shown on the Football Header.
        DESCRIPTION: Verify url https://envURL/favourites/ leads to the Home page
        EXPECTED: * Favourites icon isn't shown on the Football Header
        EXPECTED: * Home page is opened when follow the https://envURL/favourites/ link
        """
        pass

    def test_008_pass_the_steps_2_5_with_favourites_enabled_for_desktop_version_and_disabled_for_mobile_and_tablet_version_verify_icons_are_shown_for_desktop_and_arent_shown_for_mobile_and_tablet(self):
        """
        DESCRIPTION: Pass the steps 2-5 with favourites enabled for desktop version and disabled for mobile and tablet version. Verify icons are shown for desktop and aren't shown for mobile and tablet
        EXPECTED: Icons are shown for desktop and not for other versions
        """
        pass

    def test_009__desktop_version_set_displayontablet_to_trueverify_favourites_widget_is_shown(self):
        """
        DESCRIPTION: _Desktop version_
        DESCRIPTION: Set "displayOnTablet" to true.
        DESCRIPTION: Verify Favourites widget is shown
        EXPECTED: Favourites widget is shown
        """
        pass

    def test_010__desktop_version_set_displayontablet_to_falseverify_favourites_widget_isnt_shown(self):
        """
        DESCRIPTION: _Desktop version_
        DESCRIPTION: Set "displayOnTablet" to false.
        DESCRIPTION: Verify Favourites widget isn't shown
        EXPECTED: Favourites widget isn't shown
        """
        pass

    def test_011_pass_the_steps_2_5_with_favourites_enabled_for_tablet_version_and_disabled_for_mobile_and_desktop_version_verify_icons_are_shown_for_tablet_and_arent_shown_for_mobile_and_desktop(self):
        """
        DESCRIPTION: Pass the steps 2-5 with favourites enabled for tablet version and disabled for mobile and desktop version. Verify icons are shown for tablet and aren't shown for mobile and desktop
        EXPECTED: Icons are shown for tablet and not for other versions
        """
        pass

    def test_012__tablet_version_set_displayondesktop_to_trueverify_favourites_widget_is_shown(self):
        """
        DESCRIPTION: _Tablet version_
        DESCRIPTION: Set "displayOnDesktop" to true.
        DESCRIPTION: Verify Favourites widget is shown
        EXPECTED: Favourites widget is shwon
        """
        pass

    def test_013__tablet_version_set_displayondesktop_to_falseverify_favourites_widget_isnt_shown(self):
        """
        DESCRIPTION: _Tablet version_
        DESCRIPTION: Set "displayOnDesktop" to false.
        DESCRIPTION: Verify Favourites widget isn't shown
        EXPECTED: Favourites widget isn't shown
        """
        pass
