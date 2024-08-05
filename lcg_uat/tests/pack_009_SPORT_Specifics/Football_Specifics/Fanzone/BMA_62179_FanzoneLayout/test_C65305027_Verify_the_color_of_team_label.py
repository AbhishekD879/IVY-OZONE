import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305027_Verify_the_color_of_team_label(Common):
    """
    TR_ID: C65305027
    NAME: Verify the color of team label.
    DESCRIPTION: Verify the color of team label.
    PRECONDITIONS: 1) User login should be successful
    PRECONDITIONS: 2) User has already subscribed for Fanzone
    PRECONDITIONS: 3) Fanzone should be enabled in System Configuration
    PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 4) All the entry points should be enabled in Fanzone Configuration(CMS)
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
    PRECONDITIONS: 5) Image should be uploaded in Site core and image id should be inputted while creating the Fanzone for respective teams
    PRECONDITIONS: 6) Fanzone should be enabled in A-Z menu and Sports Ribbon
    PRECONDITIONS: CMS-->Sports Pages-->Sport Categories-->Fanzone-->General Sport Configuration
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User login should be successful
        PRECONDITIONS: 2) User has already subscribed for Fanzone
        PRECONDITIONS: 3) Fanzone should be enabled in System Configuration
        PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 4) All the entry points should be enabled in Fanzone Configuration(CMS)
        PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
        PRECONDITIONS: 5) Image should be uploaded in Site core and image id should be inputted while creating the Fanzone for respective teams
        PRECONDITIONS: 6) Fanzone should be enabled in A-Z menu and Sports Ribbon
        PRECONDITIONS: CMS-->Sports Pages-->Sport Categories-->Fanzone-->General Sport Configuration
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
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
        fanzone[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()

    def test_001_navigate_to_fanzone_page_via_any_of_below_entry_pointsa_fanzone_in_a_z_menub_fanzone_in_sports_ribbonmobile_onlyc_launch_banner_in_home_pagehighlights_tabd_launch_banner_in_football_slp(self):
        """
        DESCRIPTION: Navigate to Fanzone page via any of below entry points
        DESCRIPTION: a) Fanzone in A-Z menu
        DESCRIPTION: b) Fanzone in Sports Ribbon(Mobile only)
        DESCRIPTION: c) Launch banner in Home page/Highlights tab
        DESCRIPTION: d) Launch banner in Football SLP
        EXPECTED: User should be able to navigate to Fanzone Page
        """
        # self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
        # fanzone_banner = self.site.home.fanzone_banner()
        # fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=10,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_002_verify_color_of_the_team_labelex_if_you_choose_everton_it_will_be_blue_if_you_choose_man_united_it_will_be_red(self):
        """
        DESCRIPTION: Verify color of the team label
        DESCRIPTION: Ex: If you choose Everton it will be Blue, If you choose Man United it will be Red
        EXPECTED: Team label color should be based on the Fanzone we have subscribed from Show Your Colors page
        """
        # Using Local var as color is depend on team selected while subscribing
        selected_color = self.site.fanzone.background_color_value
        self.assertEqual(selected_color, vec.colors.TEAM_LABEL_COLOR,
                         msg=f'Team label actual color "{selected_color}"'
                             f' is not as expected team label color '
                             f'"{vec.colors.TEAM_LABEL_COLOR}"')
