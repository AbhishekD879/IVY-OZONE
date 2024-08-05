import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305063_Verify_User_will_be_able_to_navigate_to_Fanzone_page_from_other_entry_points_when_Show_in_Home_Page_launch_Banner_toggle_is_On(Common):
    """
    TR_ID: C65305063
    NAME: Verify User will be able to navigate to Fanzone page from other entry points when Show in Home Page launch Banner toggle is On
    DESCRIPTION: Verify User will be able to navigate to Fanzone page from other entry points when Show in Home Page launch Banner toggle is On
    PRECONDITIONS: 1) User has already subscribed for Fanzone
    PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
    PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 3) Show In Home Page Launch Banner toggle should be On in Fanzone Configuration(CMS)
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
    PRECONDITIONS: 4) Fanzone related Banner's should be uploaded into SiteCore
    PRECONDITIONS: 5) Image Banner Url field should be inputted Sitecore team Id of the banner we want to display
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Details
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User has already subscribed for Fanzone
        PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
        PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 3) Show In Home Page Launch Banner toggle should be On in Fanzone Configuration(CMS)
        PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
        PRECONDITIONS: 4) Fanzone related Banner's should be uploaded into SiteCore
        PRECONDITIONS: 5) Image Banner Url field should be inputted Sitecore team Id of the banner we want to display
        PRECONDITIONS: CMS-->Fanzone-->Fanzone Details
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        everton_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.everton.title())
        if everton_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.everton.title())
        if not everton_fanzone['fanzoneConfiguration']['homePage']:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.everton.title(), homePage=True)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All teams to be displayed',
                        timeout=5)
        self.__class__.team_name = vec.fanzone.TEAMS_LIST.everton.title()
        team_name = self.site.show_your_colors.items_as_ordered_dict.get(self.team_name)
        team_name.scroll_to_we()
        team_name.click()
        sleep(3)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=10)
        dialog_confirm.confirm_button.click()
        sleep(6)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        self.site.wait_content_state_changed(timeout=10)
        sleep(3)

    def test_001_logon_to_lads_application(self):
        """
        DESCRIPTION: Logon to Lads application
        EXPECTED: User login should be successful
        """
        # covered in preconditions

    def test_002_verify_launch_banner_is_populated_in_home_pagedesktop_and_under_highlights_tab_in_mobile(self):
        """
        DESCRIPTION: Verify Launch Banner is Populated in Home page(desktop) and under Highlights tab in mobile
        EXPECTED: Launch banner should be populated
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")

    def test_003_click_on_let_me_see_button_and_verify_user_is_routed_to_fanzone_page(self):
        """
        DESCRIPTION: Click on 'LET ME SEE' button and verify user is routed to Fanzone Page
        EXPECTED: User should be routed to Fanzone page
        """
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_004_check_user_is_routed_to_subscribed_fanzone_page_as_per_the_fanzone_opted_from_show_your_colors_page(self):
        """
        DESCRIPTION: Check user is routed to subscribed fanzone page as per the Fanzone opted from Show Your Colors page
        EXPECTED: User should be routed to relevant Fanzone Page
        """
        team_name = self.site.fanzone.fanzone_heading
        self.assertIn(self.team_name, team_name, msg=f'Actual team name "{self.team_name}" is not same as expected'
                                                     f'team name "{team_name}"')
