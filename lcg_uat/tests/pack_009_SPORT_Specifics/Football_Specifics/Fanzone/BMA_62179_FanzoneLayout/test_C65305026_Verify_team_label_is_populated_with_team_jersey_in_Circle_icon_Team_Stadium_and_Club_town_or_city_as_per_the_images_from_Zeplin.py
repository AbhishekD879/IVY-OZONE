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
@pytest.mark.fanzone
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C65305026_Verify_team_label_is_populated_with_team_jersey_in_Circle_icon_Team_Name_Stadium_Name_and_Club_town_or_city_as_per_the_images_from_Zeplin(Common):
    """
    TR_ID: C65305026
    NAME: Verify team label is populated with team jersey in Circle icon, Team Name, Stadium Name, and Club town or city as per the images from Zeplin
    DESCRIPTION: Verify team label is populated with team jersey in Circle icon, Team Name, Stadium Name, and Club town or city as per the images from Zeplin
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

    def test_000_precondition(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.__class__.aston_villa = vec.fanzone.TEAMS_LIST.aston_villa.title()
        astonVilla_fanzone = self.cms_config.get_fanzone(self.aston_villa)
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state('Homepage')
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams.get(self.aston_villa).scroll_to_we()
        teams.get(self.aston_villa).click()
        sleep(3)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_(self):
        """
        DESCRIPTION:
        EXPECTED: User should be able to navigate to Fanzone Page
        """
        # fanzone_banner = self.site.home.fanzone_banner()
        # fanzone_banner.let_me_see.click() as per the new change, after subscription, we will be in fanzone page only
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')

    def test_002_team_label_is_populated_with_team_jersey_in_circle_icon(self):
        """
        DESCRIPTION: Team label is populated with team jersey in Circle icon
        EXPECTED: team label should be populated with team jersey in Circle icon
        """
        self.assertTrue(self.site.fanzone.team_icon.is_displayed(), msg='team jersey is not found')

    def test_003_team_name_stadium_name_and_club_towncity_will_populate_per_the_images_from_zeplin(self):
        """
        DESCRIPTION: Team Name, Stadium Name, and Club town/city will populate per the images from Zeplin
        EXPECTED: Team Name, Stadium Name, and Club town/city should populate as per the images from Zeplin
        EXPECTED: Note: This title's are configurable from CMS
        """
        fanzone = self.cms_config.get_fanzone(fanzone_name=self.aston_villa)
        result = self.site.fanzone.fanzone_heading.split('\n')
        self.assertEqual(fanzone['assetManagementLink'], result[0].upper(),
                         msg=f'Actual team title {result[0].upper()} is not same as '
                             f'expected title {fanzone["assetManagementLink"]}')
        self.assertEqual(fanzone['location'].upper(), result[1].upper(),
                         msg=f'Actual location {result[1].upper()} is not same as '
                             f'expected location {fanzone["location"].upper()}')
