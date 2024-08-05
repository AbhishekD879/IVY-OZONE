import pytest
import tests
from tests.base_test import vtest
from time import sleep
from tests.Common import Common
from datetime import datetime
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305055_To_verify_same_created_promotion_should_be_populated_in_all_the_fanzone(Common):
    """
    TR_ID: C65305055
    NAME: To verify same created promotion should be populated in all the fanzone
    DESCRIPTION: To verify same created promotion should be populated in all the fanzone
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)User has enabled Club toggle in Fanzone page
    PRECONDITIONS: 4)Promotion banners are created in Sitecore
    PRECONDITIONS: 5)User has created promotion in club subsection in Fanzone
    PRECONDITIONS: 6)User has FE url and Valid credentials to Login Lads FE(user credentials of Everton, Liverpool, etc. )
    PRECONDITIONS: 7) User has logged into the application successfully with credentials which is
    """
    keep_browser_open = True

    def subscribe_FanZone_Team(self, team_name=vec.fanzone.TEAMS_LIST.aston_villa.title()):
        self.cms_config.update_fanzone(team_name)
        team_fanzone = self.cms_config.get_fanzone(team_name)
        if team_fanzone['fanzoneConfiguration']['showClubs'] is not True:
            raise CmsClientException('showClubs is not enabled')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state('Homepage')
        self.site.login(username=username)
        self.navigate_to_page(name='sport/football', fanzone=True)
        self.site.wait_content_state(state_name='Football')
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzones are displayed',
                        timeout=5)
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        fanzone[team_name].click()
        sleep(3)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        if tests.settings.device_type == "mobile":
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(
                vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=10,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_000_preconditions(self):
        """
         PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)User has enabled Club toggle in Fanzone page
        PRECONDITIONS: 4)Promotion banners are created in Sitecore
        PRECONDITIONS: 5)User has created promotion in club subsection in Fanzone
        PRECONDITIONS: 6)User has FE url and Valid credentials to Login Lads FE(user credentials of Everton, Liverpool, etc. )
        PRECONDITIONS: 7) User has logged into the application successfully with credentials which is
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        fanzone_clubs = self.cms_config.get_fanzone_club()
        self.__class__.fanzoneclub = []
        for fanzone_club in fanzone_clubs:
            if (fanzone_club['validityPeriodStart'] <= datetime.utcnow().isoformat() <= fanzone_club[
                'validityPeriodEnd']) and fanzone_club['active'] is True:
                self.fanzoneclub.append(fanzone_club)
        if self.fanzoneclub is None:
            raise CmsClientException('fanzone promotions are not available')
        self.subscribe_FanZone_Team()

    def test_001_navigate_to_fanzone_page_everton_team(self):
        """
        DESCRIPTION: Navigate to Fanzone page (Everton team)
        EXPECTED: User should be navigated to Everton Fanzone page
        """
    #     Covered In above step

    def test_002_verify_user_is_able_to_see_club_tab_in_fanzone_page(self):
        """
        DESCRIPTION: Verify user is able to see Club Tab in Fanzone page
        EXPECTED: User should be able to see Club Tab in Fanzone page
        """
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.CLUB, tabs_menu,
                      msg=f'"{vec.fanzone.CLUB}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.CLUB)
        sleep(5)

    def test_003_verify_the_promotion_shown_in_club_tab(self):
        """
        DESCRIPTION: Verify the promotion shown in Club tab
        EXPECTED: User should be able to see all the promotions in club tab which were created in CMS under Club section
        """
        fanzone_banners = self.site.fanzone.tab_content.club_container
        for i in range(len(self.fanzoneclub)):
            self.assertTrue(fanzone_banners.get(self.fanzoneclub[i]['title']).name,
                            msg=f'banner name is not displayed in promotions')

    def test_004_logout_and_login_with_another_credentials_having_another_fanzone_team(self):
        """
        DESCRIPTION: Logout and Login with another credentials having another Fanzone team
        EXPECTED: user should be able to login FE
        """
        self.site.logout()

    def test_005_repeat_step1_3(self):
        """
        DESCRIPTION: Repeat step1-3
        EXPECTED: User should be able the promotions same as seen in step 2 for Everton teams
        """
        self.subscribe_FanZone_Team(team_name=vec.fanzone.TEAMS_LIST.everton.title())
        self.test_002_verify_user_is_able_to_see_club_tab_in_fanzone_page()
        self.test_003_verify_the_promotion_shown_in_club_tab()
        self.test_004_logout_and_login_with_another_credentials_having_another_fanzone_team()

    def test_006_try_the_above_steps_with_other_fanzone_team_and_verify_the_promotions(self):
        """
        DESCRIPTION: Try the above steps with other fanzone team and verify the promotions
        EXPECTED:
        """
        self.subscribe_FanZone_Team(team_name=vec.fanzone.TEAMS_LIST.manchester_city.title())
        self.test_002_verify_user_is_able_to_see_club_tab_in_fanzone_page()
        self.test_003_verify_the_promotion_shown_in_club_tab()
        self.test_004_logout_and_login_with_another_credentials_having_another_fanzone_team()
