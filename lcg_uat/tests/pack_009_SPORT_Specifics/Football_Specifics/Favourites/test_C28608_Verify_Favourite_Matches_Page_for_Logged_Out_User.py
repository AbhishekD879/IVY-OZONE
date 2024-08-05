import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
@pytest.mark.low
@pytest.mark.slow
@pytest.mark.football
@pytest.mark.back_button
@pytest.mark.favourites
@pytest.mark.sports
@pytest.mark.login
@vtest
class Test_C28608_Verify_Favourite_Matches_Page_for_Logged_Out_User(BaseSportTest):
    """
    TR_ID: C28608
    VOL_ID: C9697791
    NAME: Verify 'Favourite Matches' icon for Logged out user
    """
    sport_name = 'Football'
    keep_browser_open = True

    def verify_page_title(self):
        page_title = self.site.favourites.header_line.page_title.title
        self.assertEqual(
            page_title,
            vec.sb.FAVOURITE_MATCHES,
            msg='Page title "%s" doesn\'t match expected text "%s"'
                % (page_title, vec.sb.FAVOURITE_MATCHES)
        )

    def test_000_tap_football(self):
        """
        DESCRIPTION: Tap "FOOTBALL" icon from Sports Menu Ribbon, 'Football' landing page is opened
        """
        self.site.open_sport(name=self.sport_name)

    def test_001_tap_tab_name(self, tab_name=None):
        """
        DESCRIPTION: Tap 'In Play' in Events Filter Ribbon Menu
        """
        if not tab_name:
            tab_name = self.get_sport_tab_name(
                self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play, self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(tab_name)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, tab_name,
                         msg=f'"{tab_name}" tab is not active, active is "{active_tab}"')

    def test_002_tap_favourite_page_icon(self):
        """
        DESCRIPTION: Tap on the 'Favourite Matches' page icon:
        EXPECTED: - Oxygen app loads the ‘Favourite Matches’ page
        EXPECTED: - ‘Favourite Matches’ page contains a ‘Log In’ button
        EXPECTED: - ‘Favourite Matches’ page containis 'Back' button '<'
        """
        self.site.football.header_line.go_to_favourites_page.click()
        self.site.wait_content_state(state_name='Favourites')
        self.verify_page_title()
        login_button = self.site.favourites.login_button
        self.assertTrue(login_button is not None, "‘Log In’ button was not found")
        has_please_login_text = self.site.favourites.please_login_text
        self.assertTrue(has_please_login_text, msg="\"To view and add matches into your favourites, "
                                                   "please log in to your account. \" text was not found")

    def test_003_tap_back(self):
        """
        DESCRIPTION: Tap on the back button and verify user is redirect to the previous page
        """
        self.site.favourites.header_line.back_button.click()
        self.site.wait_content_state_changed()

    def test_004_tap_favourite_icon_again(self):
        """
        DESCRIPTION: Tap on the 'Favourite Matches' page icon again and verify 'Favourite Matches' page is opened
        """
        self.site.football.header_line.go_to_favourites_page.click()
        self.site.wait_content_state(state_name='Favourites')
        self.verify_page_title()

    def test_005_tap_login(self):
        """
        DESCRIPTION: - Enter user credentials and press 'Log In'
        EXPECTED: - Favourite Matches page is opened
        EXPECTED: - 'Go To Maches' button is present
        EXPECTED: - 'Go To Tab Matches button is present
        """
        self.site.favourites.login_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg='\'Login dialog is not present on page\'')
        dialog.username = tests.settings.betplacement_user
        dialog.password = tests.settings.default_password
        dialog.click_login()
        dialog.wait_dialog_closed()

        self.site.close_all_dialogs(async_close=False)
        self.site.wait_logged_in()

        logged_in = self.site.header.right_menu_button.is_displayed()
        self.assertTrue(logged_in, msg='User is not logged in')

        # logout user for step 6
        self.site.logout()
        self.site.wait_content_state('HomePage', timeout=6)

    def test_006_verify_all_tabs(self):
        """
        DESCRIPTION: Repeat steps 1-5 for :
        EXPECTED: 'MATCHES' tab
        EXPECTED: 'COUPONS' tab
        EXPECTED: 'OUTRIGHTS' tab
        EXPECTED: 'Competition' tab
        """
        self.test_000_tap_football()
        tabs = self.site.football.tabs_menu.items_as_ordered_dict
        self.assertTrue(tabs, msg='No tabs found on Football page')
        tab_names_to_skip = [self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                                     # because this verification is already done in test_001_tap_tab_name
                                                     self.ob_config.football_config.category_id)]

        for name in tabs.keys():
            if name in tab_names_to_skip:
                continue
            self._logger.info(f'*** Repeating steps for "{name}" tab')
            self.test_001_tap_tab_name(name)
            self.test_002_tap_favourite_page_icon()
            self.test_003_tap_back()
            self.test_004_tap_favourite_icon_again()
            self.test_005_tap_login()
            self.navigate_to_page(name='sport/football')
            self.site.wait_content_state(state_name='Football')
