import pytest
from tests.Common import Common
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result, wait_for_haul
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_h1
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@pytest.mark.adhoc24thJan24
@pytest.mark.adhoc_suite
@vtest
class Test_C66017365_Verify_21st_team_subscribed_Fanzone_RGY_user_is_navigating_to_Now_Nexttab(Common):
    """
    TR_ID: C66017365
    NAME: Verify 21st team subscribed Fanzone RGY user is navigating to Now & Next tab
    DESCRIPTION: RGY user who subscribed to 21st team fan zone user should land on 'Now & Next' tab by default when it is enable.
    DESCRIPTION: If disabled should land on any other active tab
    PRECONDITIONS: In CMS navigate to Fanzone&gt; Fanzones&gt; Fanzone FC &gt; under Now & Next sub tab&gt;enable 'Show Now & Next' then under Clubs sub tab&gt;enable 'Show Clubs' &gt; then under Fanzone games subtab enable all the fields.
    PRECONDITIONS: User who subscribed to fanzone 21st team should be available.
    """
    keep_browser_open = True
    fanzone_name = "Fanzone FC"

    def test_000_preconditions(self):
        """
        Description : Checking whether "Now & Next" and "Show Clubs" is enabled or not in "Fanzone FC"/"Fanzones" in cms.
        """
        # getting whole fanzone_fc data
        fanzone_fc = self.cms_config.get_fanzone(self.fanzone_name)
        if not fanzone_fc:
            raise VoltronException('Cannot get Gaming promotions external link')
        # *****************************************************************
        is21st_Or_Unlisted_Fanzone_Team = fanzone_fc.get('is21stOrUnlistedFanzoneTeam')
        if not is21st_Or_Unlisted_Fanzone_Team:
            self.cms_config.update_fanzone(self.fanzone_name, is21stOrUnlistedFanzoneTeam=True)
        fanzone_configuration = fanzone_fc.get('fanzoneConfiguration')
        # *****************************************************************
        show_Now_Next = fanzone_configuration.get('showNowNext')
        if not show_Now_Next:
            self.cms_config.update_fanzone(self.fanzone_name, showNowNext=True)
        # *****************************************************************
        show_Clubs = fanzone_configuration.get('showClubs')
        if not show_Clubs:
            self.cms_config.update_fanzone(self.fanzone_name, showClubs=True)
        # *****************************************************************
        show_games = fanzone_configuration.get('showGames')
        show_slot_rivals = fanzone_configuration.get('showSlotRivals')
        show_scratch_cards = fanzone_configuration.get('showScratchCards')
        if not show_games:
            self.cms_config.update_fanzone(self.fanzone_name, showGames=True)
        if not show_slot_rivals and not show_scratch_cards:
            self.cms_config.update_fanzone(self.fanzone_name, showSlotRivals=True, showScratchCards=True)

    def test_001_login_to_the_application_with_rgy_user_who_is_already_subscribed_to_fanzone_21st_team(self):
        """
        DESCRIPTION: Login to the application with RGY user who is already subscribed to Fanzone 21st team
        EXPECTED: Logged in successfully
        """
        # Checking whether user has been subscribed user or not
        self.site.login(username="Ganeshgunjal99", password="Sand1234")
        self.site.wait_content_state(state_name='Homepage')

    def test_002_now_click_on_fanzone_menu_item_either_from_top_menu_or_left_menu(self):
        """
        DESCRIPTION: Now click on Fanzone menu item either from top menu or left menu
        EXPECTED: Should navigate to Fanzone page.
        """
        if self.device_type == 'desktop':
            self.assertTrue(self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.FANZONE.upper()),
                            msg="Fanzone option is not displayed in Sports Ribbon Menu")
        else:
            self.assertTrue(self.site.home.menu_carousel.items_as_ordered_dict.get(vec.sb.FANZONE),
                            msg="Fanzone option is not displayed in Sports Ribbon Menu")
            # ***********************************************************************************
        if self.device_type == 'desktop':
            self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.FANZONE.upper()).click()
        else:
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.sb.FANZONE).click()

    def test_003_validate_the_landing_position_of_user(self):
        """
        DESCRIPTION: Validate the landing position of user
        EXPECTED: By default user should land on 'Now &amp; Next' tab.
        """
        self.site.wait_content_state_changed(timeout=30)
        dialog_alert_fanzone_game = wait_for_result(
            lambda: self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES, verify_name=False),
            timeout=3,
            name=f'Dialog "{vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES}" to display',
            bypass_exceptions=VoltronException)
        if dialog_alert_fanzone_game and dialog_alert_fanzone_game.name.title() == vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES.title():
            dialog_alert_fanzone_game.close_btn.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu.current, name='Fanzone page not displayed', timeout=10)
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}" is not same expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_004_in_cms_now_disable_the_show_now_amp_next_toggle_button_under_fanzone_fcampgtnow_amp_next_sub_tab(self):
        """
        DESCRIPTION: In CMS now disable the 'Show Now &amp; Next' toggle button under Fanzone FC&amp;gt;Now &amp; Next sub tab
        EXPECTED: Button is disabled
        """
        fanzone_fc = self.cms_config.get_fanzone(self.fanzone_name)
        now_next_tab_status = fanzone_fc['fanzoneConfiguration']['showNowNext']
        wait_for_haul(10)
        if now_next_tab_status:
            self.cms_config.update_fanzone(self.fanzone_name, showNowNext=False)
        # it will take few seconds to reflect in front end
        wait_for_haul(20)

    def test_005_logout_form_the_application_and_login_again_with_same_user(self):
        """
        DESCRIPTION: Logout form the application and login again with same user
        EXPECTED: Logged in successfully
        """
        self.device.driver.execute_script('localStorage.clear();')
        self.device.driver.refresh()
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(), msg='User has not logged out!')
        self.site.login(username="Ganeshgunjal99", password="Sand1234")
        self.site.wait_content_state('HomePage')

    def test_006_navigate_to_fanzone_screen_and_validate_the_landing(self):
        """
        DESCRIPTION: Navigate to Fanzone screen and validate the landing.
        EXPECTED: On Fanzone page, user should land on any active tab. In this case user should land on 'Clubs' since 'Now &amp; Next' tab is disabled.
        """
        if self.device_type == 'desktop':
            self.assertTrue(self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.FANZONE.upper()),
                            msg="Fanzone option is not displayed in Sports Ribbon Menu")
        else:
            self.assertTrue(self.site.home.menu_carousel.items_as_ordered_dict.get(vec.sb.FANZONE),
                            msg="Fanzone option is not displayed in Sports Ribbon Menu")
            # **********************************************************************************
        if self.device_type == 'desktop':

            self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.FANZONE.upper()).click()
        else:
            all_sports = self.site.home.menu_carousel.items_as_ordered_dict
            all_sports.get(vec.sb.FANZONE).click()
            # **********************************************************************************
        dialog_alert_fanzone_game = wait_for_result(
            lambda: self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES, verify_name=False),
            timeout=3,
            name=f'Dialog "{vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES}" to display',
            bypass_exceptions=VoltronException)
        if dialog_alert_fanzone_game and dialog_alert_fanzone_game.name.title() == vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES.title():
            dialog_alert_fanzone_game.close_btn.click()
        # **********************************************************************************
        self.site.wait_content_state_changed(timeout=30)
        wait_for_result(lambda: self.site.fanzone.tabs_menu.current, name='Fanzone page not displayed', timeout=10)
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab.upper(), vec.fanzone.FANZONE_GAMES,
                         msg=f'Actual Tab "{current_tab.upper()}" is not same expected tab "{vec.fanzone.FANZONE_GAMES}"')
