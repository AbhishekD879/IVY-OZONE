import pytest
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result, wait_for_haul
from voltron.environments import constants as vec
from tests.Common import Common


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone_reg_tests
@vtest
class Test_C65305073_Verify_accessing_Fanzone_page_from_A_z_menu(Common):
    """
    TR_ID: C65305073
    NAME: Verify accessing Fanzone page from A-z menu
    DESCRIPTION: To verify user should be able to access Fanzone page by clicking on Fanzone option from A-z menu(Device/desktop )

    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: 3)User has FE url and Valid credentials to Login Lads FE
        PRECONDITIONS: 4)User has completed the Fanzone Syc successfully in FE
        """
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
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        wait_for_haul(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        wait_for_haul(3)
        dialog_alert_email = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN)
        if dialog_alert_email:
            dialog_alert_email.remind_me_later.click()
        wait_for_haul(3)
        dialog_alert_fanzone_game = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES)
        if dialog_alert_fanzone_game:
            dialog_alert_fanzone_game.close_btn.click()

    def test_001_hit_the_fe_url_and_login_to_lads_fe(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")

    def test_002_verify_user_is_able_to_see_fanzone_option_in_a_z_menu(self):
        """
        DESCRIPTION: verify user is able to see Fanzone option in A-Z Menu
        EXPECTED: User should be able to see Fanzone option in A-Z menu
        """
        if self.device_type == 'mobile':
            # Top Sports
            self.site.open_sport(name='ALL SPORTS')
            sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
            self.assertIn('Fanzone', sports, msg='Fanzone is present in Top Sports')
            # A-Z Sports
            sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
            self.assertIn('Fanzone', sports, msg='Fanzone is present in A-Z Sports')
        else:
            # A - Z Sports
            self.__class__.sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertIn('Fanzone', self.sports, msg='Fanzone is present in A-Z Sports')

    def test_003_click_on_the_fanzone_option_from_the_menu(self):
        """
        DESCRIPTION: Click on the Fanzone option from the menu
        EXPECTED: User should be navigated to Fanzone page
        """
        if self.device_type == 'mobile':
            self.site.all_sports.click_item(vec.sb.FANZONE)
        else:
            self.site.sport_menu.click_item(vec.sb.FANZONE)
        wait_for_haul(3)
        self.assertEqual(self.site.fanzone.header_line.page_title.text, vec.sb.FANZONE,
                         msg=f'Actual page title "{self.site.fanzone.header_line.page_title.text}" '
                             f'is not same as Expected title "{vec.sb.FANZONE}"')
