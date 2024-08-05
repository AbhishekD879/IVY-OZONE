import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.fanzone
@vtest
class Test_C65305084_Verify_User_navigated_away_using_footer_menu(Common):
    """
    TR_ID: C65305084
    NAME: Verify User navigated away using footer menu
    DESCRIPTION: To verify user is able to navigate away from Fanzone page by clicking on any footer menu in the device
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)User has FE url and Valid credentials to Login Lads FE
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                           typeId=self.football_config.autotest_class.autotest_premier_league.type_id)

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='OK button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=15)
        dialog_confirm.confirm_button.click()
        sleep(6)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS, timeout=15)
        dialog_alert.exit_button.click()

    def test_001_hit_the_fe_url_and_login_to_lads_fe(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application, User is on Homepage
        """
        # covered in preconditions

    def test_002_now_navigate_homepage_football_slpa_z_menusports_ribbon(self):
        """
        DESCRIPTION: Now navigate Homepage /Football slp/A-Z menu/Sports ribbon
        EXPECTED: User should be navigated to Homepage /Football slp/A-Z menu/Sports ribbon
        """
        # covered in preconditions

    def test_003_click_on_fanzone__launch_banner_from_homepage_football_slpa_z_menusports_ribbon(self):
        """
        DESCRIPTION: Click on Fanzone  Launch banner from Homepage /Football slp/A-Z menu/Sports ribbon
        EXPECTED: User is navigated to Fanzone Page
        """
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_004_Click_on_any_tab_from_footer_menu(self):
        """
        DESCRIPTION:Click on any tab from footer menu
        EXPECTED: User is navigated away from fanzone page
        """
        menu_items = self.site.navigation_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Footer menu items are not found')

        my_bets = menu_items.get(vec.sb.MY_BETS_FOOTER_ITEM)
        my_bets.click()
        self.site.wait_content_state_changed()
        current = self.device.get_current_url()
        expected_value = 'fanzone'
        self.assertNotIn(expected_value, current, msg='User is not navigated away from fanzone page')
